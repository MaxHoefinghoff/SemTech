QI = """
PREFIX s: <http://schema.org/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?country 
WHERE 
{
?country a s:Property .
?country dbo:currentSeason dbr:Bundesliga.
} 
"""

Q2 = """
PREFIX s: <http://schema.org/>
PREFIX dbp: <http://dbpedia.org/property/>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT ?year
WHERE 
{
?year a s:Property .
dbr:Bundesliga dbo:foundingYear ?year.
} 
"""

Q2 = """
select distinct ?property ?label {
  { dbr:Bundesliga ?property ?o }
  union
  { ?s ?property dbr:Bundesliga }

  optional { 
    ?property rdfs:label ?label .
    filter langMatches(lang(?label), 'en')
  }
}
"""

Q3 = """
select ?year {
  { dbr:Bundesliga dbo:foundingYear ?year. }
}
"""

Q3 = """
select ?year 
{ dbr:Bundesliga dbo:wikiPageWikiLink ?year.
?year a dbo:SportsClub. 
}

"""

Q4 = """
SELECT * WHERE {
  ?player a <http://dbpedia.org/ontology/SoccerPlayer> .
  ?player <http://dbpedia.org/ontology/birthDate> ?birthDate .
  ?player <http://dbpedia.org/ontology/Person/height> ?height .
  ?player <http://dbpedia.org/ontology/position> ?position .
  ?player <http://dbpedia.org/ontology/team> ?team .
}
"""


main = """
SELECT * WHERE {
  ?player a <http://dbpedia.org/ontology/SoccerPlayer> .
  ?player   rdfs:label ?PlayerName .
  FILTER(langMatches(lang(?PlayerName),"en"))
  ?player <http://dbpedia.org/ontology/birthDate> ?birthDate .
  ?player <http://dbpedia.org/ontology/Person/height> ?height .
  ?player <http://dbpedia.org/ontology/position> ?position .
  ?player <http://dbpedia.org/ontology/team> ?team .
  ?team   rdfs:label ?name .
  FILTER(langMatches(lang(?name),"en")) .
  ?team dbo:league ?league .
   ?league rdfs:label ?leagueName .
  FILTER(langMatches(lang(?leagueName),"en")) .
}"""

test = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT * WHERE {
  ?sub ?pred ?obj .
} LIMIT 10"""


####################################################################

prefixes = """
PREFIX facts: <http://example.org/match_facts#>
PREFIX match: <http://example.org/match#>
PREFIX abc: <http://example.org/> """


queryG = """
SELECT * WHERE {
  ?sub ?pred ?obj .
} LIMIT 10"""

queryG1 = """
SELECT * WHERE {
?obj a match:match_ID .
  ?sub ?pred ?obj .
} LIMIT 10"""

queryG1 = """
SELECT ?sub ?obj2 ?obj  WHERE {
{
?sub <http://example.org/match_facts#away_offsides> ?obj .
}
  union
{ 
?sub <http://example.org/match#match_ID> ?obj2
}
} LIMIT 10"""

queryG2 = """
SELECT ?s ?o  WHERE {
?s <http://example.org/match#home_id> ?o.
?sub <http://example.org/match_facts/home_saves> ?obj
LIMIT 10 }"""


queryG1 = """
PREFIX num:<http://example.org/team/index=>
SELECT ?s ?o ?o2 ?t1 WHERE {
{
?s <http://example.org/match#home_id> ?o.
?o <http://example.org/team#team> num?t1
}
  union
{ 
?s <http://example.org/match#away_id> ?o2.

}
} LIMIT 10"""


#PREFIX num:<http://example.org/team/index=>
teams_stats = """
SELECT ?h ?a ?o ?t1 ?t2 WHERE {
?s a <http://example.org/match> .
?s <http://example.org/match_facts#home_goal_scorers> ?o .
?s <http://example.org/match#home_id> ?h .
?s <http://example.org/match#away_id> ?a .
?tn1 <http://example.org/team#team_id> ?h . 
?tn2 <http://example.org/team#team_id> ?a .
?tn1 <http://example.org/team#team> ?t1 . 
?tn2 <http://example.org/team#team> ?t2 .
} LIMIT 10"""

leagues = """
SELECT DISTINCT ?o WHERE {
?s a <http://example.org/venue> .
?s <http://example.org/venue#country> ?o .
} LIMIT 10"""


leaguesI = """
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?cn ?ln ?uri WHERE {
?l a <http://example.org/league> .
?l <http://example.org/league#country_names> ?cn .
?l <http://example.org/league#league_name> ?ln .
?l <http://example.org/league#URL> ?uri 
"""
#?uri dbo:currentSeason ?cs

#?


queryG2 = """
SELECT ?s ?o WHERE {
{
?s a <http://example.org/match> .
?s <http://example.org/match_facts#away_wonCorners> ?o
}
  union
{ 
?s <http://example.org/match#away_id> ?o2.

}
} LIMIT 10"""


city = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?h ?a ?o ?city ?t1 ?t2 WHERE {
?s a <http://example.org/match> .
?s <http://example.org/match_facts#venue> ?o .
?o  <http://example.org/venue#venue> ?city .
?s <http://example.org/match#home_id> ?h .
?s <http://example.org/match#away_id> ?a .
?tn1 <http://example.org/team#team_id> ?h . 
?tn2 <http://example.org/team#team_id> ?a .
?tn1 <http://example.org/team#team> ?t1 . 
?tn2 <http://example.org/team#team> ?t2 .
} LIMIT 10"""


team = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?t1 ?t2 ?d WHERE {
?s a <http://example.org/match> .
?s <http://example.org/match#ref-home_id> ?h .
?s <http://example.org/match#ref-away_id> ?a .
?h <http://example.org/team#team> ?t1 . 
?a <http://example.org/team#team> ?t2 . 
?s <http://example.org/match#ref-match_stats> ?st .
?st <http://example.org/match_facts#date> ?d .
"""


team = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?t1 ?t2 ?d ?s ?s1 ?s2 ?v WHERE {
?s a <http://example.org/match> .
?s <http://example.org/match#ref-home_id> ?h .
?s <http://example.org/match#ref-away_id> ?a .
?h <http://example.org/team#team> ?t1 . 
?a <http://example.org/team#team> ?t2 . 
?s <http://example.org/match#ref-match_stats> ?st .
?st <http://example.org/match_facts#date> ?d .
?st <http://example.org/match_facts#home_score> ?s1 .
?st <http://example.org/match_facts#away_score> ?s2 .
?st <http://example.org/match_facts#ref-venue> ?v .
"""

matchSubG = """
SELECT * WHERE {
{num} a <http://example.org/match> .
"""


team_name = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?t ?c WHERE {
?s a <http://example.org/match> .
?s <http://example.org/match#ref-home_id> ?h .
?h <http://example.org/team#team> ?t . 
?s <http://example.org/match#ref-match_stats> ?m .
?m  <http://example.org/match_facts#ref-venue> ?v .
?v  <http://example.org/venue#country> ?c . }
"""


team_id = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?t1 ?t2 ?s WHERE {
?s a <http://example.org/match> .
?s <http://example.org/match#ref-home_id> ?h .
?s <http://example.org/match#ref-away_id> ?a .
?h <http://example.org/team#team> ?t1 . 
?a <http://example.org/team#team> ?t2 . 
"""



team_city = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?t ?c WHERE {
?s a <http://example.org/match> .
?s <http://example.org/match#ref-home_id> ?h .
?h <http://example.org/team#team> ?t . 
?s <http://example.org/match#ref-match_stats> ?m .
?v  <http://example.org/venue#city> ?c . 
?m  <http://example.org/match_facts#ref-venue> 
"""

team_city2 = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?c WHERE { """



city_hotel = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>
SELECT ?c WHERE {
?c a dbo:City
} LIMIT 5
"""

hotel_q = """
PREFIX dbo: <http://dbpedia.org/ontology/>
SELECT ?name ?hotel ?address ?rooms ?hp
WHERE {
?hotel a dbo:Hotel .
?hotel <http://dbpedia.org/ontology/location> 
"""

#?s <http://example.org/match#away_id> ?a .
#?s <http://example.org/match_facts#date> ?d .


league_q = """
SELECT ?ma ?c ?t ?msc ?tg 
WHERE {
"""

league_q2 = """
SELECT ?fy
WHERE {
"""

info = """
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbr: <http://dbpedia.org/resource/>

SELECT  ?thing
WHERE {
?city a dbo:City .
?thing dbo:location ?city .
?thing a 
"""

