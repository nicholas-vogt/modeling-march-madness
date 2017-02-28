# Modeling March Madness in Python
### A four-part series by Nick Vogt
###### Repo is updated through _Workshop 1: Webscraping_. The next workshop will be posted by February 20, 2017.

Join [me](http://nicholas-vogt.github.io/home) and [MSU Data Science](http://msudatascience.com/) in modeling march madness entirely in Python!

Learn how to scrape web pages to build your dataset and model the tournament in 4 parts:

1. Web Scraping  
2. Data Mining and Feature Engineering  
3. Choosing a Model  
4. Model Evaluation  

At the end of this project, you will have a fully function model of the NCAA Basketball Tournament. Tweak it to your own needs and desires to beat up on your friends and co-workers in a tourney pool. 

## Quick Start

All files are intended to be run from their directories. Running files from a different directory will create folders in its parent directory. 

To scrape all web pages, run the `scrape-sportsreference-cbb.py` file in the command line. This will take a few hours to run depending on the dates you choose to scrape.

To mine all htmls, run the `GamesheetMiner.py` and `BoxscoreMiner.py` files in the command line. These don't take as long to run, but will still take about an hour depending on how many seasons you're scraping. 

Selection Sunday is almost here! The model selection and model evaluation files will be posted next. 

## Python Version and Libraries

These workshops use Python 3.5. I'm pretty certain any Python 3 version will suffice, but update your version if you have doubts. 

We'll make heavy use of the `requests` and `BeautifulSoup` libraries. The former is a Python default, but the latter will need to be installed. If you don't know how, [read the docs](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup). Others have explained this better than I could, so if the docs leave you confused, a google search should be sufficient to help you install it.

Of course, we'll use other libraries, but I've specifically left these workshops to focus on Python built-ins. 

# Resources

There are three main resources:

1. Jupyter Notebooks  
2. Powerpoint Presentations
3. Youtube Videos (forthcoming)

### Jupyter Notebooks and Powerpoint Presentations

There are powerpoint (.pptx) and jupyter notebook (.ipynb) files which complement each other. They are titled similarly, such that `web-scraping.pptx` corresponds to `web-scraping.ipynb`. Powerpoints can be found in the root directory for easy access. All notebooks and python files are found in the src folder. 

```
Directory Map
    - modeling-march-madness -- root directory.  
    |-/data -- stores clean data files.  
    |-/data-raw -- stores raw data files.  
    |-/html -- stores raw htmls in .txt files.  
    |-/src -- stores all python source files.  
```

The `src` files wil create the remaining directories in the root directory when python are run. 

### Youtube Videos

The workshops will be posted on the MSU Data Science [youtube channel](https://www.youtube.com/channel/UC6QjLVucAiw_XelTrPnAu1g) and  delivered at Michigan State Univeristy throughout the Spring. 

If you live near East Lansing, MI and want to attend the workshops, keep an eye on the MSU Data Science [website](http://msudatascience.com/) or [facebook page](https://www.facebook.com/MSUDataScience/) for event updates. Attendance is free for everyone.

### Python Files

All Python files can be found in the `src` subdirectory.

```
/src
    Scripts:
        Scraper.py -- Contains the main Scraper class.
        scrape-sports-reference.py -- Scrapes all cbb gamesheets and boxscores from sports-reference.com

    Notebooks:
        web-scraping.ipynb -- Corresponding notebook to the `web-scraping.pptx` file.
```
## Legal Disclaimer

None of my communication should be understood as legal advice. I am not responsible for any liabilities incurred by users of this repo. It is your responsibility to ensure you are operating within your legal rights. As noted several times throughout the tutorials, scrape responsibly.
