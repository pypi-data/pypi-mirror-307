"""
    Import Syphe database in CSV format
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"




import logging
from pathlib import Path
import datetime
import pickle

import numpy as np 
import pandas as pd

from pyDendron.dataset import Dataset
from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.alien.mdb2csv import read_table

from pyDendron.tools.location import add_geocode

sylphe_col_sequences = {   
    'NumSeq': ID, #int
    'libellé': KEYCODE, #string  

    'espèce':SPECIES, #string
    #'NatureSeq' : 'object.type', #string
    #'Forme': 'object.shape', # string

    'NumGeo': SITE_CODE, #string
    #'DouteGeo' :'place.doubt', # bool

    'origine': DATE_BEGIN, #float
    'terme' : DATE_END, #float
    #'termeOptimum' : DATE_END_OPTIMUM, #float
    #'termeMaxi' : DATE_END_MAXIMUM, #float
    'DateSupose' : SYNC, # bool

    'NumTypseq' : CATEGORY, #string
    'NumSousTypSeq' : SUBCATEGORY, #string

    #'Aubier' : SAPWOOD, # bool
    'PosAubier' : SAPWOOD, #float

    'Moelle' : PITH, # bool
    'PosMoellerEstime' : PITH_ESTIMATED, #float

    'Cambium' : CAMBIUM, # bool
    #'PosCambiumEstimeMaxi' : CAMBIUM_MAXIMUM, #float
    #'PosCambiumEstimeOpti': CAMBIUM_OPTIMUM, #float
    #'typeEstimation': CAMBIUM_METHOD, #float
    'CambiumType' : CAMBIUM_SEASON, #string

    'Ecorce' : BARK, # bool

    'DateCréation': CREATION_DATE, # date ?, #string
    #'Informateur' : 'creation.owner', # string
    'NumPersonne' : PERS_ID, # string
    'Note': COMMENTS # string
    }

sylphe_col_sequences_miss = [
        DATA_LENGTH, DATA_VALUES, DATA_TYPE, DATA_WEIGHTS,
        ]

sylphe_col_components = {'NumMean' : ID_PARENT, 'NumSeq' : ID_CHILD, 'Pos' : OFFSET}
#sylphe_col_components_miss = ['keycode.child', 'path.child', ]
sylphe_col_indices = {'NumSeq' : ID, 'Longueur': 'count', 'TypeInd' : 'key', 'Val' : 'values'}
sylphe_col_indices_miss = []

class IOSylphe:
    """
    Class to import Sylphe database after conversion in CSV files with '@' as separator
    """
    file_extension = ['.mdb']

    def __init__(self, base_directory='./',get_place=False, places='location.p', reverse_places='reverse_location.p'):
        self.get_place = get_place
        self.places = {}
        self.places_fn = places
        self.reverse_places_fn = reverse_places
        self.elevations = {}
        self.base_directory = base_directory

        self.sequences = None
        self.components = None
        
    def read_sequences(self, sep : str ='@', header : int =0) :
        """
        Read cvs sequences

        Keyword Arguments:
            sep -- fields separator (default: {'@'})
            header -- head column values (default: {0})
            usecols -- columns to keep (default: 
            rename_columns -- how to rename columns 
        Returns:
            a Pandas DataFrame and a list sequences with trouble
        """

        def _places():
            def load(name):
                if (name is not None) and Path(name).exists():
                    with open(name , 'rb') as fic:
                        dic = pickle.load(fic)
                else:
                    dic = {}
                return dic
            def load2(name):
                if (name is not None) and Path(name).exists():
                    with open(name , 'rb') as fic:
                        dic = pickle.load(fic)
                else:
                    dic = [{}, {}]
                return dic
            places = load(self.places_fn)
            reverse_places, elevation = load2(self.reverse_places_fn)
            
            places, reverse_places, elevation = add_geocode(sequences, places, reverse_places, elevation)
            with open(self.places_fn , 'wb') as fic:
                pickle.dump(places, fic)
                
            with open(self.reverse_places_fn , 'wb') as fic:
                pickle.dump([reverse_places, elevation], fic)

        def _gregorian():
            # set gregorian date to astronomique gregorian date
            for key in [DATE_BEGIN, DATE_END]: #, DATE_END_OPTIMUM, DATE_END_MAXIMUM]:
                sequences[key] = sequences[key].astype('Int32')
                sequences.replace({key : {0: pd.NA}}, inplace=True) 
                sequences.loc[sequences[key] < 0, key] += 1

        def _type():
            for key in [SAPWOOD]: 
                sequences[key] = sequences[key].apply(lambda x: pd.NA if (x > 159394000) or (x == 0) or (x == 65535) else x)
                sequences[key] = sequences[key].astype('Int32')
                sequences.loc[sequences[key] > 0, key] -= 1

            for key in [BARK, CAMBIUM, PITH]:
                sequences[key] = sequences[key] > 0
                sequences[key] = sequences[key].astype(bool)


        #filename = Path(self.path) / Path(self.sequences_filename)
        #sequences = pd.read_csv(filename, sep=sep, header=header, usecols=sylphe_col_sequences.keys())
        sequences = read_table(self.mdb_file, 'Sequence', converters_from_schema=False, usecols=sylphe_col_sequences.keys()) 
        
        
        sequences.rename(columns=sylphe_col_sequences, inplace=True)
        sequences = sequences[sylphe_col_sequences.values()]

        for col in sylphe_col_sequences_miss:
            sequences[col] = None

        sequences.replace({CATEGORY: {'MEAN': MEAN, 'SET': SET, 'SEQ': MEASURE}}, inplace=True)

        _gregorian()
        _type()
        if self.get_place: _places()
        
        self.sequences = sequences.set_index(ID)
        
        self._check_sequences()
        
        return self.sequences

    def _string(self, dataframe, key):
        dataframe[key] = dataframe[key].astype('string')

    def _check_sequences(self):
        # Check lastYear and firstYear consistency
        year = datetime.datetime.now().year
        date1 = self.sequences.loc[(self.sequences[DATE_END] - self.sequences[DATE_BEGIN]) < 0].index.tolist()
        date2 = self.sequences.loc[(self.sequences[DATE_END] > year) | 
                                (self.sequences[DATE_BEGIN] > year)].index.tolist()

        trouble = list()
        if date1 is not None:
            trouble = date1
        if date2 is not None:
            trouble += date2
        if len(trouble) > 0:
            for id in trouble:
                row = self.sequences.loc[id]
                logger.warning(f'inconsistent dates, to ckeck: {id} {row[KEYCODE]} (begin: {row[DATE_BEGIN]}, end:{row[DATE_END]})')

        return trouble

    def read_indices(self,sep='@', header=0):
        """Read CSV Indices

        Keyword Arguments:
            sep -- fields separator (default: {'@'})
            header -- head column values (default: {0})
        Returns:
            a indices object and a list sequences with trouble
        """
        def count_nan_in_vector(vector):
            if vector is None:
                return 0
            return np.isnan(vector).sum()
        
        def _read_values():
            values = []
            weights = []
            tmp = row['values'].replace(',', '.')
            tmp = tmp.replace('\\r\\n', '')
            for line in tmp.split(';')[:-1]:
                try :
                    s = line.split()
                    x = s[1]
                    w = s[3]
                    x = np.nan if x == 'ABS' else float(x)
                    x = np.nan if (x == 999) or (x == 9999) else x
                except ValueError:
                    x = np.nan
                    w = 0
                    logger.warning(f'error in values {id} {self.sequences.loc[id, KEYCODE]} | {line}')
                weights.append(w)
                values.append(x)
            
            if len(values) == 0:
                return pd.NA, 0, pd.NA
            
            return np.array(values), len(values), np.array(weights)
        
        def _check_dates(length):
            keycode, begin, end = self.sequences.loc[id, [KEYCODE, DATE_BEGIN, DATE_END]]
            c = row['count']
            s = f'end-begin dates != values length for: {id} {keycode} : len != (DateEnd - DateBegin + 1)  {length} {c} != ( {end} - {begin} + 1 = {end - begin + 1})',  
            if not pd.isna(end) and not pd.isna(begin) and length != (end - begin + 1):
                trouble.append([id, length, begin, end])
                logger.warning(s)

        # -------
        #fn = Path(self.path) / Path(self.indices_filename)
        #indices = pd.read_csv(fn, sep=sep, header=header, usecols=sylphe_col_indices.keys())
        indices = read_table(self.mdb_file, 'Indice', converters_from_schema=False, usecols=sylphe_col_indices.keys()) 

        indices.rename(columns=sylphe_col_indices, inplace=True)

        # Get raw indices
        indices = indices.loc[(indices['key'] == 'NAT') & (indices[ID].isin(self.sequences.index)), :]
        
        trouble = []
        to_drop = []
        for id, df in indices.groupby(ID): 
            row = df.iloc[0]
            values, length, weights = _read_values()
            self.sequences.at[id, DATA_VALUES] = values
            self.sequences.at[id, DATA_LENGTH] = length
            self.sequences.at[id, DATA_TYPE] = RAW

            if self.sequences.at[id, CATEGORY] == MEAN:
                self.sequences.at[id, DATA_WEIGHTS] = weights
            _check_dates(length)

            if (length == count_nan_in_vector(values)):
                if self.sequences.at[id, CATEGORY] == MEASURE:
                    to_drop.append(id)
                else:
                    self.sequences.at[id, DATA_VALUES] = pd.NA
                    self.sequences.at[id, DATA_LENGTH] = 0
                    self.sequences.at[id, CATEGORY] = SET
                    self.sequences.at[id, DATA_WEIGHTS] = pd.NA
        
        if len(to_drop) > 0:
            logger.warning(f'Drop empty or full NaN {DATA_VALUES} for samples:  {to_drop}')
            self.sequences.drop(to_drop, inplace=True)
        
        for k, t in sequences_dtype_dict.items():
            if k not in self.sequences.columns:
                self.sequences[k] = ''
            if t == 'string':
                self.sequences[k] = self.sequences[k].fillna('')
        
        self.sequences[SPECIES] = self.sequences[SPECIES].str.upper()
        mask = self.sequences[SPECIES].str.startswith('QU')
        self.sequences.loc[mask, SPECIES] = 'QU'
        
        self.sequences[SUBCATEGORY] = self.sequences[SUBCATEGORY].str.upper()
        self.sequences[COMMENTS] = self.sequences[COMMENTS].str.replace(r'\n', '.')
        self.sequences[COMMENTS] = self.sequences[COMMENTS].str.replace(r'\r', '')
        self.sequences[INCONSISTENT] = False
        
    def read_components(self, sep='@', header=0):
        """_summary_

        Keyword Arguments:
            sep -- fields separator (default: {'@'})
            header -- head column values (default: {0})
        Returns:
            a Pandas DataFrame and 3 lists with trouble
        """

        # ----------
        #filename = Path(self.path) / Path(self.components_filename)
        #components = pd.read_csv(filename, sep=sep, header=header, usecols=sylphe_col_components.keys())
        components = read_table(self.mdb_file, 'Composant', converters_from_schema=False, usecols=sylphe_col_components.keys()) 

        components.rename(columns=sylphe_col_components, inplace=True)

        self._add_missing_components_col(components)
        key = OFFSET
        components[key] = components[key].apply(lambda x: pd.NA if (x > 159394000) or (x == 0) or (x == 65535) else x)
        components[key] = components[key].astype('Int32')
        components.loc[components[key] > 0, key] -= 1
        
        components_parents = self._id_parent_is_in_sequences(components)
        self._id_child_is_in_sequences(components, components_parents)
        
        components = self._check_components(components)

        self.components = components
        return self.components

    def _add_missing_components_col(self, components):
        pass
        #for col in sylphe_col_components_miss:
        #    components[col] = None

    def _id_parent_is_in_sequences(self, components):
        owner_before = set(components[ID_PARENT].to_list())
        components_parents = components.loc[components[ID_PARENT].isin(self.sequences.index)]
        owner_after = set(components[ID_PARENT].to_list())
        owner_removed = owner_before - owner_after
        if len(owner_removed) > 0:
            logger.warning(f'remove components without sequence:  {owner_removed}')
        return components_parents
        
    def _id_child_is_in_sequences(self, components, components_parents):
        id_before = set(components[ID_CHILD].to_list())
        components = components_parents.loc[components[ID_CHILD].isin(self.sequences.index)]
        id_after = set(components[ID_CHILD].to_list())
        id_removed = id_before - id_after

        if len(id_removed) > 0:
            logger.warning(f'remove components without sequence:  {id_removed}')
            
    def _check_components(self, components):
        components_with_date_begin = components.merge(self.sequences[DATE_BEGIN], left_on=ID_CHILD, right_on=ID)
        
        for id_parent, data in components_with_date_begin.groupby(ID_PARENT):
            min_date = data[DATE_BEGIN].min()
            min_pos = data[OFFSET].min()
            if pd.isna(min_date) or pd.isna(min_pos):
                components_with_date_begin.loc[components_with_date_begin[ID_PARENT] == id_parent, DATE_BEGIN] = 0
                components_with_date_begin.loc[components_with_date_begin[ID_PARENT] == id_parent, OFFSET] = 0
            else:
                components_with_date_begin.loc[components_with_date_begin[ID_PARENT] == id_parent, DATE_BEGIN] -= min_date
                components_with_date_begin.loc[components_with_date_begin[ID_PARENT] == id_parent, OFFSET] -= min_pos
        
        mask = (components_with_date_begin[OFFSET] != components_with_date_begin[DATE_BEGIN])
        components_with_date_begin.loc[mask, OFFSET] = components_with_date_begin.loc[mask, DATE_BEGIN]
        return components_with_date_begin.drop(DATE_BEGIN, axis=1)
    
    def set_project(self):
        components = self.dataset.components
        leaf = self.dataset.get_leafs()
        for id in leaf:
            filter = components.index.get_level_values(ID_CHILD) == id
            if np.sum(filter) == 1:
                id_parent = components[filter].index.get_level_values(ID_PARENT).to_list()[0]
                self.dataset.sequences.at[id, PROJECT] = self.dataset.sequences.at[id_parent, KEYCODE]
        
    def to_dataset(self, keycode_parent='Dataset',root_id=ROOT, trash_keycode='Trash', clipboard_keycode='Clipboard', workshop_keycode='Workshop' ):
        logger.info('read sequences')
        self.read_sequences()
        logger.info('read indices')
        self.read_indices()
        logger.info('read components')
        self.read_components()
        #print(self.sequences)
        self.dataset = Dataset(self.sequences, self.components, save_auto=False)
        self.set_project()
        
        logger.info(f'to_dataset roots: {self.dataset.get_roots()}')
        
        self.dataset.new_root(keycode_parent, root_id)
        self.dataset.new_clipboard(clipboard_keycode)
        self.dataset.new_trash(trash_keycode)
        self.dataset.new_workshop(workshop_keycode)
        
        return self.dataset

    def read(self, ndb_file, keycode_parent='Sylphe'):
        self.mdb_file = Path(ndb_file)

        return self.to_dataset(keycode_parent=keycode_parent)
    
    def read_buffer(self, keycode_parent, buffer, mine_type=None):
        
        output_file = Path(self.base_directory) / Path(keycode_parent).with_suffix(self.file_extension[0])
        with open(output_file, 'wb') as f:
            f.write(buffer)  # Récupère le contenu binaire du buffer
        
        
        dataset = self.read(output_file, keycode_parent=keycode_parent) 
        output_file.unlink()
        return dataset             
