import os
import csv
import re

from bs4 import BeautifulSoup

class Miner:
    '''
    The Miner class manages everything related to mining HTMLs.
    This is the skeleton which every subsequent Miner class will inherit.
    '''

    days = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')

    def __init__(self, csv_path='data/gamesheet.txt'):
        """
        Initialize GamesheetMiner
        :param csv_path: path to export data
        """
        self._csv = csv_path

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

    def header(self):
        """
        :return: a tab-separated value header line.
        """
        return '\t'.join([k for k, v in self.__dict__.items() if k is not "soup"]) + '\n'

    def row(self):
        '''
        :return: tab-separated variable row
        '''
        values = [', '.join(v) if isinstance(v, list) else v for k, v in self.__dict__.items() if k is not "soup"]
        return '\t'.join(values) + '\n'

    def write_txt(self):
        '''
        This write function is SLOW. Think of a better solution.
        :return: None
        '''
        self._clean()
        parent = os.path.split(self._csv)[0]
        if not os.path.exists(parent):
            os.makedirs(parent)
        if not os.path.exists(self._csv):
            header_row = '\t'.join(
                ("Path", "EventID", "Period", "Time",
                 "Home", "Away", "Offense", "CumScore",
                 "Type", "ScoredBy", "Assists",
                 "OffenseOnIce", "DefenseOnIce")
            ) + "\n"
            with open(self._csv, 'wb') as csv:
                csv.write(header_row.encode('UTF-8'))

        attrs = '\t'.join(
                (self.path, self.event_ID, self.period, self.time,
                 self.home, self.away, self.offense, self.cum_score,
                 self.type, self.scored_by, self.assists,
                 self.offense_on_ice, self.defense_on_ice)
        ) + '\n'
        with open(self._csv, 'ab') as csv:
            csv.write(attrs.encode('UTF-8'))

    def write_csv(self):
        '''
        DO NOT USE THIS FUNCTION BEFORE YOU FIX IT.
        Uses the csv library.
        Like the other write function, this is SLOW. Think of a better solution.
        :return: None
        '''
        self._clean()
        parent = os.path.split(self._csv)[0]
        if not os.path.exists(parent):
            os.makedirs(parent)
        if not os.path.exists(self._csv):
            header = sorted([k for k, v in self.__dict__.items()])
            header_row = '\t'.join(header) + '\n'
            with open(self._csv, 'w', newline='\n') as csv_file:
                writer = csv.writer(csv_file, delimiter='\t',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(header_row)

        attrs = [(k, str(v)) for k, v in self.__dict__.items()]
        attrs = sorted(attrs, key=lambda sort_on: sort_on[0])
        attrs = [v for k, v in attrs]
        # row = '\t'.join(attrs) + '\n'

        with open(self._csv, 'a') as csv_file:
            writer = csv.writer(csv_file, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(attrs)




if __name__ == '__main__':
    miner = GamesheetMiner("data/test-gamesheet.txt")
    for root, dirs, files in os.walk('html'):
        text_files = [f for f in files if f.endswith('.txt') and not f.startswith('2017')]
        for tf in text_files:
            print('\tmining {}...'.format(tf))
            file_path = os.path.join(root, tf)

            miner.load_gamesheet(file_path)
            miner.mine_gamesheet()
            miner.write_txt()
