"""
Location tools
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"


import re
from pathlib import Path
import requests
import numpy as np
import pandas as pd
import time

from pathlib import Path

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *

departements = {
    '01': 'Ain',
    '02': 'Aisne',
    '03': 'Allier',
    '04': 'Alpes-de-Haute-Provence',
    '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes',
    '07': 'Ardèche',
    '08': 'Ardennes',
    '09': 'Ariège',
    '10': 'Aube',
    '11': 'Aude',
    '12': 'Aveyron',
    '13': 'Bouches-du-Rhône',
    '14': 'Calvados',
    '15': 'Cantal',
    '16': 'Charente',
    '17': 'Charente-Maritime',
    '18': 'Cher',
    '19': 'Corrèze',
    '21': 'Côte-d\'Or',
    '22': 'Côtes-d\'Armor',
    '23': 'Creuse',
    '24': 'Dordogne',
    '25': 'Doubs',
    '26': 'Drôme',
    '27': 'Eure',
    '28': 'Eure-et-Loir',
    '29': 'Finistère',
    '2A': 'Corse-du-Sud',
    '2B': 'Haute-Corse',
    '30': 'Gard',
    '31': 'Haute-Garonne',
    '32': 'Gers',
    '33': 'Gironde',
    '34': 'Hérault',
    '35': 'Ille-et-Vilaine',
    '36': 'Indre',
    '37': 'Indre-et-Loire',
    '38': 'Isère',
    '39': 'Jura',
    '40': 'Landes',
    '41': 'Loir-et-Cher',
    '42': 'Loire',
    '43': 'Haute-Loire',
    '44': 'Loire-Atlantique',
    '45': 'Loiret',
    '46': 'Lot',
    '47': 'Lot-et-Garonne',
    '48': 'Lozère',
    '49': 'Maine-et-Loire',
    '50': 'Manche',
    '51': 'Marne',
    '52': 'Haute-Marne',
    '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle',
    '55': 'Meuse',
    '56': 'Morbihan',
    '57': 'Moselle',
    '58': 'Nièvre',
    '59': 'Nord',
    '60': 'Oise',
    '61': 'Orne',
    '62': 'Pas-de-Calais',
    '63': 'Puy-de-Dôme',
    '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées',
    '66': 'Pyrénées-Orientales',
    '67': 'Bas-Rhin',
    '68': 'Haut-Rhin',
    '69': 'Rhône',
    '70': 'Haute-Saône',
    '71': 'Saône-et-Loire',
    '72': 'Sarthe',
    '73': 'Savoie',
    '74': 'Haute-Savoie',
    '75': 'Paris',
    '76': 'Seine-Maritime',
    '77': 'Seine-et-Marne',
    '78': 'Yvelines',
    '79': 'Deux-Sèvres',
    '80': 'Somme',
    '81': 'Tarn',
    '82': 'Tarn-et-Garonne',
    '83': 'Var',
    '84': 'Vaucluse',
    '85': 'Vendée',
    '86': 'Vienne',
    '87': 'Haute-Vienne',
    '88': 'Vosges',
    '89': 'Yonne',
    '90': 'Territoire de Belfort',
    '91': 'Essonne',
    '92': 'Hauts-de-Seine',
    '93': 'Seine-Saint-Denis',
    '94': 'Val-de-Marne',
    '95': 'Val-d\'Oise',
    '971': 'Guadeloupe',
    '972': 'Martinique',
    '973': 'Guyane',
    '974': 'La Réunion',
    '976': 'Mayotte'
}

def request_get(base_url, params, timeout=100, rep=5):
    #print('request_get')
    response = None
    try:
        for i in range(rep):
            response = requests.get(base_url, params=params, timeout=timeout)
            
            #logger.debug(f'info {i}, {base_url}, {params}, {response}')
            if response.status_code == 200 :
                return response
            time.sleep(i)
        
    except Exception as inst:
        logger.error(f'request_get : {inst}', exc_info=True)
    finally:
        return response    

def reverse_geocode(lat, lon, reverse_places=None):
    """Query address 

    Arguments:
        lat -- lattitude
        lon -- longitude

    Returns:
        the striucture address
    """
    
    empty = '', '', '', '', '', ''
    #print('place:', lat, lon)
    
    if (reverse_places is not None) and ((lat, lon) in reverse_places):
        #print('find in places')
        return reverse_places[lat, lon]

    if np.isnan(float(lat)) or np.isnan(float(lon)):
        return empty

    #print('reverse_geocode:', lat, lon)
    if (abs(float(lat)) > 90) or (abs(float(lon)) > 180):
        return empty

    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lon': str(lon),
        'lat': str(lat),
        'format': 'json'
    }

    country = ''
    state = ''
    county = ''
    zip_code = ''
    town = ''
    site = ''
    response = request_get(base_url, params=params)
    if response is not None:
        if response.status_code == 200 :
            data = response.json()
            if 'address' in data:
                address = data['address']
                #print(address)
                if 'municipality' in address:
                    town = address['municipality']
                elif 'village' in address:
                    town = address['village']
                elif 'suburb' in address:
                    town = address['suburb']
                elif 'borough' in address:
                    town = address['borough']
                if ('postcode' in address) and ('country_code' in address):
                    zip_code = address['country_code']+'-'+address['postcode']
                if 'county' in address:
                    county = address['county']
                elif 'city' in address:
                    county = address['city']
                if 'country' in address:
                    country = address['country']
                if 'state' in address:
                    state = address['state']
                site = f'{town}, {county}, {state}, {country}'
                #print(site)
        else:
            logger.warning(f'query error lat:{lat} lon:{lon} {response.status_code} {response.text}')
        
        if reverse_places is not None:
            #print(reverse_places)
            #print((lat, lon))
            #print((country, state, county, town, zip_code, site))
            reverse_places[(float(lat), float(lon))] = (country, state, county, town, zip_code, site)
        
    return country, state, county, town, zip_code, site

def geocode(name):

    params = {
        'q': name,  
        'format': 'json', 
        'limit': 1  
    }

    base_url = 'https://nominatim.openstreetmap.org/search'
    response = request_get(base_url, params=params)
    if (response is not None) and (response.status_code == 200):
        data = response.json()
        if data:
            result = data[0]  
            return result.get('lat'), result.get('lon')
    return np.nan, np.nan

def get_elevation(lat, long, elevations=None):
    
    if (elevations is not None) and ((lat, long) in elevations):
        return elevations[(lat, long)]
    if np.isnan(float(lat)) or np.isnan(float(long)):
        return np.nan
    
    if (abs(float(lat)) > 90) or (abs(float(long)) > 180):
        return np.nan

    query = f'https://api.open-meteo.com/v1/elevation?latitude={lat}&longitude={long}'
    response = request_get(query, None)
    if (response is not None) and (response.status_code == 200):
        data = response.json()
        elevation = data['elevation'][0]
        if elevations is not None: 
            elevations[(lat, long)] = elevation
        return float(elevation)
    
    return np.nan

def fullgeocode(name, model=r'^(.*?)\s*\((\d{2,3})\)$', country='France', reverse_places=None, elevation=None):
    empty = (np.nan, np.nan, np.nan, '', '', '', '', '', '')
    name_save = name
    if pd.isna(name):
        return empty
    
    res = re.match(model, name)
    if res:
        town = res.group(1)
        if res.groups == 2 and dep in departements:
            dep = res.group(2)
            name = f'{town}, {departements[dep]}, '    
        else:
            name = ''
            for i in range(len(res.groups())):
                name += res.group(i)+', '
        if country != '':
            name += country

    logger.info(f'localisation code: {name} extrat from {name_save} using regex {model}.')   
    lat, lon = geocode(name)
    if lat is np.nan :
       return empty
    else:
        country, state, district, town, zip_code, site = reverse_geocode(lat, lon, reverse_places)
        alt = get_elevation(lat, lon, elevations=elevation)
    return (lat, lon, alt, country, state, district, town, zip_code, site)

def add_geocode(sequences, saved_places, reverse_places=None, elevation=None):
    places_lst = []
    
    places = saved_places
    for place in sequences[SITE_CODE]:
        if place not in places:         
            #print("get location for ", place, 'on web')  
            data = fullgeocode(place, reverse_places=reverse_places, elevation=elevation)
            places[place] = data
            places_lst.append(data)
        else:
            places_lst.append(places[place])

    df = pd.DataFrame(places_lst, columns=[SITE_LATITUDE, SITE_LONGITUDE, SITE_ELEVATION, SITE_COUNTRY, SITE_STATE, SITE_DISTRICT, SITE_TOWN, SITE_ZIP, SITE_CODE])

    sequences[SITE_CODE] = df[SITE_CODE]
    sequences[SITE_LATITUDE] = df[SITE_LATITUDE]
    sequences[SITE_LONGITUDE] = df[SITE_LONGITUDE]
    sequences[SITE_ELEVATION] = df[SITE_ELEVATION]
    
    return places, reverse_places, elevation

    