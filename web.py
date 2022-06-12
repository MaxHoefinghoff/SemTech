import streamlit as st
from constructor import queryDB
import Queries
import pickle
import rdflib
from dataCleaning import match_facts_table, venue_table
from helper import loadG, getLeagues, getTeams, getInfoLeague, querySub, getInfoAtt

from SPARQLWrapper import SPARQLWrapper, JSON, N3


sparql = SPARQLWrapper("http://dbpedia.org/sparql")

# if st.sidebar.button('TEst'):

# players = Queries.Q4
# result = queryDB(players)
# st.sidebar.write(result)"""

countries = pickle.load(open('Data/countries.pickle', 'rb'))
leagues = pickle.load(open('Data/table.pickle', 'rb'))
other_data = "Data/rdf-dataset.ttl"



qres = getLeagues()

leaguesT = []
for row in qres:
    raw_string = row.o.toPython().split("/")[-1]
    leaguesT.append(raw_string)

leagues_set = list(set(leaguesT) & set(countries))

country = st.sidebar.selectbox('Select League', leagues_set)


teams = getTeams()
team_selection = st.sidebar.selectbox('Select Team', teams[country])

options = st.sidebar.selectbox('Options', ['Infos', 'Hotels', 'Tickets', 'Attractions'])



if options == 'Infos':

    if team_selection == 'All':

        data = pickle.load(open('Data/matches_clean.pkl', 'rb'))
        table = pickle.load(open('Data/table.pickle', 'rb'))

        for i in table:
            l = [str(n) for n in i.iloc[:, 1]]
            if any(x in teams[country] for x in l):
                st.write(i)

        url = getInfoLeague(country)

        q = "PREFIX dbo: <http://dbpedia.org/ontology/>"
        q += Queries.league_q #.translate(str.maketrans({
        #                                   "<":  r"\<",
        #                                   ">":  r"\>"})) + end + filter1


        q += url + """
         dbp:champions ?c;
         dbp:mostAppearances ?ma;
         dbp:mostSuccessfulClub ?msc;
         dbp:teams ?t;
         dbp:topGoalscorer ?tg         
         }
         """.translate(str.maketrans({"<":  r"\<",
                                           ">":  r"\>"}))


        q = q.replace("\\", "")
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult =  sparql.query().convert()
        #st.write(qresult)
        for i in qresult["results"]["bindings"]:
            #st.write("Cup: " + '**' + i["dc"]["value"] + "**")
            st.write("Top Goalscorer: " + i["tg"]["value"].split("/")[-1].replace('_', ' '))
            st.write("Most succesful club: " + '**' + i["msc"]["value"].split("/")[-1].replace('_', ' ') + "**")
            st.write("Most appearances: " + i["ma"]["value"].split("/")[-1].replace('_', ' '))
            st.write("Champions: " + '**' + i["c"]["value"].split("/")[-1].replace('_', ' ') + "**")
            st.write("Teams: " + i["t"]["value"].split("/")[-1].replace('_', ' '))

        #         dbo:foundingYear ?fy;
        #st.write("Founding Year: " + '**' + i["fy"]["value"] + "**")


    else:

        g, result = loadG()

        constrainT = "FILTER(REGEX(str(?t1), '" + team_selection + "' ,'i') || REGEX(str(?t2), '" + team_selection + "' ,'i')) } LIMIT 5"
        q = Queries.team + constrainT  #Queries.prefixes +
        #q = Queries.team
        #st.write(q)
        qres = g.query(q)
        games = []

        st.subheader('Last Results')

        for row in qres:
            st.write(f"**{row.d}**")
            st.write(f"{row.t1} vs. {row.t2} : **{row.s1}:{row.s2}**  ")
            #st.write(f" ID:  {row.s}")
            games.append(row.t1 + " - " + row.t2 + ", Date: " + row.d)
            match_id = row.s



        st.subheader('Get infos about specific games')
        st.selectbox('Last 5 Games:', games)


        with st.expander('Match statistics'):
            data = querySub(match_id, g)
            #st.write(data)
            options = set(data.keys())
            delete = ["match_ID", "ref-venue", "home_score", "away_score", "venue", "date", "year", "type"]
            options = list(options.difference(set(delete)))
            info = st.multiselect("Select Info", options)
            if st.button('Get statistics'):
                for i in info:
                    st.write(f"{str(i).replace('_', ' ').capitalize()}: {data[i]}")



        with st.expander('More stats'):
            pass


if options == 'Hotels':

    if team_selection != 'All':
        g, result = loadG()

        constrainT = "FILTER(REGEX(str(?t2), '" + team_selection + "' ,'i')) } LIMIT 5"
        q = Queries.team + constrainT
        qres = g.query(q)
        cities = []
        games = []

        st.subheader('Next 5 Away Games')

        for row in qres:
            st.write(f"**{row.d}**")
            st.write(f"{row.t1} vs. {row.t2}  ")
            # st.write(f" ID:  {row.s}")
            match_id = row.s
            cities.append(row.v) # venue_ID
            games.append(row.t1 + " - " + row.t2 + ", Date: " + row.d)
            city_name = row.t1

        away_game = st.selectbox('Next 5 Away Games:', games)

        team_ind = games.index(away_game)
        city = cities[team_ind]

        constrainT = "<" + city + ">" + " <http://example.org/venue#city> ?c}"
        q = Queries.team_city2 + constrainT
        qres2 = g.query(q)

        for row in qres2:
            city = row.c




        end = "<" + city + "> . ?hotel rdfs:label ?name .  " \
                                    "?hotel dbp:numberOfRooms ?rooms . " \
                                    "?hotel foaf:homepage ?hp . " \
                                    "?hotel dbo:address ?address "
        filter1 = "FILTER (LANG(?name) = 'en')}  LIMIT 5"
        q = Queries.hotel_q.translate(str.maketrans({
                                          "<":  r"\<",
                                          ">":  r"\>"})) + end + filter1
        if st.checkbox('Show query'):
            st.write(q)

        q = q.replace("\\", "")
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        text = "Hotels in " +  city.split("/")[-1]
        st.subheader(text)

        for i in qresult["results"]["bindings"]:
            st.write('**' + i["name"]["value"] + "**")
            st.write(i["hotel"]["value"])
            st.write("**Homepage**: " + i["hp"]["value"])
            st.write("**Address**: " + i["address"]["value"])
            st.write("")
            st.write("")


if options == "Tickets":

    g, result = loadG()

    constrainT = "FILTER(REGEX(str(?t1), '" + team_selection + "' ,'i') || REGEX(str(?t2), '" + team_selection + "' ,'i')) } LIMIT 5"
    q = Queries.team + constrainT  # Queries.prefixes +

    qres = g.query(q)
    games = []
    for row in qres:
        games.append(row.t1 + " - " + row.t2 + ", Date: " + row.d)

    #st.subheader('Last Results')

    #subheader('Get infos about specific games')
    selected = st.selectbox('Next  5 Games:', games)
    st.write("**" + selected + "**")

    if st.button('Buy tickets'):
        pass



if options == 'Attractions':

    g, result = loadG()

    constrainT = "FILTER(REGEX(str(?t2), '" + team_selection + "' ,'i')) } LIMIT 5"
    q = Queries.team + constrainT  # Queries.prefixes +

    qres = g.query(q)
    games = []
    cities = []
    city_name = []
    for row in qres:
        games.append(row.t1 + " - " + row.t2 + ", Date: " + row.d)
        cities.append(row.v)

    selected = st.selectbox('Next  5 Games:', games)

    team_ind = games.index(selected)
    city = cities[team_ind]



    constrainT = "<" + city + ">" + " <http://example.org/venue#city> ?c}"
    q = Queries.team_city2 + constrainT
    qres2 = g.query(q)

    for row in qres2:
        city = row.c

    st.write("**Attractions in " + city.split("/")[-1] + "**")



    with st.expander('Museum'):

        q = getInfoAtt("Museum", city) # city
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        for i in qresult["results"]["bindings"]:
            res = i["thing"]["value"]
            st.write(res.split("/")[-1].replace("_", " "))

    with st.expander('Parks'):

        q = getInfoAtt("Park", city) # city
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        for i in qresult["results"]["bindings"]:
            res = i["thing"]["value"]
            st.write(res.split("/")[-1].replace("_", " "))

    with st.expander('Church'):

        q = getInfoAtt("Church", city) # city
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        for i in qresult["results"]["bindings"]:
            res = i["thing"]["value"]
            st.write(res.split("/")[-1].replace("_", " "))


    with st.expander('Architectural Structure'):

        q = getInfoAtt("ArchitecturalStructure", city) # city
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        for i in qresult["results"]["bindings"]:
            res = i["thing"]["value"]
            st.write(res.split("/")[-1].replace("_", " "))

    with st.expander('Historic Building'):

        q = getInfoAtt("HistoricBuilding", city)  # city
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        for i in qresult["results"]["bindings"]:
            res = i["thing"]["value"]
            st.write(res.split("/")[-1].replace("_", " "))



    with st.expander('Event'):

        q = getInfoAtt("Event", city) # city
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        for i in qresult["results"]["bindings"]:
            res = i["thing"]["value"]
            st.write(res.split("/")[-1].replace("_", " "))

    with st.expander('Attraction'):

        q = getInfoAtt("Attraction", city) # city
        sparql.setQuery(q)

        sparql.setReturnFormat(JSON)
        qresult = sparql.query().convert()

        for i in qresult["results"]["bindings"]:
            res = i["thing"]["value"]
            st.write(res.split("/")[-1].replace("_", " "))


    pass