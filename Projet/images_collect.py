import requests
import shutil
import os
import sys
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON



endpoint_url = "https://query.wikidata.org/sparql"
os.chdir(os.path.basename("Projet"))

# Get countrysides
query1 = """SELECT ?paysage ?paysageLabel ?image ?pays ?paysLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?paysage wdt:P31 wd:Q107425;
    wdt:P17 ?pays; 
    wdt:P18 ?image.
}
LIMIT 60"""

query2 = """SELECT ?nourriture ?nourritureLabel ?image ?pays ?paysLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  OPTIONAL {  }
  
  ?nourriture wdt:P279 wd:Q2095;
         wdt:P18 ?image;
        wdt:P17 ?pays.
}
LIMIT 60
"""

query3 = """
SELECT ?voiture ?voitureLabel ?image ?pays ?paysLabel WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?voiture wdt:P31 wd:Q1420;
    wdt:P18 ?image;
    wdt:P17 ?pays.
}
LIMIT 60"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (
        sys.version_info[0],
        sys.version_info[1],
    )
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


array = []
results1 = get_results(endpoint_url, query1)
results2 = get_results(endpoint_url, query2)
results3 = get_results(endpoint_url, query3)

for result in results1["results"]["bindings"]:
    array.append(
        (
            "paysage",
            result["paysageLabel"]["value"],
            result["paysLabel"]["value"],
            result["image"]["value"],
        )
    )

for result in results2["results"]["bindings"]:
    array.append(
        (
            "nourriture",
            result["nourritureLabel"]["value"],
            result["paysLabel"]["value"],
            result["image"]["value"],
        )
    )

for result in results3["results"]["bindings"]:
    array.append(
        (
            "voiture",
            result["voitureLabel"]["value"],
            result["paysLabel"]["value"],
            result["image"]["value"],
        )
    )

dataframe = pd.DataFrame(array, columns=["type", "label", "pays", "image"])
dataframe = dataframe.drop_duplicates(subset="image")
dataframe = dataframe.astype(
    dtype={"type": "<U200", "label": "<U200", "pays": "<U200", "image": "<U200"}
)
dataframe = dataframe.sample(frac=1).reset_index(drop=True)

def download_image(url):
    print(url)
    headers = {"User-Agent": "Mozilla/5.0"}
    request = requests.get(url, allow_redirects=True, headers=headers, stream=True)
    if request.status_code == 200:
        os.chdir("../images_project")
        with open(os.path.basename(url), 'wb') as image:
            request.raw.decode_content = True
            shutil.copyfileobj(request.raw, image)
        os.chdir("../Projet")
    return os.path.basename(url)

dataframe.to_json("../data_project/data.json")
dataframe.image.apply(download_image) 

print("Done !")