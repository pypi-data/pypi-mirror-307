[![codecov](https://codecov.io/gh/mrmegatelo/articulo/graph/badge.svg?token=4UDVH5KHWP)](https://codecov.io/gh/mrmegatelo/articulo)
[![Python Versions](https://img.shields.io/pypi/pyversions/articulo)](PyPI)
[![PyPI - Version](https://img.shields.io/pypi/v/articulo)](Version)
![GitHub](https://img.shields.io/github/license/mrmegatelo/articulo)


# Articulo
Tiny library for extraction articles from html.  
It can extract the content of an article, both in text and HTML, and it's title.

## Usage
### Basic usage
This library is designed to be as simple as possible.  
To start using it just import it and instantiate with link you want to parse as a parameter.  

Also the library designed to work in lazy manner.  
So, until you make a request for some property, it does not send any requests.  

```python
from articulo import Articulo

# Step 1: initializing Articulo instance
article = Articulo('https://info.cern.ch/')

# Step 2: requesting article properties. All properties resolve lazily.
print(article.title) # article title as a string
print(article.text) # article content as a string
print(article.markup) # article content as an html markup string
print(article.icon) # link to article icon
print(article.description) # article meta description
print(article.preview) # link to article meta preview image
print(article.keywords) # article meta keywords list
```

### Verbose mode
In case you want to see the whole procees just provide parameter `verbose=True` to the instance. It can be helpful for debugging.


```python
from articulo import Articulo

# Initializing Articulo instance with verbose mode
article = Articulo('https://info.cern.ch/', verbose=True)
```

### Controlling information loss coefficient
The whole idea of parsing article content is to define the part of the document that has the highest information density. To find that part there is the so-called `information loss coefficient`. This coefficient determines the decrease in the text density of the document during parsing.  

The default value is `0.7` which stands for `70%` information density decrease. In most cases, this works fine.  
Nevertheless, you can change it in case you have insufficient parsing results. Just provide `theshold` parameter to the `articulo` instance, it might help.

```python
from articulo import Articulo

# Initializing Articulo instance with information loss coefficient of 30%
article = Articulo('https://info.cern.ch/', threshold=0.3)
```

### Providing headers
In some cases  you need to provide additional headers to get an article html from url.  
For that case you can provide headers with `http_headers` parameter when 
you create new instance of `articulo`.

```python
from articulo import Articulo

# Initializing Articulo instance with custom user agent
headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36' }
article = Articulo('https://info.cern.ch/', http_headers=headers)
```

### Providing custom charset
Articulo uses `requests` library to get html from url. This library tries to guess the encoding of the response based on the HTTP headers.
Although it works fine most of the time, in some cases this might not work as expected, and you'll get a mess instead of text. For that case you can provide custom charset with `def_charset` parameter when you create new instance of `articulo`.

```python
from articulo import Articulo

# Initializing Articulo instance with cp1251 charset
article = Articulo('https://info.cern.ch/', def_charset='cp1251')
```