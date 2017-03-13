
import os
from itertools import combinations

import pandas as pd 
import numpy as np

from PutModelData import get_gamesheets, get_game_results


def put_team_ids(ofile='./../data/Teams.csv', verbose=True):
    """Create Teams.csv file with one unique ID per team.

    Parameters:
        ofile (str) -- out file to export DataFrame. 
        verbose (bool) -- Whether to include file overwrite warning.

    Returns: pd.DataFrame
    """
    if os.path.exists(ofile):
        if verbose:
            print(ofile, "exists. File was not overwritten.")
        Teams = pd.read_csv(ofile, index_col=False)
    else:
        Teams = pd.DataFrame(pd.unique(get_game_results()['TeamName']), 
                             columns=['TeamName'])
        Teams = Teams.sort_values('TeamName')
        Teams['TeamID'] = np.arange(1000, 1000 + len(Teams['TeamName']))
        Teams.to_csv(ofile, index=False)

    return Teams


def put_all_matchups(ofile='./../data/Matchups.csv', verbose=True):
    """Create Matchups.csv file with one unique ID per team.

    Parameters:
        ofile (str) -- out file to export DataFrame. 
        verbose (bool) -- Whether to include file overwrite warning.

    Returns: pd.DataFrame
    """
    Teams = put_team_ids(verbose=False)
    if os.path.exists(ofile):
        if verbose: 
            print(ofile, "exists. File was not overwritten.")
        Matchups = pd.read_csv(ofile, index_col=False)
    else:
        Matchups = pd.DataFrame((c for c in combinations(Teams['TeamName'], 2)),
                                columns=['Team1', 'Team2'])
        Matchups = pd.merge(Matchups, Teams, left_on='Team1', right_on='TeamName').rename(columns={'TeamID': 'TeamID1'})
        del Matchups['TeamName']
        Matchups = pd.merge(Matchups, Teams, left_on='Team2', right_on='TeamName').rename(columns={'TeamID': 'TeamID2'})
        del Matchups['TeamName']

        Matchups['MatchupID'] = Matchups.apply(lambda x: '_'.join([str(x['TeamID1']), str(x['TeamID2'])]), axis=1)
        Matchups.to_csv(ofile, index=False)
    return Matchups


def put_game_ids(ofile='./../data/Games.csv', verbose=True):
    """Create Games.csv file with one unique ID per team.

    Parameters:
        ofile (str) -- out file to export DataFrame. 
        verbose (bool) -- Whether to include file overwrite warning.

    Returns: pd.DataFrame
    """
    if os.path.exists(ofile):
        if verbose: 
            print(ofile, "exists. File was not overwritten.")
        Games = pd.read_csv(ofile, index_col=False)
        Games['Date'] = pd.to_datetime(Games['Date'])
    else:
        Games = get_gamesheets()[['Date', 'WinningTeam', 'LosingTeam']]
        Games = Games.rename(columns={'WinningTeam': 'Team1', 'LosingTeam': 'Team2'})
        Games['GameID'] = np.arange(10000, len(Games['Date'])+10000)
        Team1 = Games[['Date', 'Team1', 'GameID']].rename(columns={'Team1': 'TeamName'})
        Team2 = Games[['Date', 'Team2', 'GameID']].rename(columns={'Team2': 'TeamName'})
        Games = pd.concat([Team1, Team2], axis=0)
        Games['Date'] = pd.to_datetime(Games['Date'])
        Teams = put_team_ids()
        Games = pd.merge(Games, Teams, on='TeamName')
        del Games['TeamName']
        Games.to_csv(ofile, index=False)

    return Games

if __name__ == '__main__':
    put_team_ids()
    put_game_ids()
    put_all_matchups()
