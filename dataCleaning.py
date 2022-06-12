import pandas as pd
import pickle

"""data = pd.read_csv('matches.csv')

data = data.iloc[:, 1:34]
pickle.dump(data, open('matches_clean.pkl', 'wb'))
test = pickle.load(open('matches_clean.pkl', 'rb'))"""

delete = ["time (utc)", "league", "part_of_competition", "game_status", "shootout", "home_goal_minutes", "away_goal_minutes"]

data = pickle.load(open('Data/matches_clean.pkl', 'rb'))

data = data[data.year > 2018]
league_t = data

data = data.drop(delete, axis=1)

#pickle.dump(data, open('matches_clean.pkl', 'wb'))
#test = pickle.load(open('matches_clean.pkl', 'rb'))

team_t_columns = ["home"]

team_t = list(set(data[team_t_columns].home))
team_table = pd.DataFrame()
team_table["team"] = team_t


team_t = team_table.reset_index(level=0)
#team_t["team_id"] = team_t["index"]

convert = team_t.set_index("team").to_dict()["index"]



#game_t = ["home_id", "away_id", "date", "year", "attendance", "venue", ]

game_t = data
match_table = game_t
match_table = match_table.replace({"away": convert}).replace({"home": convert})
match_table.rename(columns={'home': 'home_id', 'away': "away_id"}, inplace=True)

#leagues_pre = league_t.league.map(lambda x: x.split(' ')[1:]).map(lambda x: ' '.join(x))




match_table_new = match_table[['home_id', 'away_id']].reset_index()
del match_table_new['index']
match_table_new = match_table_new.reset_index().rename(columns={"index" : "match_ID"})
match_facts_table = match_table.iloc[:, 2:].reset_index().rename(columns={"index" : "match_ID"})
match_facts_table['match_ID'] = match_table_new["match_ID"]

match_table = match_table_new
#


#match_table["match"] = match_table["match_ID"]
#match_facts_table['match'] = match_table_new["match_ID"]
#### venue to multiple columns

venue_table = pd.DataFrame()
venue_table["venue"] = match_facts_table['venue']
venue_table[['venue', 'city', 'country']] = venue_table['venue'].str.split(',', expand=True).iloc[:, :-1]

venue_table["city"] = venue_table["city"].str.lstrip()
venue_table["country"] = venue_table["country"].str.lstrip()
venue_table["venue_id"] = match_table.loc[: , "home_id"]

match_facts_table["venue"] = match_table.loc[:, "home_id"]


cols = venue_table.columns.tolist()
cols = cols[-1:] + cols[:-1]
venue_table = venue_table[cols]
venue_table = venue_table.drop_duplicates()
venue_table = venue_table[venue_table["venue"].notna()].drop_duplicates(subset=['venue_id'], keep="last")

match_table["match_stats"] = match_facts_table["match_ID"]


league_table = league_t.league.map(lambda x: x.split(' ')[1:])#
leagues_pre = league_table.map(lambda x: ' '.join(x))

league_table = list(set(leagues_pre))

convertLeague = {k: v for v, k in enumerate(league_table)}


match_table["league_id"] = leagues_pre.values
#match_table = match_table.replace({"league_id": convertLeague})

#


league_table.remove('Season')
#league_table.remove('Barclays Premier League')
#league_table.remove('French Ligue 1')
#league_table.remove('German Bundesliga')
#league_table.remove("Spanish Primera División")



league_table_new = pd.DataFrame()
league_table_new['league_names'] = league_table
country_names = ["France", "Italy", "Netherlands", "Germany", "Spain", "England"]
league_table_new["country_names"] = country_names
URIS = ["<http://dbpedia.org/resource/Ligue_1>",
        "<http://dbpedia.org/resource/Italian_Serie_A>",
        "<http://dbpedia.org/resource/Dutch_Eredivisie>",
        "<http://dbpedia.org/resource/German_Bundesliga>",
        "<http://dbpedia.org/resource/LaLiga>",
        "<http://dbpedia.org/resource/Premier_League>"]

league_table_new["URL"] = URIS
league_table_new["league_name"] = league_table_new["league_names"]
#league_table_new = league_table_new.replace({"league_names": convertLeague})
league_table_new.rename(columns = {'league_names':'league_id'}, inplace = True)
convertNew = league_table_new.reset_index().set_index("league_id").to_dict()["index"]
pickle.dump(league_table_new, open('Data/table_new.pickle', 'wb'))
#{key:convertNew[str(key)] for key in convertNew}
convertNew["Season"] = 6

match_table = match_table.replace({"league_id": convertNew})
league_table_new = league_table_new.replace({"league_id": convertNew})




"""test = pickle.load(open('table.pickle', 'rb'))
del test[4]
del test[4]
del test[7]
del test[7]
del test[17]
del test[17]

pickle.dump(test, open('table.pickle', 'wb'))"""

"""names = pickle.load( open('countries.pickle', 'rb'))
print(len(names))
names.remove('San Marino')
print(len(names))
pickle.dump(names, open('countries.pickle', 'wb'))

"""

