import sqlite3
import pandas as pd
import pickle
from dataCleaning import team_t, match_table, match_facts_table, venue_table, league_table_new

#data = pickle.load(open('matches_clean.pkl', 'rb'))

conn = sqlite3.connect('database')
c = conn.cursor()



match_table.to_sql('match', conn, if_exists='replace', index = False, dtype={'match_ID': 'INTEGER PRIMARY KEY NOT NULL', })


team_t.to_sql('team', conn, if_exists='replace', index = False, dtype={'index': 'INTEGER PRIMARY KEY NOT NULL'})


match_facts_table.to_sql('match_facts', conn, if_exists='replace', index = False, dtype={'match_ID': 'INTEGER PRIMARY KEY NOT NULL'})

venue_table.to_sql('venue', conn, if_exists='replace', index = False, dtype={'venue_id': 'INTEGER PRIMARY KEY NOT NULL'})

league_table_new.to_sql('league', conn, if_exists='replace', index = False, dtype={'league_id': 'INTEGER PRIMARY KEY NOT NULL'})








