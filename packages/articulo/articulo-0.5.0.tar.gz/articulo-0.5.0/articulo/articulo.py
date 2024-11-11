#!/usr/bin/env python3

"""This is Articulo.
Tiny library for extracting html article content."""

import re
from functools import cached_property
from typing import Union
from urllib.parse import urlparse, urlunparse

import extruct
import validators
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from requests import RequestException

from .exceptions import (
    HTTPErrorException,
    MaxIterations,
    NoTitleException,
    NoHTMLException,
    DecodingException,
)
from .utils import (
    sanitize_html,
    get_json_ld_element,
    is_url,
)


class Articulo:
    """
    Articulo is the only and basic class of this library.
    Usage is really staightforward and simple: just import this class
    and instantiate with link as a parameter.
    """

    __max_iterations_count = 100

    def __init__(
        self,
        link_or_content: str,
        threshold: float = 0.7,
        verbose: bool = False,
        http_headers: Union[dict, None] = None,
        def_charset: str = "utf-8",
    ) -> None:
        """
        Article object

        Params:
        :link_or_content: Link to the article or content of the article, that should be processed.
        :threshold (optional): Max information loss coefficient, that affects content parsing.
        :verbose (optional): Verbose mode. If enabled than all the operations will be logged.
        :http_headers (optional): Additional headers for HTTP request. There is no default headers.
        :def_charset (optional): Default charset for article html. Default is utf-8.
        """

        self.__link_or_content = link_or_content
        self.__threshold = threshold
        self.__verbose = verbose
        self.__http_headers = http_headers
        self.__def_charset = def_charset

    @property
    def title(self):
        """
        Parsed article title
        """
        return self.__clean_title_text(self.__title_element.text)

    @property
    def text(self):
        """
        Parsed article main content text.
        """
        markup = self.__content_markup
        if markup is None:
            return None
        return self.__content_markup.text

    @property
    def markup(self):
        """
        Article main content html markup.
        """
        if self.__content_markup is None:
            return None
        return str(self.__content_markup)

    @cached_property
    def description(self):
        """
        Article short description.
        """
        return self.__try_get_meta_content(
            ["name", "property"],
            ["description", "og:description", "twitter:description"],
        )

    @cached_property
    def preview(self):
        """
        Dict with article icons.
        Keys are sizes and values are links to icons.
        """
        preview = self.__try_get_meta_content(
            ["name", "property"], ["og:image", "twitter:image", "twitter:image:src"]
        )

        if not preview is None:
            preview = self.__get_absolute_link(preview)
        return preview

    @cached_property
    def icon(self):
        """
        Link to article icon.
        The biggest possible icon will be returned if there are
        multiple icons and size attribute provided.
        In other case will be returned first icon.
        """
        icon_src = None
        last_biggest_size = 0

        soup = BeautifulSoup(self.__html, features="lxml")
        icons_meta = soup.findAll("link", attrs={"rel": "icon"})
        for icon in icons_meta:
            href: Union[str, None] = icon.get("href")
            sizes: Union[str, None] = icon.get("sizes")

            if href is None:
                continue

            if sizes is None:
                if icon_src is None:
                    icon_src = self.__get_absolute_link(href)
                continue

            for size in sizes.split(" "):
                if re.match(r"\d+x\d+", size):
                    [width, _] = [int(i) for i in size.split("x")]
                    if width > last_biggest_size:
                        icon_src = self.__get_absolute_link(href)
                        last_biggest_size = width
                else:
                    self.__log(f"Invalid size attribute: {size} for icon {href}")
                    icon_src = self.__get_absolute_link(href)
        return icon_src

    @cached_property
    def keywords(self):
        """
        List of article's keywords.
        """
        kw_str = self.__try_get_meta_content(["name"], ["keywords"], "")
        return [] if len(kw_str) == 0 else [kw.strip() for kw in kw_str.split(",")]

    @cached_property
    def rss(self):
        """
        Link to article's RSS feed.
        """
        soup = BeautifulSoup(self.__html, features="lxml")
        links = soup.findAll("link", attrs={"type": "application/rss+xml"})

        if len(links) == 0:
            links = soup.findAll("link", attrs={"type": "application/atom+xml"})

        if len(links) == 0:
            return links

        return [self.__get_absolute_link(link.attrs.get("href")) for link in links]

    @cached_property
    def has_paywall(self):
        """
        Check if article has paywall.
        """

        if "json-ld" in self.__microformat:
            is_accessable_for_free = get_json_ld_element(
                self.__microformat.get("json-ld", []), "isAccessibleForFree"
            )
            return (
                is_accessable_for_free is False
                or is_accessable_for_free == "False"
                or False
            )
        return False

    @cached_property
    def __content_markup(self):
        """
        Parses article HTML and returns the main article content markup using recursion.
        """
        soup = BeautifulSoup(self.__html, features="lxml")
        raw_content = self.__look_for_best_parent(soup.body, 0)
        if raw_content is None:
            return raw_content

        sanitized_content = self.__sanitize_content(raw_content)
        return sanitized_content

    @cached_property
    def __microformat(self):
        try:
            return extruct.extract(self.__html, base_url=self.__link_or_content)
        except ValueError:
            return {}

    @cached_property
    def __title_element(self):
        """
        Parses article html and returns article title.
        This method assumes, that article HTML has two things:
        * title tag - as an initial title
        * any tag at the body with matching content - as a reference point for the article content
        """

        soup = BeautifulSoup(self.__html, features="lxml")
        title = soup.find("title")

        if title is None:
            raise NoTitleException(self.__link_or_content)

        title_text = title.text
        title_meta = self.__try_find_meta(
            ["property", "name"], ["og:title", "twitter:title"]
        )

        if title_meta is not None:
            title_text = title_meta.get("content")

        possible_titles = soup.findAll(["h1", "h2", "h3", "h4", "h5", "h6", "p"])

        for p_title in possible_titles:
            if not isinstance(p_title.text, str) or len(p_title.text.strip()) == 0:
                continue
            pt_text = self.__clean_title_text(p_title.text)
            normalized_title_text = self.__clean_title_text(title_text)

            if normalized_title_text in pt_text or pt_text in normalized_title_text:
                return p_title

        return title

    @cached_property
    def __html(self) -> Union[str, None]:
        """
        Loads article html from link provided at the moment of an Articulo object instantiation.
        Returns full page html or None if request was not successful.
        """
        if is_url(self.__link_or_content):
            text = self.__get_html_by_url()
        else:
            text = self.__link_or_content

        if text is None or len(text) == 0:
            raise NoHTMLException(self.__link_or_content)

        return text

    def __get_html_by_url(self):
        """
        Gets the article content from the url
        """
        self.__log(f"Start loading article from {self.__link_or_content}...")
        response = requests.get(
            self.__link_or_content, timeout=2000, headers=self.__http_headers
        )
        response.encoding = self.__def_charset

        try:
            response.raise_for_status()
        except RequestException as exc:
            self.__log("Error loading an article.")
            raise HTTPErrorException(
                f"Http error: {response.reason}", response.status_code
            ) from exc
        self.__log("Article loaded.")

        try:
            return response.content.decode(self.__def_charset)
        except ValueError as exc:
            raise DecodingException(self.__link_or_content, self.__def_charset) from exc

    def __try_find_meta(
        self, attr_keys: list[str], attr_values: list[str]
    ) -> Union[Tag, NavigableString, None]:
        """
        Looks for metatags content by their names
        """
        soup = BeautifulSoup(self.__html, features="lxml")
        for key in attr_keys:
            for val in attr_values:
                if soup.findAll("meta", attrs={key: val}):
                    return soup.find("meta", attrs={key: val})

        return None

    def __try_get_meta_content(
        self, attr_keys: list[str], attr_values: list[str], defval=None
    ):
        soup = self.__try_find_meta(attr_keys, attr_values)
        if soup is None:
            return defval

        return soup.get("content")

    def __look_for_best_parent(self, parent: Tag, iter_counter: int):
        """
        Recursively searches for the best parent element containing the main article content.
        """
        self.__log(
            f'Looking for an element containing "{self.__title_element.text}" title inside {parent.name.upper()} tag...'  # pylint: disable=line-too-long
        )

        if parent == self.__title_element.parent:
            self.__log(
                f"{parent.name.upper()} is equal to title's parent element. Best possible parent is found."  # pylint: disable=line-too-long
            )
            return parent

        if iter_counter >= self.__max_iterations_count:
            raise MaxIterations(
                "Cannot find the best parent element within the maximum iterations."
            )  # pylint: disable=line-too-long

        best_parent = None

        for child in parent.children:
            if isinstance(child, NavigableString):
                self.__log(f'Skipping the "{child}" string...')
                continue

            if (
                child.find(self.__title_element.name, string=self.__title_element.text)
                is None
            ):
                self.__log(
                    f'Not found "{self.__title_element.text}" inside {child.name.upper()} tag. Skipping...'  # pylint: disable=line-too-long
                )
                continue

            self.__log(
                f'Found a {child.name.upper()} child tag with "{self.__title_element.text} inside."'  # pylint: disable=line-too-long
            )
            best_parent_content_length = len(parent.text)
            child_content_length = len(child.text)

            information_loss_coeff = 1.0 - (
                child_content_length / best_parent_content_length
            )
            if information_loss_coeff > self.__threshold:
                self.__log(
                    f"Content loss coefficient: {information_loss_coeff}. The best possible parent is {parent.name.upper()}."  # pylint: disable=line-too-long
                )
                best_parent = parent
                break

            iter_counter += 1

        if best_parent:
            return best_parent

        # Recursively search in child elements
        for child in parent.children:
            if isinstance(child, Tag):
                result = self.__look_for_best_parent(child, iter_counter)
                if result:
                    return result

        return None

    def __sanitize_content(self, content: Tag) -> Tag:
        """
        Sanitizes article content from unnecessary tags.
        """
        self.__log("Sanitizing article content...")
        return sanitize_html(content)

    def __get_absolute_link(self, link: str) -> str:
        """
        Makes absolute link from relative
        """
        if not validators.url(link):
            parsed_url = urlparse(self.__link_or_content)
            parsed_url = parsed_url._replace(path=link)
            return urlunparse(parsed_url)
        return link

    def __clean_title_text(self, text: str):
        """
        Cleans text from special and newline characters
        """
        nbsp = "\xa0"
        pt_text = re.sub(r"\n+.+", "", text.strip()).replace(nbsp, " ").strip()
        return pt_text

    def __log(self, message: str) -> None:
        """
        Logs message if object instantiated with verbose mode.
        Params:
        @message: message to log
        """
        if self.__verbose:
            print(message)
