"""
This script can be run from the command line to scrape all gamesheets from 
the /html directory. Data will be exported in tab-separated variable format 
to a .txt file named feb-gamesheets.txt in the /data directory.
"""

import os

from bs4 import BeautifulSoup

from Miner import Miner

class GamesheetMiner(Miner):
    """Mines data from daily gamesheets on 
    http://www.sports-reference.com/cbb/boxscores/

    Attributes:
        COLNAMES (tuple (str)) -- Column names to be exported with data.

    Methods:
        __init__ (None) -- Initialize class with path for exported data.
        mine_boxscore (List) -- Mine game data. Returns data in nested List.
        write (None) -- Write game data to txt file on disc.

    Todo:
        Pool multiprocessors to speed up the Miner.
    """

    COLNAMES = ("Date", "WinningTeam", "WinningScore", "LosingTeam", "LosingScore")

    def __init__(self, data_path):
        """Initialize GamesheetMiner.

        Arguments:
            data_path (str) -- Relative or absolute path to exported data.
        """
        Miner.__init__(self, data_path)
        header = '\t'.join(self.COLNAMES) + '\n'
        self.writer.write(header.encode('utf-8'))


    def mine_gamesheet(self, path):
        """Mine gamesheet specified at path.

        Arguments:
            path -- Relative or absolute path to boxscore.

        Returns: Nested list of data.
        """
        self.soup = self.make_soup(path)
        date = os.path.split(path)[-1].replace('.txt', '')

        self.game_data = []

        game_summaries = self.soup.find(class_="game_summaries") \
                                  .find_all('div', {"class":'game_summary nohover'})
        self.game_data = []
        for game in game_summaries:
            team_data = game.find(class_='winner')
            if not team_data:  # sometimes returns a NoneType
                continue
            winning_team = team_data.a.text.strip()
            winning_score = team_data.find(class_='right').text.strip()

            team_data = game.find(class_='loser')
            losing_team = team_data.a.text.strip()
            losing_score = team_data.find(class_='right').text.strip()
            self.game_data.append([date, 
                                   winning_team, winning_score, 
                                   losing_team, losing_score])

        return self.game_data


    def write(self, sep='\t'):
        """Write collected data to tab.

        Arguments:
            sep (str) -- separator used in data export.

        Returns: None
        """
        for game in self.game_data:
            game.append('\n')
            self.writer.write(sep.join(game).encode())


if __name__ == '__main__':
    miner = GamesheetMiner("./../data/feb-gamesheets.txt")
    gamesheet_dir = "./../html/gamesheets/"
    for root, dirs, files in os.walk(gamesheet_dir):
        for f in files:
            if f.endswith('txt'):
                print("Mining", f)
                miner.mine_gamesheet(os.path.join(gamesheet_dir, f))
                miner.write()
