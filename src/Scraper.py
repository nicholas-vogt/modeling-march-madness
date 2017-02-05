#!/usr/bin/python
# In Unix, an executable file that's meant to be interpreted can indicate 
# what interpreter to use by having a #! at the start of the first line, 
# followed by the interpreter (and any flags it may need).
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script

# Everything pertaining to the main scraper class.

from copy import deepcopy
from random import randrange
import requests
import os
from time import sleep

from bs4 import BeautifulSoup

class Scraper:
    """Scraper class for web scraping from different urls.
    
    Methods:
        __init__ (None) -- Initialize scraper.
        set_crawl_delay (None) -- Set crawl delay to a positive int.
        write_html (None) -- Write given url to disc at specified path. 
        
    Todo:
        Give option for randomized crawl delay. Adds protection against bot detectors.
    """
    _session = requests.Session()
    
    _default_headers = {
        'Accept-Encoding': 'gzip, deflate', 
        'User-Agent': 'python-requests/2.10.0', 
        'Connection': 'keep-alive', 
        'Accept': '*/*'
    }
    
    # Insert your own VPN headers here
    _VPN_headers = deepcopy(_default_headers)
    
    
    def __init__(self, *, use_VPN=False, encoding='UTF-8', crawl_delay=5):
        """Initialize Scraper class.
        
        Keyword arguments:
            use_VPN (bool) -- Whether to use VPN headers in request. Requests are slower if True. (default False)
            encoding (str) -- Which encoding to use when writing html to disk. (default 'UTF-8')
            crawl_delay (int, float) -- Number of seconds to delay the scraper.
        
        Returns: None
        """
        assert isinstance(use_VPN, bool), TypeError('use_VPN parameter must be True or False')
        assert isinstance(encoding, str), TypeError('encoding parameter must be a str')        
        assert isinstance(crawl_delay, (int, float)), TypeError('crawl_delay parameter must be a positive int or float')
        assert crawl_delay >= 0, TypeError('crawl_delay parameter must be a positive int or float')
        
        try:
            'a'.encode(encoding)
        except LookupError as err:
            raise LookupError("encoding parameter is not valid.")
        
        self._session.headers = self._default_headers
        if use_VPN:
            self._session.headers = self._VPN_headers
        self._encoding = encoding
        self._crawl_delay = crawl_delay
        
        return None

    def set_crawl_delay(self, seconds=5):
        """Set crawl delay in seconds. Default 5 seconds.

        Arguments:
            seconds (int, float) -- Number of seconds to delay the scraper.

        Returns: None
        """
        assert isinstance(seconds, (int, float)), TypeError('seconds parameter must be a positive int or float')
        assert seconds >= 0, TypeError('seconds parameter must be a positive int or float')
        self._crawl_delay = seconds
        
        return None

    
    def write_html(self, url, path, *, overwrite=False):
        """Write html source code from url to user-defined path as encoded byte string.
        Creates directories as necessary. Will not overwrite a file unless told to do so.
        Writes a commented hexadecimal ID line to top of html for identifying purposes.

        Arguments:
            url (str) -- Full url to site.
            path (str) -- Full path to txt file.
        
        Keyword arguments:
            overwrite (bool) -- Whether to overwrite existing files. (default False)
        
        Errors:
            TypeError -- url or path parameters not a string. No exceptions.
            LookupError -- User specified unknown encoding.

        Returns: None
        """
        assert isinstance(url, str), TypeError('`url` must be a string')
        assert isinstance(path, str), TypeError('`path` must be a string')
        assert path.endswith('.txt'), AssertionError('path parameter does not lead to txt file.')
        assert isinstance(overwrite, bool), TypeError('`headers` must be a bool')
        
        parent, child = os.path.split(path)
        if os.path.exists(path) and not overwrite:
            print('\t{} already exists. File was not overwritten.'\
                    .format(path), end='\r')
            return None
        elif not os.path.exists(parent):
            os.makedirs(parent)

        sleep(self._crawl_delay)
        
        try:
            r = self._session.get(url)
        except requests.exceptions.ConnectionError as e:
            print('Your internet may be disconnected.', end='\r')
            raise e
        
        if self._encoding.lower() == 'utf-8':
            soup = BeautifulSoup(r.content, 'html.parser')
            pretty_html = soup.prettify()
        else:
            soup = BeautifulSoup(r.text, 'html.parser')
            pretty_html = soup.prettify().encode(self._encoding)

        # We may want to uniquely identify the subjects of these htmls later.
        ID = hex(randrange(16**30))
        print('\tsaving', path, end='         \r')
        with open(path, 'wb') as html_txt:
            ID_line = '''<!--ID: %s-->\n''' % ID
            ID_line = ID_line.encode(self._encoding)
            html_txt.write(ID_line)
            html_txt.write(pretty_html.encode(self._encoding))
        
        return None
