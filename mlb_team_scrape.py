#mlb web scrape for historical team data
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import numpy as np

#function to scrape website with URL param
#returns parsed html
def get_soup(URL):
    #enable chrome options
    options = Options()
    options.add_argument('--headless=new')  

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    #get page source
    html = driver.page_source
    #close driver for webpage
    driver.quit
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_stats(soup):
    stats_table = soup.find('div', attr={"class":"stats-body-table team"})
    #get column headers from mlb table
    headers = soup.findAll('div', class_='bui-text cellheader bui-text')
    return headers

#url for each team standings, add year at the end of url string to get particular year
standings_url = 'https://www.mlb.com/standings/'

#url for season hitting stats for all teams, add year at end of url for particular year
hitting_stats_url = 'https://www.mlb.com/stats/team'

#url for season pitching stats for all teams, add year at end of url for particular year
pitching_stats_url = 'https://www.mlb.com/stats/team/pitching'

#get parsed data from each url
soup_hitting = get_soup(hitting_stats_url)
#soup_pitching = get_soup(pitching_stats_url)
#soup_standings = get_soup(standings_url)

#get data from 
team_hit_stats = get_stats(soup_hitting)
print(team_hit_stats)
