"""
    Import from DCCD dataverse
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"


from pyDataverse.api import NativeApi, DataAccessApi, SearchApi
from pyDataverse.models import Dataverse
import json
from pathlib import Path
import xml.etree.ElementTree as ET
import requests
from requests.exceptions import RequestException
import pyDendron.dataname as dn

path = Path('./dataset/dccd')
base_url = 'https://dataverse.nl'
search_api = SearchApi(base_url)
api_token = ''
api = NativeApi(base_url, api_token)
access_api = DataAccessApi(base_url, api_token)

def get_dccd(keywords='dccd'):
    dataverse_list = []
    suffix = keywords
    data_type = 'dataverse'
    start = 0
    total = 1
    while start < total:
        query = suffix + "&start=" + str(start)
        search_results = search_api.search(query, data_type=data_type).json()
        total = search_results['data']['total_count']
        start = search_results['data']['start']
        for i, result in enumerate(search_results['data']['items']):
            identifier = result['identifier']
            name = result['name']
            #print(i, total, identifier, name)
            dataverse_list.append({'type': 'dataverse', 'id': identifier, dn.KEYCODE:  name})
            start += 1
    return dataverse_list

def get_dataverse(identifier='dccd'):
    contents = api.get_dataverse_contents(identifier).json()
    return contents['data']

def get_dataset(pid, keycode, identifier):
    contents = api.get_dataset(pid).json()
    if 'latestVersion' in contents['data']:
        for i, content in enumerate(contents['data']['latestVersion']['files']):
            #print(i, content)
            if content['restricted'] == False:
                dir = path / Path(keycode) / Path(identifier)
                destination = dir / Path(content['dataFile']['filename']) 
                if not destination.exists():
                    req = access_api.get_datafile(content['dataFile']['id'])
                    dir.mkdir(parents=True, exist_ok=True)
                    #print(f'\t download {destination}')
                    req.raise_for_status()  
                    with open(destination, 'wb') as fic:
                        fic.write(req.content)
            else :
                logger.info(f'\t restricted {content["label"]}')
            
dccds = get_dccd()
dataverses = get_dataverse(dccds[0]['id'])
keycode = 'empty'
for dataverse in dataverses:
    keycode = dataverse[dn.KEYCODE]
    #print('-'*10)
    #print(f'access to dataset of {keycode}')
    datasets = get_dataverse(dataverse['id'])
    for dataset in datasets:
        if dataset['type'] == 'dataset':
            #print(f'get file of {dataset["identifier"]} from {keycode}')
            pid = f'{dataset["protocol"]}:{dataset["authority"]}/{dataset["identifier"]}'
            get_dataset(pid, keycode, dataset["identifier"])
        
