# Modeling March Madness in Python
### A four-part series by Nick Vogt
###### Repo is updated through _Workshop 3: Model Selection_. The next workshop will be posted in early April.

Join me and [MSU Data Science](http://msudatascience.com/) in modeling march madness entirely in Python!

Learn how to scrape web pages to build your dataset and model the tournament in 4 parts:

1. Web Scraping  
2. Data Mining and Feature Engineering  
3. Choosing a Model  
4. Model Evaluation   

At the end of this project, you will have a fully function model of the NCAA Basketball Tournament. Tweak it to your own needs and desires to beat up on your friends and co-workers in a tourney pool. 

If you have any feedback or run into any problems, you can [find me on twitter](twitter.com/vogt4nick).

## Quick Start

All files are intended to be run from their directories. Running files from a different directory will create folders in its parent directory. 

To scrape all web pages, run the `scrape-sportsreference-cbb.py` file in the command line. This will take a few hours to run depending on the dates you choose to scrape. By default, it scrapes from 2017-01-01 through the current date. 

To mine all htmls, run the `GamesheetMiner.py` and `BoxscoreMiner.py` files in the command line. These don't take as long to run, but will still take about an hour depending on how many seasons you're scraping. 

Due to a family emergency in early March, I wasn't able to put as much time into the Model Selection portion of the repo as I would have liked. The `feature-engineering-and-model-selection.ipynb` file contains sample code for building a (rather poor) logit model. I understand it's not much use after the tournament has started, but I will continue to push updates on the model selection files through the month of March. 

Model evaluation is next! Look out for the next update on April 10, 2017.

## Python Version and Libraries

These workshops use Python 3.5. I'm pretty certain any Python 3 version will suffice, but update your version if you have doubts. 

We'll make heavy use of the `requests`, `BeautifulSoup`, `pandas`, and `statsmodels` libraries. The first is a Python default, but the others will need to be installed. If you don't know how to install packages, I encourage you to look online for tutorials. Others have explained this better than I could. 

# Resources

There are two main resources:

1. Jupyter Notebooks  
2. Powerpoint Presentations

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

## Legal Disclaimer

None of my communication should be understood as legal advice. I am not responsible for any liabilities incurred by users of this repo. It is your responsibility to ensure you are operating within your legal rights. As noted several times throughout the tutorials, scrape responsibly.
