
import os
from itertools import combinations

import pandas as pd 
import numpy as np

from PutModelData import get_game_results


def put_team_ids(ofile='./../data/Teams.csv', verbose=True):
    """Create Teams.csv file with one unique ID per team.

    Parameters:
        ofile (str) -- out file to export DataFrame. 
        verbose (bool) -- Whether to include file overwrite warning.

    Returns: pd.DataFrame
    """
    Teams = pd.unique(get_game_results()['TeamName'])
    # Teams = pd.DataFrame({"TeamName": ["MSU", 'Michigan', 'Ohio State']})
    Teams['TeamID'] = np.arange(1000, 1000 + len(Teams['TeamName']))
    if not os.path.exists(ofile):
        Teams.to_csv(ofile)
    elif verbose:
        print(ofile, "exists. File was not overwritten.")
    return Teams


def put_all_matchups(ofile='./../data/Matchups.csv', verbose=True):
    """Create Teams.csv file with one unique ID per team.

    Parameters:
        ofile (str) -- out file to export DataFrame. 
        verbose (bool) -- Whether to include file overwrite warning.

    Returns: pd.DataFrame
    """
    Teams = put_team_ids(verbose=False)
    Matchups = pd.DataFrame((c for c in combinations(Teams['TeamName'], 2)),
                            columns=['Team1', 'Team2'])
    Matchups = pd.merge(Matchups, Teams, left_on='Team1', right_on='TeamName').rename(columns={'TeamID': 'TeamID1'})
    del Matchups['TeamName']
    Matchups = pd.merge(Matchups, Teams, left_on='Team2', right_on='TeamName').rename(columns={'TeamID': 'TeamID2'})
    del Matchups['TeamName']

    Matchups['MatchupID'] = Matchups.apply(lambda x: '_'.join([str(x['TeamID1']), str(x['TeamID2'])]), axis=1)

    if not os.path.exists(ofile):
        Matchups.to_csv(ofile)
    elif verbose:
        print(ofile, "exists. File was not overwritten.")
    return Matchups


if __name__ == '__main__':
    put_team_ids()
    put_all_matchups()
