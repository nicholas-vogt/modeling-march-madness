import os

from bs4 import BeautifulSoup

from Exceptions import OverwriteError

class Miner:
    """Base class for other Miners.

    Attributes:
        days (List (str)) -- Days of the week.
        writer (ioBufferedWriter) -- Initialized in init.
        soup (BeautifulSoup) -- Initialized in make_soup.

    Methods:
        __init__ (None) -- initialize Miner with a writer object.
        make_soup (BeautifulSoup) -- Makes BeautifulSoup from html.

    Todo: 
        
    """

    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

    def __init__(self, data_path):
        """Initialize Miner.

        Arguments:
            data_path (str) -- Relative or absolute path to exported data.
        """
        self._data_path = data_path
        if os.path.exists(data_path):
            raise OverwriteError("A file at {} already exists!".format(data_path))
        self.writer = open(data_path, 'wb')


    def make_soup(self, path):
        '''
        Make BeautifulSoup object from html on disk.

        :param path: path to tsv document.
        :return: BeautifulSoup object
        '''
        if not os.path.exists(path):
            raise AttributeError('path parameter must point to an existing directory.')
        with open(path, 'rb') as f:
            html = f.read().decode('UTF-8')
        html = ''.join(line.strip() for line in html.split('\n'))
        html = html.replace(u'\xa0', ' ')  # A troublesome UTF-8 character

        self.soup = BeautifulSoup(html, 'html.parser')
        return self.soup
