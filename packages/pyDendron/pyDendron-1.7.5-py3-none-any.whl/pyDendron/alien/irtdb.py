"""
    Import form IRTDB 
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"




import matplotlib.pyplot as plt
import numpy as np
import json
import requests
from requests.exceptions import RequestException

from pathlib import Path
 

def download_file(url, destination):
    try:
        req = requests.get(url)
        req.raise_for_status()  # Lève une exception si la requête a échoué
        with open(destination, 'wb') as fic:
            fic.write(req.content)
        return True
    except RequestException as e:
        logger.warning(f"Erreur lors du téléchargement de {url}: {e}")
        return False

## specify API request
api_base = "https://www.ncei.noaa.gov/access/paleo-search/study/search.json?"
req_params ="dataTypeId=18&dataPublisher=NOAA&locations=Continent>Europe"

req_str = api_base + req_params

fn_json = Path('./dataset/irtdb.json')
if not fn_json.exists():
    #print('request json')
    req = requests.get(req_str)
    data = json.loads(req.text)                 # load JSON-formatted search results
    with open(fn_json, 'w') as fic:
        json.dump(data, fic, indent=2)
else:
    #print('load json')
    with open(fn_json, dn.CORRELATION) as fic:
        data = json.load(fic)
    
#print('get study')
i = 0
for study in data['study']:
    if study["reconstruction"] == 'N':
        #print(f'{i} {study["xmlId"]} type: {study["dataType"]}, reconstruction: {study["reconstruction"]}, date: {study["earliestYearCE"]} / {study["mostRecentYearCE"]}')
        for site in study["site"]:
            keycode = site["siteName"]
            properties = site["geo"]["properties"]
            lat = (float(properties["southernmostLatitude"])+float(properties["northernmostLatitude"]))/2
            long = (float(properties["westernmostLongitude"])+float(properties["westernmostLongitude"]))/2  
            #species =  site['paleoData']['species']['speciesCode']
            #print(f'{keycode} {lat} {long}')
            for paleoData in site['paleoData']:
                for datafile in paleoData['dataFile']:
                    url = datafile["fileUrl"]
                    fn = Path('./dataset/irtdb') / Path(datafile["linkText"])
                    if not fn.exists():
                        #print(datafile["linkText"])
                        while not download_file(url, fn):
                                pass
            #print('-'*10)
            i += 1
                    

