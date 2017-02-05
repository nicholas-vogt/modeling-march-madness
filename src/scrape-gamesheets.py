#!/usr/bin/python
# In Unix, an executable file that's meant to be interpreted can indicate 
# what interpreter to use by having a #! at the start of the first line, 
# followed by the interpreter (and any flags it may need).
# http://stackoverflow.com/questions/2429511/why-do-people-write-usr-bin-env-python-on-the-first-line-of-a-python-script

# Gamesheet scraper for college basketball data on sports-reference.com

from copy import deepcopy
import datetime

from Scraper import Scraper

ROOT_URL = "http://www.sports-reference.com/"

def make_dated_url(year, month, day):
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


def main():
    """Scrape gamesheets and boxscores from sports-reference.
    Specify date range with while loop. 
    
    Todo:
        Allow for command line interface using argparse library.
    """
    scraper = Scraper(crawl_delay=3)
    # Specify date range with start_date and end_date variables.
    start_date = datetime.datetime(year=2017, month=2, day=1)
    end_date = datetime.datetime.now()
    
    date = deepcopy(start_date)
    one_day = datetime.timedelta(days=1)
    while start_date <= date <= end_date:
        year, month, day = date.year, date.month, date.day
        gamesheet_url = make_dated_url(year, month, day)
        filepath = make_dated_filepath(year, month, day)
        scraper.write_html(gamesheet_url, filepath)
        date += one_day

    return None

if __name__ == '__main__':
    main()
