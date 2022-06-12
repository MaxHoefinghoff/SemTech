import Queries
import streamlit as st
import rdflib

@st.experimental_singleton
def loadG():
    g = rdflib.Graph()
    print('loaded')
    result = g.parse('Data/rdf-dataset.ttl', format='turtle')
    return g, result


def getLeagues():
    q = Queries.leagues  # + constrainT  #Queries.prefixes +
    g, result = loadG()
    qres = g.query(q)
    return qres


@st.cache
def getTeams():
    q = Queries.team_name
    g, result = loadG()
    qres = g.query(q)
    teams = dict()

    for row in qres:
        country = row.c.toPython().split("/")[-1]
        team = row.t.toPython()
        if country not in teams:
            teams[country] = list()
            teams[country].append('All')
        if team not in teams[country]:
            teams[country].append(team)

    return teams


def getInfoLeague(country):
    constrainT = "FILTER(REGEX(str(?cn), '" + country + "' ,'i')) }"
    q = Queries.leaguesI  + constrainT
    g, result = loadG()

    qres = g.query(q)
    for row in qres:
        pass
        #st.write(row.cn, row.ln, row.uri)
        # st.write(row.ln, row.cn)

    return row.uri.toPython()


def querySub(match_id, g):
    subject = rdflib.term.URIRef(str(match_id).replace("match", "match_facts", 1))
    # st.write(subject)
    subGraph = rdflib.Graph()
    subGraph += g.triples((subject, None, None))
    data = {}
    for s, p, o in subGraph:
        p = str(p).split("#")[-1]
        # st.write(f"{p}: {o}")
        data[p] = str(o).replace(":", ", ")

    return data



def getInfoAtt(type, city):
    ext1 = "dbo:" + type
    ext2 = " FILTER(REGEX(str(?city), '" + city + "' ,'i')) } LIMIT 10"

    q = Queries.info + ext1 + ext2
    q = q.translate(str.maketrans({
        "<": r"\<",
        ">": r"\>"}))

    q = q.replace("\\", "")

    print('HERE' + q)

    return q