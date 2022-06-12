import requests
from bs4 import BeautifulSoup
import pickle
import pandas as pd

def get_page():
    # get the response in the form of html
    wikiurl = "https://en.wikipedia.org/wiki/List_of_top-division_football_clubs_in_UEFA_countries"
    #table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    soup = BeautifulSoup(response.text, 'html.parser')
    indiatable = soup.find_all('table', {'class': "wikitable"})
    countries = soup.find_all('span', {'class': "mw-headline"})
    names = []
    for el in countries:
        names.append(el.get_text())
    names = names[3:-3]
    leagues = []
    for i in indiatable:
        df = pd.read_html(str(i))
        # convert list to dataframe
        df = pd.DataFrame(df[0])
        leagues.append(df)
    return names, leagues


names, leagues = get_page()

pickle.dump(names, open('countries.pickle', 'wb'))
pickle.dump(leagues, open('table.pickle', 'wb'))