from SPARQLWrapper import SPARQLWrapper, JSON, get_sparql_dataframe
from Queries import QI, Q3, Q4
import pandas as pd
import sparql_dataframe


dbpsparql = SPARQLWrapper("http://dbpedia.org/sparql")

def queryDB(query):

    dbpsparql.setQuery(query)
    # The result is in JSON
    dbpsparql.setReturnFormat(JSON)
    result = dbpsparql.query().convert()
    vars = (result["head"]["vars"])
    data = result["results"]["bindings"]
    all = []
    for i in data:
        set1 = []
        for var in vars:
            var1 = i[var]
            set1.append(var1["value"])
        all.append(set1)
    result = pd.DataFrame(all).set_axis(vars, axis=1)
    #print(data)
    #result = pd.DataFrame(result["results"])


    return result

