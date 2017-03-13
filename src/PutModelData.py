import pandas as pd

# from PutMatchups import put_season_matchups


def get_game_results(csv='./../data/gamesheets-2017.txt'):
    """Get Gamesheet Data
    """
    # Clean Gamesheet Data
    Gamesheets = pd.read_csv(csv, sep='\t', index_col=False)
    Gamesheets['Date'] = pd.to_datetime(Gamesheets['Date'])
    Gamesheets['ScoreDiff'] = Gamesheets['WinningScore'] - Gamesheets['LosingScore']

    Winners = Gamesheets[['Date', 'WinningTeam', 'WinningScore', 'ScoreDiff']]
    Winners.columns = ('Date', 'TeamName', 'Score', 'ScoreDiff')
    Losers = Gamesheets[['Date', 'LosingTeam', 'LosingScore', 'ScoreDiff']]
    Losers.columns = ('Date', 'TeamName', 'Score', 'ScoreDiff')
    Losers['ScoreDiff'] = Losers.apply(lambda x: -x['ScoreDiff'], axis=1)
    GameResults = pd.concat([Winners, Losers], axis=0)
    
    # Teams = pd.read_csv("./../data/Teams.csv")
    # Teams.columns = ('TeamID', 'TeamName')
    # GameResults = pd.merge(GameResults, Teams, how='left', on='TeamName')
    
    # GameResults = GameResults[['Date', 'TeamID', 'TeamName', 'Score', 'ScoreDiff']]
    GameResults = GameResults[['Date', 'TeamName', 'Score', 'ScoreDiff']]
    GameResults['Win'] = GameResults['ScoreDiff'] > 0
    GameResults['Win'].astype(int)
    GameResults.sort_values(by=['Date', 'TeamName'])
    
    return GameResults

def get_boxscores(csv='./../data/boxscores-2017.txt'):
    Boxscores = pd.read_csv(csv, sep='\t', index_col=False)
    Boxscores['Date'] = pd.to_datetime(Boxscores['Date'])
    Boxscores = Boxscores.rename(columns={'Team': 'TeamName'})
    # Boxscores = Boxscores.set_index(['Date', 'TeamName']).groupby(level=[0,1]).sum()
    return Boxscores

def get_season_game_stats():
    Boxscores = get_boxscores().sort_values(['Date', 'TeamName'])
    GameResults = get_game_results().sort_values(['Date', 'TeamName'])

    # Calculate Individual Game Stats
    variables = [c for c in Boxscores.columns if c not in ('Player', 'IsStarter', 'TeamID')]
    SeasonGameStats = Boxscores[variables].groupby(by=['Date','TeamName']).sum()
    SeasonGameStats.reset_index(inplace=True)  # Removes multi-index from previous operation
    SeasonGameStats['NumOT'] = SeasonGameStats.apply(lambda x: (x['MP'] - 200) // 25, axis=1)
    SeasonGameStats = pd.merge(SeasonGameStats, GameResults, on=['Date', 'TeamName'])
    return SeasonGameStats

def get_season_cum_stats():
    SeasonGameStats = get_season_game_stats()
    SeasonCumStats = SeasonGameStats.set_index(['Date', 'TeamName']).groupby(level=1).cumsum().reset_index()
    SeasonCumStats.columns = ['Cum'+c if c not in ('Date', 'TeamName') else c for c in SeasonCumStats.columns]
    SeasonCumStats['Cum2Ppct'] = SeasonCumStats['Cum2P'] / SeasonCumStats['Cum2PA']
    SeasonCumStats['Cum3Ppct'] = SeasonCumStats['Cum3P'] / SeasonCumStats['Cum3PA']
    SeasonCumStats['CumFTpct'] = SeasonCumStats['CumFT'] / SeasonCumStats['CumFTA']
    del SeasonCumStats['CumTeamID']
    return SeasonCumStats

def get_season_stats():
    SeasonStats = get_season_game_stats()
    SeasonStats.set_index(['Date', 'TeamName']).groupby(level=1).sum()
    return SeasonStats

def put_logit_data(ofile='./../data/model-data-logit.csv'):
    """Create logit data csv file.
    
    Parameters:
        ofile (str) -- File where data will be exported.
    
    Returns: pandas.DataFrame
    """
    SeasonGameStats = get_season_game_stats()
    SeasonCumStats = get_season_cum_stats()
    LogitData = pd.merge(SeasonGameStats, SeasonCumStats, on=['Date', 'TeamName'])

    LogitData = LogitData[[c for c in LogitData.columns if c !='CumTeamID']]
    SeasonMatchups = put_season_matchups()
    df = pd.merge(SeasonMatchups, LogitData, on=['Date', 'TeamName'], copy=True)
    
    LogitData.columns = ['Opp'+c if c not in ('Date', 'TeamName') else c for c in LogitData.columns]
    df = pd.merge(df, LogitData, left_on=['Date','Opponent'], right_on=['Date','TeamName'])
    del df['TeamName_y']
    df = df.rename(columns={'TeamName_x': 'TeamName'})
    df = df.sort_values(['Date', 'TeamName'])
    df.to_csv('./../data/model-data-logit.csv', index=False)

    return df
    
if __name__ == "__main__":
    put_model_data()
    put_logit_data()