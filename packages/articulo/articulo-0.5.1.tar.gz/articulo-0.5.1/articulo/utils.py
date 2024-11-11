"""
This file contains the utility functions that are used in the main module.
"""
from urllib.parse import urlparse

from bs4 import Tag, Comment

from articulo.constants import tags_to_completely_remove, important_content_tags


def sanitize_html(content: Tag) -> Tag:
    """
    This function will sanitize the HTML content by removing all the unnecessary tags and comments.
    """
    # Filtering all the non-important tags.
    for tag in content.find_all(True):  # find_all(True) will match any tag
        if tag.decomposed:
            continue
        # First, we need to remove all the tags that should be completely removed
        if tag.name in tags_to_completely_remove:
            tag.decompose()
        # Then, we need to unwrap all the tags that has important content
        # but not needed by themselves
        elif tag.name not in important_content_tags:
            tag.unwrap()

    # Removing all the comments
    comments = content.find_all(string=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    return content


def get_dublincore_element(data, key):
    """
    Gets dublincore element by key
    """
    for item in data:
        for element in item.get("elements"):
            if element.get("name") == key:
                return element.get("content")
    return None


def get_json_ld_element(data: list[dict], key):
    """
    Gets json-ld element by key
    """
    for item in data:
        return item.get(key)
    return None


def get_og_element(data, key):
    """
    Gets opengraph element by key
    """
    for item in data:
        for element in item.get("properties"):
            (og_key, og_value) = element
            if og_key == key:
                return og_value
    return None


def is_url(maybe_url):
    """
    Checks if the string is url
    """
    try:
        result = urlparse(maybe_url)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False
