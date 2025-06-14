#mlb web scrape for historical team data
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import re




#function to scrape website with URL param
#returns parsed html
def get_soup(URL):
    #enable chrome options
    options = Options()
    options.add_argument('--headless=new')  

    driver = webdriver.Chrome(options=options)
    driver.get(URL)
    
    #get page source
    html = driver.execute_script("return document.documentElement.outerHTML;")
    #close driver for webpage
    driver.implicitly_wait(3)
    #stats_table = driver.find_element(By.CSS_SELECTOR, "bui-table")
    #print(stats_table)

    driver.quit
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_hitting_stats(URL, year):
    #get parsed data from each url
    #soup_hitting = get_soup(URL+)

    #parse tables off url, returns list of dictionaries (list of tables from url)
    df_hitting_list = pd.read_html(URL+year)

    #create dataframe from 1st list in df_hitting_list
    hitting_df = df_hitting_list[0]

    #update column names to remove dupe (EX: TEAMTEAM)
    headers_list = []
    for col in hitting_df.columns:
        mid = len(col)//2
        col2 = col[:mid]
        if col2 == 'caret-upcaret-downHR':
            col2 = 'HR'
        headers_list.append(col2)

    #remove numbers from team name in 1st column and remove dupe team name from every col0 on every row 
    # (ex: New York YankeesYankees -> New York Yankees)
    for index, name in hitting_df.iterrows():
        hitting_df.iloc[index, 0] = re.sub(r'\d+', '', hitting_df.iloc[index,0])
        team_name = " ".join(re.split(r'(?=[A-Z])', hitting_df.iloc[index, 0])[:-1])
        #team_name = ' '.join(team_name.split()[:-1]
        hitting_df.iloc[index, 0] = team_name
    print(hitting_df)

    #output to xlsx
    hitting_df.to_excel('Team Hitting Stats.xlsx', sheet_name=year)


def get_pitching_stats(URL, year):
    #parse html table
    pitching_list_df = pd.read_html(URL+year)
    #print(pitching_list_df)

    pitching_df = pitching_list_df[0]
    #print(pitching_df)

    #remove numbers from team name in 1st column and remove dupe team name from every col0 on every row 
    # (ex: New York YankeesYankees -> New York Yankees)
    for index, name in pitching_df.iterrows():
        pitching_df.iloc[index, 0] = re.sub(r'\d+', '', pitching_df.iloc[index,0])
        team_name = " ".join(re.split(r'(?=[A-Z])', pitching_df.iloc[index, 0])[:-1])
        #team_name = ' '.join(team_name.split()[:-1]
        pitching_df.iloc[index, 0] = team_name
    #print(pitching_df)

    headers_list = []
    for col in pitching_df.columns:
        mid = len(col)//2
        col2 = col[:mid]
        if col2 == 'caret-upcaret-downSO':
            col2 = 'SO'
        headers_list.append(col2)
    
    #print(headers_list)
    pitching_df.columns = headers_list
    #print(pitching_df.columns)

    print(pitching_df)

    #output to xlsx
    pitching_df.to_excel('Team Pitching Stats.xlsx', sheet_name='2025')


def get_standings(URL, year):
    #parse html table
    standings_list_df = pd.read_html(URL+year)
    print(standings_list_df)



#main function
def main():

    #url for each team standings, add year at the end of url string to get particular year
    standings_url = 'https://www.mlb.com/standings/' 
    #url for season hitting stats for all teams, add year at end of url for particular year
    hitting_stats_url = 'https://www.mlb.com/stats/team/'
    #url for season pitching stats for all teams, add year at end of url for particular year
    pitching_stats_url = 'https://www.mlb.com/stats/team/pitching/'

    #call functions to scrape and create dataframes for each URL
    get_hitting_stats(hitting_stats_url, '2025')
    get_pitching_stats(pitching_stats_url, '2025')
    #get_standings(standings_url, '2025')




if __name__ == '__main__':
    main()
