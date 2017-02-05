## Mine sheet htmls from http://collegehockeyinc.com/stats/compnatfull17.php

import requests
import os
from random import random
from time import sleep

from bs4 import BeautifulSoup

class Scraper:
    '''
    Scraper class for web scraping from different urls.
    '''
    _crawl_delay = 5
    session = requests.Session()
    
    default_headers = {
        'Accept-Encoding': 'gzip, deflate', 
        'User-Agent': 'python-requests/2.10.0', 
        'Connection': 'keep-alive', 
        'Accept': '*/*'
    }
    
    VPN_headers = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, sdch',
        'Accept-Language' : 'en-US,en;q=0.8',
        'Cookie' : 'm-b="ogpzsIqVdn5cbkqyG805Nw\\075\\075"; m-css_v=08e0dd11ea429f2f18; m-f=uJLMebqkiLKv7TBkILbpQ-Zr0vNiWTsEh4Kn; m-depd=62678c660bffdc59; m-s="R4t2Vt7ibXEK1_7nJ28e8A\075\075"; m-t="A10CxVk3FrWF4ah8GDuI2w\\075\\075"; m-tz=240; _ga=GA1.2.1313483809.1446236737',
        'DNT' : 1,
        'Referer' : 'https://www.google.com/',
        'Upgrade-Insecure-Requests' : 1,
        'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'X-DevTools-Emulate-Network-Conditions-Client-Id' : '4DDEEF36-D4E9-4ABE-8890-EE2619143DC6'
    }

    def set_crawl_delay(self, seconds=5):
        """
        Set crawl delay in seconds. Default 5 seconds.

        Parameters:
        -----------
        :param seconds: number of seconds to delay the scraper. 
        :return: None
        """
        assert isinstance(seconds, (int, float)), AttributeError("Crawl delay must be a positive number.")
        assert seconds >= 0, AttributeError("Cannot set a negative crawl delay.")
        self._crawl_delay = seconds

    def write_html(self, url, path, use_VPN=False, overwrite=False, encoding='UTF-8'):
        '''
        Write html source code from url to user-defined path encoded as UTF-8.
        Creates directories as necessary.
        Will not overwrite a file unless told to do so.
        Writes a commented ID line to top of html for identifying purposes.

        Parameters:
        -----------
        :param url: Full url to site.
        :param path: Full path to file.
        :param use_VPN: Whether to use VPN headers in request. Requests are slower if True. (default False)
        :param overwrite: Whether to overwrite existing files. (default False)
        :param encoding: Type of encoding. (default UTF-8)
        :return: True

        Errors:
        -------
        TypeError - url or path parameters not a string. No exceptions.
        LookupError - User specified unknown encoding.

        Returns:
        --------
        None - If file exists and should not be overwritten.
        path - If file is written without error.
        '''

        assert isinstance(url, str), TypeError('`url` must be a string')
        assert isinstance(path, str), TypeError('`path` must be a string')
        assert isinstance(use_VPN, bool), TypeError('`headers` must be a bool')
        assert isinstance(overwrite, bool), TypeError('`headers` must be a bool')
        
        assert path.endswith('.txt'), AssertionError('path parameter does not lead to txt file.')
        
        parent, child = os.path.split(path)
        if os.path.exists(path) and not overwrite:
            print('\t{} already exists. File was not overwritten.'\
                    .format(path), end='\r')
            return None
        elif not os.path.exists(parent):
            os.makedirs(parent)

        # Implement crawl delay here.
        sleep(self._crawl_delay)
        
        if use_VPN:
            session.headers = self.VPN_headers
        else:
            session.headers = self.default_headers
        
        try:
            r = session.get(url)
        except requests.exceptions.ConnectionError as e:
            print('Your internet may be disconnected.', end='\r')
            raise e
        else:
            if encoding.lower() == 'utf-8':
                soup = BeautifulSoup(r.content, 'html.parser')
                pretty_html = soup.prettify()
            else:
                soup = BeautifulSoup(r.text, 'html.parser')
                pretty_html = soup.prettify().encode(encoding)

        # We may want to uniquely identify the subjects of these htmls later.
        ID = str(random())[2:12]
        print('\tsaving', path, end='         \r')
        with open(path, 'wb') as html_txt:
            ID_line = '''<!--ID: %s-->\n''' % ID
            ID_line = ID_line.encode(encoding)
            html_txt.write(ID_line)
            try:
                html_txt.write(pretty_html.encode(encoding))
            except LookupError as err:
                # This probably won't ever be triggered, but just in case.
                print('LookupError triggered in write_html')
                print(LookupError, err)
                raise
        return path
