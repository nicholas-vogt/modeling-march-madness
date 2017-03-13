"""
This script can be run from the command line to scrape all boxscores from 
the /html directory. Data will be exported in tab-separated variable format 
to a .txt file named feb-boxscores.txt in the /data directory.
"""

import os

from bs4 import BeautifulSoup

from Miner import Miner

class BoxscoreMiner(Miner):
    """BoxscoreMiner Class for mining boxscores.

    Attributes:
        COLNAMES -- Column names for the exported data.

    Methods:
        __init__ (None) -- Initialize class with path for exported data.
        mine_boxscore (List) -- Mine player data. Returns data in nested List.
        write (None) -- Write player data to txt file on disc.

    Todo:
        Pool multiprocessors to speed up the Miner.
    """

    """
    MP -- Minutes Played
    FG -- Field Goals
    FGA -- Field Goal Attempts
    FGpct -- Field Goal Percentage
    2P -- 2 Point Field Goals
    2PA -- 2 Point Field Goal Attempts
    2Ppct -- 2 Point Field Goal Percentage
    3P -- 3 Point Field Goals
    3PA -- 3 Point Field Goal Attempts
    3Ppct -- 3 Point Field Goal Percentage
    FT -- Free Throw Points
    FTA -- Free Throw Attempts
    FTpct -- Free Throw Percentage
    ORB -- Offensive Rebounds
    DRB -- Defensive Rebounds
    TRB -- Total Rebounds
    AST -- Assists
    STL -- Steals
    BLK -- Blocks
    TOV -- Turnovers
    PF -- Personal Fouls
    PTS -- Total Points
    """
    COLNAMES = ("Date", "Team", "Player", "IsStarter", "MP", 
                "FG", "FGA", "FGpct", 
                "2P", "2PA", "2Ppct", 
                "3P", "3PA", "3Ppct",
                "FT", "FTA", "FTpct",
                "ORB", "DRB", "TRB", 
                "AST", "STL", "BLK", 
                "TOV", "PF",  "PTS")

    def __init__(self, data_path):
        """Initialize BoxscoreMiner.

        Arguments:
            data_path (str) -- Relative or absolute path to exported data.
        """
        Miner.__init__(self, data_path)
        header = '\t'.join(self.COLNAMES) + '\n'
        self.writer.write(header.encode('utf-8'))


    def mine_boxscore(self, path):
        """Mine boxscore specified at path.

        Arguments:
            path -- Relative or absolute path to boxscore.

        Returns: Nested list of data. 
        """
        self.make_soup(path)
        date = os.path.split(path)[-1][:10]
        away_team, home_team = get_team_names(self.soup)
        tables = self.soup.find_all('tbody')
        
        home_tbl = tables[-2]
        home_players = [[date, home_team] + stats for stats in get_stats_from_table(home_tbl)]
        
        away_tbl = tables[-1]
        away_players = [[date, away_team] + stats for stats in get_stats_from_table(away_tbl)]
        
        self.game_data = home_players + away_players
        return self.game_data


    def write(self, sep='\t'):
        """Write collected data to tab.

        Arguments:
            sep (str) -- separator used in data export.

        Returns: None
        """
        for player in self.game_data:
            player.append('\n')
            self.writer.write(sep.join(player).encode())


def get_stats_from_table(table):
    """A generator which returns stats from table.

    Yields: Row of player data.
    """
    for i, row in enumerate(table.find_all('tr')):
        player_stats = [col.text for col in row.find_all('td')]
        if player_stats:
            player_name = row.find('th').text
            is_starter = "Starter" if i < 5 else "Reserve"
            player_stats.insert(0, player_name)
            player_stats.insert(1, is_starter)

            yield player_stats

def get_team_names(soup):
    """Get team names from soup.

    Returns: Tuple with away team and home team names. 

    Examples:
        > string = "Sam Houston State vs. Abilene Christian Box Score, February 4, 2017"
        > get_team_names(string)
        ("Sam Houston State", "Abilene Christian")
    """
    h1 = soup.h1.text
    teams, date = h1.split('Box Score,')
    away, home = teams.split(' vs. ')
    away = away.strip()
    home = home.strip()
    return (away, home)


if __name__ == '__main__':
    miner = BoxscoreMiner("./../data/boxscores-2017.txt")
    boxscore_dir = "./../html/boxscores/"
    for root, dirs, files in os.walk(boxscore_dir):
        for f in files:
            if f.endswith('txt'):
                print("Mining", f)
                try:
                    miner.mine_boxscore(os.path.join(boxscore_dir, f))
                    miner.write()
                except ValueError as err:
                    print(err)
