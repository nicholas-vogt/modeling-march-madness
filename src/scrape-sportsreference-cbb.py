#!/usr/bin/python
# In Unix, an executable file that's meant to be interpreted can indicate 
# what interpreter to use by having a #! at the start of the first line, 
# followed by the interpreter (and any flags it may need).
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script

# Gamesheet scraper for college basketball data on sports-reference.com

from copy import deepcopy  
import datetime
import os.path as ospath
import requests

from bs4 import BeautifulSoup

from definitions import ROOT_URL
from Scraper import Scraper


def make_dated_gamesheet_url(year, month, day):
    """Make absolute path to gamesheet for a given date. 
    
    Arguments:
        year (int) -- Year of gamesheet
        month (int) -- Month of gamesheet
        day (int) -- Day of gamesheet
        
    Returns:
        str -- Absolute path to gamesheet for given date.
        
    Example:
        > make_dated_url(2017, 2, 5)
        "http://www.sports-reference.com/cbb/boxscores/index.cgi?year=2017&month=2&day=5"
    """
    return ROOT_URL + "cbb/boxscores/index.cgi?year={}&month={}&day={}".format(year, month, day)


def make_dated_filepath(year, month, day):
    """Make relative filepath to gamesheet for a given date. 
    
    Arguments:
        year (int) -- Year of gamesheet
        month (int) -- Month of gamesheet
        day (int) -- Day of gamesheet
        
    Returns:
        str -- Relative filepath to gamesheet for given date.
        
    Example:
        > make_dated_filepath(2017, 2, 5)
        "./../html/gamesheets/2017-2-5.txt"
    """
    return "./../html/gamesheets/{}-{}-{}.txt".format(year, month, day)

def get_boxscore_urls(gamesheet_url):
    """Collect boxscore urls from given gamesheet.
    
    Arguments:
        gamesheet_url (str) -- Full url to gamesheet where boxscore url are found.
       
    Returns: List of boxscore urls.
    """
    # gamesheet_url = "http://www.sports-reference.com/cbb/boxscores/index.cgi?month=02&day=03&year=2017"
    r = requests.get(gamesheet_url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # I used the SelectorGadget to learn the class "teams" corresponds to boxscores
    boxscore_tags = soup.find_all(class_='right gamelink')
    return [ROOT_URL + tag.a.get('href') for tag in boxscore_tags if tag.a]

def scrape_sports_reference():
    """Scrape gamesheets and boxscores from sports-reference.
    Specify date range with while loop. 
    
    Sample gamesheet: 
        http://www.sports-reference.com/cbb/boxscores/index.cgi?month=02&day=03&year=2017
    Sample boxscore:
        http://www.sports-reference.com/cbb/boxscores/2017-02-03-ball-state.html
    
    Box scores are linked via the "Total" text beside each game score on the gamesheets page.
    
    Todo:
        Allow for command line interface using argparse library.
    """
    scraper = Scraper(use_VPN=False, encoding='utf-8', crawl_delay=3)
    
    # Specify date range with start_date and end_date variables.
    start_date = datetime.datetime(year=2017, month=2, day=4)
    end_date = datetime.datetime.now()
    
    date = deepcopy(start_date)  # Always deepcopy containers
    one_day = datetime.timedelta(days=1)
    while start_date <= date <= end_date:
        year, month, day = date.year, date.month, date.day
        print(year, month, day)
        
        gamesheet_url = make_dated_gamesheet_url(year, month, day)
        gamesheet_filepath = make_dated_filepath(year, month, day)
        scraper.write_html(gamesheet_url, gamesheet_filepath)
        
        for boxscore_url in get_boxscore_urls(gamesheet_url):
            # Make a unique boxscore filepath for each url            
            parent, child = ospath.split(boxscore_url)
            child = child.replace('.html', '')
            boxscore_filepath = "./../html/boxscores/" + child.strip(' ') + '.txt'
            
            scraper.write_html(boxscore_url, boxscore_filepath)
        
        date += one_day

    return None

if __name__ == '__main__':
    scrape_sports_reference()
