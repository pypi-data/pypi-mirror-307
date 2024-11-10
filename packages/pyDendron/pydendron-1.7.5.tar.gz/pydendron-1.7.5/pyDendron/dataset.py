"""
Dataset class
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

from typing import List, Tuple, Union
import warnings
import os
import copy
import pickle
import json
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import numpy as np
import panel as pn
import param

from collections import Counter

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.componentsTree import ComponentsNode, ComponentsTree
from pyDendron.mean import compute_mean, compute_means
from pyDendron.crossdating import CrossDating
from pyDendron.detrend import detrend, slope
from pyDendron.estimation import cambium_estimation

class Dataset(param.Parameterized):
    """
    Data storage of sequences and components. Includes also selections of pairs.
    """
    VERSION = 11
    
    notify_message = param.String(default='', doc='log change in the dataset') 
    notify_reload = param.Event()
    notify_synchronize = param.Event()
    notify_packages = param.Event()
    notification_source = param.ClassSelector(default=None, class_=object)
    #counter = param.Integer(3, doc='Node added in tree')
    save_auto =  param.Boolean(False, doc='show all components / sequences')
            
    version_control = True
    
    def __init__(self, sequences=None, components=None, username='None', cfg_tmp='./', **params):
        super(Dataset, self).__init__(**params)   
        self.username = username        
        self.filename = None
        self.cfg_tmp = cfg_tmp
        
        if (components is not None) and (sequences is not None):
            self.sequences = pd.DataFrame(sequences)
            self.components = pd.DataFrame(components)
            self.update()
        else:
            self.clean()   
        self._packages = {}
        self._freeze_components = None
        self._freeze_sequences = None
        self._log = []
        self._crossdating = pd.DataFrame()
    
    def get_log(self):
            """
            Returns the log data as a pandas DataFrame.

            Returns:
                pandas.DataFrame: The log data.
            """
            #perror('get_log', self._log)
            return pd.DataFrame(self._log, columns=log_dtype.keys())
    
    def get_sequences_copy(self, ids):
        """
        Returns a copy of the sequences at the specified indices.

        Parameters:
            ids (list): A list of indices specifying the sequences to be copied.

        Returns:
            pandas.DataFrame: A copy of the sequences at the specified indices.
        """
        data = self.sequences.loc[ids,:].copy()
        return data

    def get_components_copy(self, id_pairs):
        """
        Returns a copy of the components DataFrame based on the given index pairs.

        Parameters:
            id_pairs (list): A list of index pairs specifying the rows to be copied.

        Returns:
            pandas.DataFrame: A copy of the components DataFrame containing the specified rows.
        """
        data = self.components.loc[id_pairs,:].copy()
        return data
        
    def freeze_sequences(self, ids):
        """
        Freezes the sequences at the specified indices.

        Args:
            ids (list): A list of indices indicating the sequences to freeze.

        Returns:
            None
        """
        #perror('freeze_sequences', ids)
        self._freeze_sequences = self.get_sequences_copy(ids)

    def freeze_components(self, id_pairs):
        """
        Freezes the components specified by the given index pairs.

        Args:
            id_pairs (list): A list of index pairs specifying the components to freeze.

        Returns:
            None
        """
        self._freeze_components = self.get_components_copy(id_pairs)

    def log_components(self, id_pairs, comments=''):
        """
        Compare the components specified by the given index pairs.

        Args:
            id_pairs (list): A list of index pairs specifying the components to compare.

        Returns:
            None

        Raises:
            None
        """
        new_df = self.get_components_copy(id_pairs)
        old_df = self._freeze_components
        log = []
        
        merge = old_df.join(new_df, lsuffix='_old', rsuffix='_new')
        for ids, row in merge.iterrows():
            (id_child, id_parent) = ids
            old, new = row[OFFSET+'_old'], row[OFFSET+'_new']
            if pd.isna(old) or pd.isna(new) or (old != new):
                log.append([datetime.now(), id_child, id_parent ,OFFSET, old, new, self.username, comments])
        
        self._freeze_components = None
        if len(log) > 0:
            self._log += log
            #self.notify_changes(comments)
            return True
        #print('no change in components')
        return False
        
    def log_sequences(self, ids, comments=''):
        """
        Compare sequences between the old and new dataframes.

        Args:
            ids (list): List of indices to compare.
            comments (str, optional): Additional comments for the comparison. Defaults to ''.

        Returns:
            dict: A dictionary containing the history of changes made in the sequences.
                The dictionary keys are tuples of (index, column, date), and the values are lists
                containing the old value, new value, user, and comments.

        Raises:
            KeyError: If the two dataframes are not aligned.

        """
        def compare(id, old_row, new_row):
            log = []
            #d = new_row[DATE_SAMPLING]
            d = datetime.now()
            for col in new_row.index:
                differ = False 
                old, new = old_row[col], new_row[col]
                #perror(f'log_sequences compare {id}, {col}, {type(old)}, {type(new)}, ||{old}||, ||{new}||')
                if isinstance(old, (np.ndarray, pd.Series)) and isinstance(new, (np.ndarray, pd.Series)):
                    differ = not np.array_equal(np.nan_to_num(old), np.nan_to_num(new))
                elif (col == DATA_INFO) and isinstance(old, list) and isinstance(new, list):
                    differ = sorted(old) == sorted(new)
                elif pd.isna(old) and pd.isna(new):
                    differ = False
                elif pd.isna(old) or pd.isna(new):
                    differ = True
                else:
                    differ = old != new
                if differ:
                    log.append([d, id, pd.NA ,col, old, new, self.username, comments])
            return log
        
        old_df = self._freeze_sequences
        new_df = self.get_sequences_copy(ids)
        log = []
        if isinstance(new_df, pd.Series):
            log = compare(ids, old_df, new_df)
        else:
            for (id1, row1), (id2, row2) in zip(old_df.iterrows(), new_df.iterrows()):
                if id1 == id2:
                    log = compare(id1, row1, row2)
                else:
                    raise KeyError('The 2 dataframes are not aligned.')
        self._freeze_sequences = None
        if len(log) > 0:
            self._log += log
            return True
        return False
    
    def get_crossdating_log(self):
        """
        Returns the crossdating log associated with the dataset.

        Returns:
            The crossdating log.
        """
        return self._crossdating
    
    def log_crossdating(self, crossdating):
        """
        Logs the crossdating information for a dataset.

        Parameters:
        crossdating (dict): A dictionary containing the crossdating information.

        Returns:
        None
        """
        crossdating[CROSSDATING_DATE] = datetime.now()
        if len(self._crossdating) > 0:
            self._crossdating.loc[self._crossdating.index.max()+1] = crossdating
        else:
            self._crossdating = pd.DataFrame([crossdating])
        
    
    def is_empty(self):
        """
        Returns True if dataset is empty.
        """
        return len(self.sequences) == 0
        
    def notify_changes(self, message, source=None):
        """
        Set `msg` into `self.change`.
        """
        self.notify_message = message
        if self.save_auto:
            #print('*** Save auto ***')
            self.dump()
            
        self.notification_source = source if source is not None else self
        if message in ['load', 'reindex']:
            self.param.trigger('notify_reload')
        else:
            self.param.trigger('notify_synchronize')
        
    def update(self, update_tree=False):
        """
        Update index and dtype of `self.sequences` and `self.component`.
        """
        self.sequences.reset_index(inplace=True)
        self.sequences = pd.DataFrame(self.sequences, columns=sequences_index+sequences_cols)
        self.sequences.set_index(sequences_index, inplace=True, verify_integrity=True)  
        self.sequences = self.sequences.astype(sequences_dtype_dict, copy=True, errors='ignore')
        self.components.reset_index(inplace=True)
        self.components = pd.DataFrame(self.components, columns=components_index+components_cols)
        self.components.set_index(components_index, inplace=True, verify_integrity=True)  
    
    def clone(self):
        """
        Copy the dataset and returns it.
        """
        tmp = Dataset()
        tmp.sequences = self.sequences.copy()
        tmp.components = self.components.copy()
        tmp._packages = copy.deepcopy(self._packages)
        
        return tmp
    
    def _get_filename(self, filename: str = None) -> str:
        if filename is None:
            if self.filename is None:
                raise ValueError('DataSet._get_filename: empty filename')
            else:
                filename = self.filename
        else:
            self.filename = filename
        return filename

    def backup(self, filename: str):
        """
        Dump/save a dataset into `filename`.
        """
        filename = Path(filename)
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_filename = f"{filename.stem}_{current_datetime}{filename.suffix}"
        #print('backup', filename)
        # Construct the new full file path
        directory = filename.parent 
        new_file_path = directory / 'backup' / new_filename
        os.makedirs(directory / 'backup', exist_ok=True)

        self.dump(new_file_path, save_name=False)
 
    def dump(self, filename: str = None, save_name=True):
        """
        Dump/save a dataset into `filename`.
        """
        filename = self._get_filename(filename) if save_name else filename
        #print('save', filename, self.filename)
        suffix = Path(filename).suffix
        if suffix == '.json':
            self._dump_json(filename)
        elif suffix == '.p':
            self._dump_pickle(filename)
        elif suffix == '.xlsx':
            self._dump_excel(filename)
        else:
            raise TypeError(f'DataSet.dump: unknown suffix {suffix} from {filename}')
        #perror('dump', self.components.index)
        #perror('dump', self.components.index)

    def _dump_pickle(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('wb') as fic:
            #perror('_dump_pickle', self._log)
            pickle.dump((self.VERSION, self.sequences, self.components, self._packages, self._log, self._crossdating), fic)

    def _dump_json(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('w') as fic:
            dfs_json = {
                VERSION: self.VERSION,
                SEQUENCES: json.loads(self.sequences.to_json(orient='table', index=True, force_ascii=False, indent=2)),
                COMPONENTS: json.loads(self.components.to_json(orient='table', index=True, force_ascii=False, indent=2)),
                PACKAGES: self._packages,
                LOG: json.loads(self.get_log().to_json(orient='table', index=True, force_ascii=False, indent=2)),
                CROSSDATING: json.loads(self._crossdating.to_json(orient='table', index=True, force_ascii=False, indent=2))
            }
            json.dump(dfs_json, fic, indent=2)            

    def _dump_excel(self, filename: str):
        filename = Path(filename) 
        with pd.ExcelWriter(filename) as writer:
            self.sequences.to_excel(writer, sheet_name=SEQUENCES, merge_cells=False, float_format="%.6f")
            self.components.to_excel(writer, sheet_name=COMPONENTS, merge_cells=False, float_format="%.6f")

    def _dump_csv(self, path: str):
        base_path = Path(path)
        self.sequences.to_csv(base_path / 'sequences.csv', sep='\t', float_format="%.6f")
        self.components.to_csv(base_path / 'components.csv', sep='\t', float_format="%.6f")

    def update_version(self, version):
        """
        Update the dataset to a specific version.

        Parameters:
        - version (int): The version number to update the dataset to.

        Returns:
        - None

        Raises:
        - None
        """
            
        if version == self.VERSION:
            return
        
        self._log = []
        self._crossdating = pd.DataFrame()
        
        if version <= 1:
            self.sequences[COMPONENT_COUNT] = pd.NA
        if version <= 2:
            mask = self.sequences[CATEGORY] == 'Tree'
            self.sequences.loc[mask, CATEGORY] = MEASURE
            mask = self.sequences[CATEGORY] == 'Chronology'
            self.sequences.loc[mask, CATEGORY] = MEAN
        if version <= 3:
            self.sequences[MEANAS_MEASURE] = False
        if version <= 4:
            if 'Dated' in self.sequences.columns:
                self.sequences.drop(columns=['Dated'], inplace=True)
        if version <= 5:
            if 'tag' in self.sequences.columns:
                self.sequences[TAG] = self.sequences['tag']
                self.sequences.drop(columns=['tag'], inplace=True)
        if version <= 6:
            if 'PithAbsent' in self.sequences.columns:
                self.sequences.drop(columns=['PithAbsent'], inplace=True)
        if version <= 7:
            self.sequences.index.name = sequences_index[0]
            self.components.index.names = components_index  
        if version <= 11:
            for index, row in self.sequences.iterrows():
                length = row[DATA_LENGTH]  # Taille du tableau de zéros
                if pd.notna(length) and length > 0:
                    self.sequences.at[index, DATA_SIGNATURES] = np.zeros(length)
                else:
                    self.sequences.at[index, DATA_SIGNATURES] = pd.NA
        
        logger.info(f'update dataset version {version} to {self.VERSION}')

    def load(self, filename: str=None):
        """
        Load a dataset from `filename`.
        """
        filename = self._get_filename(filename)
        ('load', filename)
        suffix = Path(filename).suffix
        version = self.VERSION
        if suffix == '.json':
            version = self._load_json(filename)
        elif suffix == '.p':
            version = self._load_pickle(filename)
        elif suffix == '.xlsx':
            self._load_excel(filename)
        else:
            raise TypeError(f'DataSet.load: unknown suffix {suffix} from {filename}')
        self.update_version(version)
        self.notify_changes('load')
        #perror('roots', self.get_roots())

    def _load_pickle(self, filename: str):
        dataset_path = Path(filename) 
        with dataset_path.open('rb') as fic:
            data = pickle.load(fic)
            version, self.sequences, self.components, self._packages, self._log, self._crossdating = data
            #perror('load', self._log)
        return version

    def _load_json(self, filename):
        def json_to_df(json_data, key):
            data = json_data[key]["data"]
            
            # Extraire le schéma des colonnes
            schema_fields = json_data[key]["schema"]["fields"]
            columns = [field["name"] for field in schema_fields]

            # Créer le DataFrame avec les colonnes et les données
            return pd.DataFrame(data, columns=columns)
      
       
        dataset_path = Path(filename) 
        with dataset_path.open('r') as fic:
            dfs_json = json.load(fic)
        version = dfs_json[VERSION]
        self.sequences = json_to_df(dfs_json, SEQUENCES)
        self.sequences[DATA_VALUES] = self.sequences[DATA_VALUES].apply(lambda x: np.array(x)) 
        self.sequences[DATA_WEIGHTS] = self.sequences[DATA_WEIGHTS].apply(lambda x: np.array(x))
        self.sequences[DATA_SIGNATURES] = self.sequences[DATA_SIGNATURES].apply(lambda x: np.array(x))
        
        self.components = json_to_df(dfs_json, COMPONENTS)    
        self._packages = dfs_json[PACKAGES]
        self._log = json_to_df(dfs_json, LOG)
        self._crossdating = json_to_df(dfs_json, CROSSDATING)
        self.update()
        return version
    
    def _load_excel(self, filename: str):
        filename = Path(filename) 
        seqs = pd.read_excel(filename, sheet_name=SEQUENCES)
        comps = pd.read_excel(filename, sheet_name=COMPONENTS)
        self.sequences = pd.DataFrame(seqs)
        self.components = pd.DataFrame(comps)        
        self.update()

    def _load_csv(self, path: str):
        base_path = Path(path)
        seqs = pd.read_csv(base_path / 'sequences.csv', sep='\t')
        comps = pd.read_csv(base_path / 'components.csv', sep='\t')
        self.sequences = pd.DataFrame(seqs)
        self.components = pd.DataFrame(comps)        
        self.update()
        
    def new_dataset(cls):
        """
        Create a new dataset.

        Returns:
            dataset (cls.Dataset): The newly created dataset.
        """
        dataset = cls.Dataset()
        dataset.new_root()
        dataset.new_trash()
        dataset.new_workshop()
        return dataset
    
    def new_root_id(self):
        """
        Create a new root node in the dataset.

        Returns:
            int: The index of the new root node.
        """
        return self.sequences.index.min() - 10
    
    def new_root(self, keycode: str = 'Dataset', id = ROOT, append=True):
        """
        Create a new root node in the dataset.

        Args:
            keycode (str, optional): The keycode for the new root node. Defaults to 'Dataset'.
            id (int, optional): The index of the new root node. Defaults to ROOT.

        Returns:
            int: The index of the new root node.

        """
        self.new(keycode, SET, id_parent=None, id=id)
        if append:
            data = []
            for id_child in set(self.get_roots()):
                if id != id_child:
                    data.append({ID_PARENT: id, ID_CHILD: id_child, OFFSET: pd.NA})
            df = pd.DataFrame(data).set_index(components_index, verify_integrity=True)
            with warnings.catch_warnings():
                # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                warnings.filterwarnings("ignore", category=FutureWarning)
                self.components = pd.concat([self.components, df])
        return id
            
    def new_trash(self, keycode: str = 'Trash'):
        """
        Create a new trash item in the dataset.

        Parameters:
            keycode (str): The keycode for the trash item. Defaults to 'Trash'.

        Returns:
            The newly created trash item.
        """
        return self.new(id=TRASH, id_parent=None, keycode=keycode, category=SET)

    def new_workshop(self, keycode: str = 'Workshop' ):
        """
        Create a new workshop in the dataset.

        Parameters:
            keycode (str): The keycode for the workshop. Defaults to 'Workshop'.

        Returns:
            The newly created workshop.
        """
        return self.new(id=WORKSHOP, id_parent=None, keycode=keycode, category=SET)

    def new_clipboard(self, keycode: str = 'Clipboard' ):
        """
        Create a new clipboard entry in the dataset.

        Parameters:
            keycode (str): The keycode for the clipboard entry. Defaults to 'Clipboard'.

        Returns:
            The newly created clipboard entry.
        """
        return self.new(id=CLIPBOARD, id_parent=None, keycode=keycode, category=SET)

    def new(self, keycode: str, category: str, id_parent: int | None, 
            id: int | None = None, others = {}, offset : int = pd.NA) -> int:
        """
        Creat a new Sequence and component if id_parent is not None.
        
        Arguments
        ---------
        keycode: KEYCODE of the new Sequence.
        category: CATEGORY of the new Sequence.
        id_parent: ID_PARENT of the new Conponent.
        id: ID of the Sequence.
        others: dictionary of field, value pairs to set in new Sequence.
        offset: offset to set in new Component.
        make_root : !!!! error !!! make_root and id_parent
        
        
        Returns
        -------
        The ID of the new Sequence.
        """
        id = self.sequences.index.max() + 1 if id is None else id
        others.update({KEYCODE: keycode, CATEGORY: category})
        if CREATION_DATE not in others:
            others[CREATION_DATE] = datetime.now()
        self.sequences.loc[id, list(others.keys())] = others
        if id_parent is not None:
            self.components.loc[(id_parent, id), OFFSET] = offset
        #self.notify_changes(f'new')
        return id                

    def _id_list(self, ids):
        """
        Returns a list of int created form a List[int] of from int.
        """
        if not isinstance(ids, list):
            ids = [ids]
        return ids
 
    def copy(self, triplets: List[Tuple[int, int, int]], dest_path:  List[int], notify=True) -> str:
        """
        Copy `triplets` in dest_path.
        
        Arguments
        ---------
        triplets: list of tuples (ID_PARENT, ID_CHILD, OFFSET)
        dest_path: a path
        
        Returns
        -------
        A dictonary of destination data : {(ID_PARENT, ID_CHILD): OFFSET}
        """
        # detect circular referencies
        couples_ = [(p, c) for p, c, o in triplets if dest_path[-1] != p]
        if len(couples_) != len(triplets):
            logger.warning('Destination and source are equal. Copy aborded.')
            return None

        couples_ = [(p, c) for p, c, o in triplets if c not in dest_path] 
        if len(couples_) != len(triplets):
            logger.warning('circular reference. Copy aborded.')
            return None

        dest_map = {(dest_path[-1], c) : o for p, c, o in triplets}
        msg = ''
        for keys, offset in dest_map.items():
            if keys in self.components.index:
                msg= str(keys[1])+', '
            else :
                self.components.loc[keys, OFFSET] = offset
        if msg != '':
            msg = 'Duplicates not copied: ' + msg 
            logger.warning(msg)

        if notify:
            self.notify_changes('copy')
                            
        return dest_map
    
    def move(self, triplets: List[Tuple[int, int, int]], dest_path:  List[int], notify=True) -> str:
        """
        Cut `triplets` in dest_path.
        
        Arguments
        ---------
        triplets: list of tuples (ID_PARENT, ID_CHILD, OFFSET)
        dest_path: a path
        
        Returns
        -------
        A dictonary of destination data : {(ID_PARENT, ID_CHILD): OFFSET}
        """
        dest_map = self.copy(triplets, dest_path)
        if dest_map is not None:
            keys = [(p, c) for p, c, o in triplets if p != -1]
            #logger.info(f'dataset cut keys: {keys}')
            self.components.drop(index=keys, inplace=True)
            if notify:
                self.notify_changes('cut')
        return dest_map
        
    def drop(self, triplets: List[Tuple[int, int, int]], notify=True)-> str:
        """
        drop `triplets`.
        
        Arguments
        ---------
        triplets: list of tuples (ID_PARENT, ID_CHILD, OFFSET)
        
        Returns
        -------
        List of sequences droped
        """
        def drop_children(node, cpt_drops, drop_comp, drop_seq, deep=0):
            if cpt_drops[node.id] >= 0:
                #perror('cpt_drops[node.id]', cpt_drops[node.id])
                drop_comp.append((node.parent.id, node.id))
                drop_seq.append(node.id)
                for child in node.children:
                    drop_children(child, cpt_drops, drop_comp, drop_seq, deep+1)
            else:
                if deep == 0:
                    drop_comp.append((node.parent.id, node.id))
                logger.warning(f'Child {node.id} / {node.keycode} has {cpt_drops[node.id]} is dupplicated.')
        
        id_roots = self.get_roots()
        tree_roots = self.get_descendants(id_roots)
        cpt_roots = tree_roots.count_descendants()
        #perror('cpt_roots', cpt_roots)
        
        id_drops = list(set([c for p, c, o in triplets]))
        tree_drops = self.get_descendants(id_drops)
        cpt_drops = tree_drops.count_descendants()
        
        #perror('cpt_drops', cpt_drops)
        
        for key in cpt_drops.keys():
            if key in cpt_roots.keys():
                #perror('cpt_drops[key]', key, cpt_drops[key])
                #perror('cpt_roots[key]', key, cpt_roots[key])
                cpt_drops[key] = cpt_drops[key] - cpt_roots[key]

        #perror('cpt_drops', cpt_drops)
        
        drop_seq = []
        drop_comp = []
        
        for child in tree_drops.children:
            drop_children(child, cpt_drops, drop_comp, drop_seq)

    def soft_drop(self, pairs: List[Tuple[int, int]]) -> str:
        """
        soft drop of `triplets` in trash set.
        
        Arguments
        ---------
        pairs: list of tuples (ID_PARENT, ID_CHILD)

        Returns
        -------
        A string with duplicate sequences erased in trash.
        """
        return self.move(pairs, dest_path=[TRASH])
        
    def clean(self):
        """
        Remove data in `self.sequences` and `self.components` 
        """
        self.sequences = pd.DataFrame()
        self.components = pd.DataFrame()
        #self.notify_changes(f'clean')

    def append(self, dataset, verify_integrity=True, notify=True, merge_root=False):
        """
        Append a dataset to `self`. Warning use pd.concat with NA values.
        deprecated: use `merge` instead.
        """
        if len(self.sequences) > 0:
            tmp = dataset.clone()
            tmp.sequences.drop(index=WORKSHOP, inplace=True)
            tmp.sequences.drop(index=CLIPBOARD, inplace=True)
            tmp.sequences.drop(index=TRASH, inplace=True)
            roots = tmp.get_roots()
            #perror('get roots before drop', roots)
            if (tmp.components.index.get_level_values(ID_PARENT) == WORKSHOP).sum() > 0:
                tmp.components.drop(index=WORKSHOP, inplace=True)
            if (tmp.components.index.get_level_values(ID_PARENT) == CLIPBOARD).sum() > 0:
                tmp.components.drop(index=CLIPBOARD, inplace=True)
            if (tmp.components.index.get_level_values(ID_PARENT) == TRASH).sum() > 0:
                tmp.components.drop(index=TRASH, inplace=True)
            min_id = self.sequences.index.min() - 10
            roots = tmp.get_roots()
            #perror('get roots after drop', roots)
            index_mapping = dict(zip(roots, [i*-10+min_id for i in range(len(roots))]))
            #print(index_mapping)
            tmp.components.rename(index=index_mapping, level=ID_PARENT, inplace=True)
            tmp.sequences.rename(index=index_mapping, level=ID, inplace=True)
            
            tmp.reindex(start=self.sequences.index.max() + 1)
            with warnings.catch_warnings():
                # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                warnings.filterwarnings("ignore", category=FutureWarning)
                #print(keep)
                self.sequences = pd.concat([self.sequences, tmp.sequences], verify_integrity=verify_integrity)
                self.components = pd.concat([self.components, tmp.components], verify_integrity=verify_integrity)
        else:
            self.sequences = dataset.sequences.copy()
            self.components = dataset.components.copy()
        if notify:
            self.notify_changes('append')
              
    def reindex(self, start=0, notify=True) -> int:
        """
        Reindex sequences from `start` to `start` + number of sequences. 
        Modifies ID_CHILD and IXD_PARENT values in components.

        deprecated: never use.
        
        Returns
        -------
        the last ID        
        """
        # Reindexing with contiguous index
        last = start + len(self.sequences.loc[self.sequences.index >= 0])
        new_index = list(range(start, last))
        # Create a mapping dictionary between old and new index
        index_mapping = dict(zip(self.sequences.index[self.sequences.index >= 0], new_index))
        # Use the dictionary to reindex
        tmp = self.components.rename(index=index_mapping, level=ID_PARENT)
        self.components = tmp.rename(index=index_mapping, level=ID_CHILD)
        self.sequences = self.sequences.rename(index=index_mapping, level=ID)
        if notify:
            self.notify_changes('reindex')
        return last

    def drop_orphans_components(self, paires, level=ID_PARENT):
        self.components = self.components.drop(paires)

    def get_orphans_sequences(self):
        # get sequences that are not TRASH, WORKSHOP, CLIPBOARD, ...
        # root nodes should be < 0
        seqs = set(self.sequences.index[self.sequences.index > 0].tolist())
        parent_ids = set(self.components.index.get_level_values(ID_PARENT).tolist())
        child_ids = set(self.components.index.get_level_values(ID_CHILD).tolist())
        
        orphans = seqs - (parent_ids | child_ids)
        
        return orphans
        
    def get_orphans_components(self, level=ID_PARENT):
        """
        Get orphan ID 

        Returns
        -------
        List of ID        
        """
        ids = set(self.components.index.get_level_values(level).unique().tolist())
        seqs = set(self.sequences.index.unique().tolist())
        filters = self.components.index.get_level_values(level).isin(list(ids - seqs))
        return self.components.index[filters].tolist()
        
    def get_roots(self):
        """
        Get ID_CHILD roots of components and orphan ID sequences

        Returns
        -------
        List of ID        
        """
        root = ~self.sequences.index.isin(self.components.index.get_level_values(ID_CHILD))
        ids = self.sequences.index[root].unique().tolist() 
        return ids

    def get_leafs(self) -> List[int]:
        """
        Get ID_CHILD leafs of components 

        Returns
        -------
        List of ID_CHILD        
        """
        leaf = ~self.components.index.get_level_values(ID_CHILD).isin(self.components.index.get_level_values(ID_PARENT))
        return self.components[leaf].index.get_level_values(ID_CHILD).unique().tolist()

    def get_sequences(self, ids: int | List[int]) -> pd.DataFrame:
        """
        Get sequences of `ids`

        Returns
        -------
        A pandas DataFrame.        
        """
        return self.sequences.loc[self._id_list(ids), :]
    
    def get_components(self, pairs : Tuple[int, int] | List[Tuple[int, int]] = None) -> pd.DataFrame:
        """
        Get the  joint view of components and sequences of `pairs` (ID_PARENT, ID_CHILD)
        
        Returns
        -------
        A pandas DataFrame.        
        """
        comps = self.components.loc[pairs, :] if pairs is not None else self.components
        comps = comps.join(self.sequences, on=ID_CHILD, how='left')   
        comps = comps.join(self.sequences[KEYCODE], on=ID_PARENT, how='left', rsuffix='Parent')
        return comps

    def package_keys(self):
        return list(self._packages.keys())
    
    def set_package(self, key: str, value: List[Tuple[int, int]]):
        self._packages[key] = value
        self.param.trigger('notify_packages')

    def get_package(self, key: str) -> List[Tuple[int, int]]:
        if key not in self._packages:
            raise KeyError(f'DataSet.get_selections: {key} not in selections')
        return self._packages[key]

    def delete_all_packages(self):
        self._packages = {}
        self.param.trigger('notify_packages')

    def delete_package(self, key: str):
        if key not in self._packages:
            raise KeyError(f'DataSet.get_selections: {key} not in selections')
        del self._packages[key]
        self.param.trigger('notify_packages')
    
    
    def get_package_components(self, key: str, slope_resolution=None, param_cambium_estimation=None) -> pd.DataFrame:
        """
        Return the selection (a joint view of components and sequences) stored in dictonary `self.selection`.        
        
        Arguments
        ---------
        key: name of the selection.
        
        Returns
        -------
        A pandas DataFrame.
        """        
        def do_cambium_estimation(df, param):
            if CAMBIUM_LOWER not in df.columns:
                df[[CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = [pd.NA, pd.NA, pd.NA]
            if (param.cambium_estimation_method != 'user values'):
                for id, row in df.iterrows():
                    df.loc[id, [CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER]] = cambium_estimation(param, row[CAMBIUM], row[BARK], row[SAPWOOD], row[DATA_VALUES])

        df = self.get_components(self.get_package(key))
        if slope_resolution is not None:
            df[SLOPE] = df[DATA_VALUES].apply(lambda x: slope(x, slope_resolution))
            
        if param_cambium_estimation is not None:
            do_cambium_estimation(df, param_cambium_estimation)
        
        return df
 
    def get_data(self, ids: Union[int, List[int], None] = None, category: Union[str, None] = None, 
                id_roots=None, max_depth: Union[int, None] = None) -> pd.DataFrame:
        """
        Create a joint view of components and sequences of `ids` descendants.        
        
        Arguments
        ---------
        ids: an `id` or a list of `id`.
        max_depth: if not `pd.NA`, limits the recursive loop to max_deep level.
        
        Returns
        -------
        A pandas DataFrame.
        """
        d = []
        if ids is None:
            ids = self.get_roots()
        ids = self._id_list(ids)
        if id_roots is None:
            include_parent = False
            id_roots = [-1] * len(ids)
        else:
            id_roots = self._id_list(id_roots)
            include_parent = True
        dict_id_roots = {id: id_root for id, id_root in zip(ids, id_roots)}
        
        pairs = set()
        tree = self.get_descendants(ids, max_depth=max_depth)        
        for node, offset in tree.filter(categories=category, max_depth=max_depth).items():
            id_parent = node.parent.id if node.id not in ids else dict_id_roots[node.id]
            if (node.id not in ids) or include_parent:
                if (node.id, id_parent) not in pairs:
                    d.append({ID_CHILD: node.id, ID_PARENT: id_parent, OFFSET: offset})
                    pairs.add((node.id, id_parent))
            
        components = pd.DataFrame(d, columns=components_index+components_cols)
        components.set_index(components_index, inplace=True, verify_integrity=True)  
        return components.join(self.sequences, on=ID_CHILD, how='left')

    def get_path_to_root(self, id: int) -> List[int]:
        if id is None:
            return []
        lst = [id]
        if id < 0:
            return lst
        id_parents = self.components.xs(id, level=ID_CHILD)
        if len(id_parents) > 0:
            if len(id_parents) > 1:
                logger.warning(f'multiple parents for {id} in {id_parents.index[0]}')
            lst = self.get_path_to_root(id_parents.index[0]) + lst
        #print('get_path_to_root:', lst)
        return lst
        
    def get_ascendants(self, id: int, recursive=False, categories=[MEAN, SET]):
        #perror('get_ascendants', id)
        comp = self.components
        id_parents = comp.xs(id, level=ID_CHILD).index.to_list() if id in comp.index.get_level_values(ID_CHILD) else []
        #perror('get_ascendants', id_parents, len(id_parents))
        l = self.sequences.loc[id_parents, CATEGORY].isin(categories).index.tolist() if len(id_parents) > 0 else []

        if recursive:
            for i in l:
                l += self.get_ascendants(i, recursive, categories)
        return l

    def get_category(self, category, mean_as_measure, check_mean_as_measure):
        #logger.info(f'get_category: {category} {mean_as_measure} {check_mean_as_measure}')
        if check_mean_as_measure and mean_as_measure and (category == MEAN):
            logger.warning(f'get_category: {category} is replaced by {MEASURE}')
            return MEASURE
        return category    

    def get_descendants(self, ids: int | List[int], max_depth=None, check_mean_as_measure=False) -> ComponentsTree():
        """
        Get descendants of `ids`.
        
        Arguments
        ---------
        ids: an `id` or a list of `id`.
        max_depth: if not `pd.NA`, limits the recursive loop to max_deep level.

        Returns
        -------
            A tree.
        """
        categories_keycodes = self.sequences.loc[:, [CATEGORY, MEANAS_MEASURE, KEYCODE]]
        data = self.components.join(categories_keycodes, on=ID_CHILD, how='left')
        group_parents = data.groupby(ID_PARENT)
        id_depth = []

        def iterate(parent, id, keycode, category, mean_as_measure, offset, depth, max_depth):
            if id in id_depth:
                keycode_id = self.sequences.at[id, KEYCODE]
                keycode_id_depth = [self.sequences.at[i, KEYCODE] for i in id_depth]                
                logger.warning(f'DataSet.get_descendants: circular reference: {id} in {id_depth}. Recursive loop aborded.\n {keycode_id} in {keycode_id_depth}')
                return None
            id_depth.append(id)
            category = self.get_category(category, mean_as_measure, check_mean_as_measure)
            node = ComponentsNode(parent, id, keycode, category, offset, depth=depth)
            if (id in group_parents.groups) and (category != MEASURE) and ((max_depth is None) or (depth+1 <= max_depth)):
                for (_, id_child), row in group_parents.get_group(id).iterrows():
                    child = iterate(node, id_child, row[KEYCODE], row[CATEGORY], row[MEANAS_MEASURE], row[OFFSET], depth+1, max_depth)
                    if child is not None:
                        node.append(child)
            id_depth.pop()
            return node
            #return node, errors
        
        tree = ComponentsTree()
        for id in self._id_list(ids):
            child = iterate(tree, id, categories_keycodes.at[id, KEYCODE], categories_keycodes.at[id, CATEGORY], categories_keycodes.at[id, MEANAS_MEASURE], 0, 0, max_depth)
            if child is not None:
                tree.append(child)
        return tree

    def edit_component(self, id_parent, id_child, value, notify=True, source=None):
        ids = [(id_parent, id_child)]
        self.freeze_components(ids)
        self.components.at[(id_parent, id_child), OFFSET] = np.round(value)

        self.log_components(ids, 'edit_component')
        if notify:
            self.notify_changes('notify_synchronize', source=source)
        if self.save_auto:
            self.dump()
    
    def edit_sequence(self, ids, column, value, notify=True, source=None):
        def check_keycode():
            if column == KEYCODE:
                if len(ids) > 1:
                    raise ValueError(f'Edit: multiple editions for {column} are not allowed')
                elif value in self.sequences[KEYCODE].values:
                    raise ValueError(f'Edit: duplicate {KEYCODE} for value: {value}')
        
        def update(ids, column, value):
            #perror('update', ids, column, value)
            for id in ids:
                self.sequences.at[id, column] = value       
            
        def update_date_end(ids):
            self.sequences.loc[ids, DATE_END] = self.sequences.loc[ids, DATE_BEGIN] + self.sequences.loc[ids, DATA_LENGTH] - 1

        def update_date_begin(ids):
            self.sequences.loc[ids, DATE_BEGIN] = self.sequences.loc[ids, DATE_END] - self.sequences.loc[ids, DATA_LENGTH] + 1
            
        if sequences_dtype_dict[column].lower().startswith('int'):
            value = np.round(value) if pd.notna(value) else pd.NA
        elif sequences_dtype_dict[column].lower().startswith('float'):
            if pd.isna(value):
                value = pd.NA   
        elif sequences_dtype_dict[column].lower().startswith('bool'):
            value = string_to_boolean(value)
        
        ids = self._id_list(ids)    
        check_keycode() 
        self.freeze_sequences(ids)
        
        update(ids, column, value)
        if column == DATA_VALUES:
            update(ids, DATA_LENGTH, len(value))
            update_date_end(ids)
        elif column == DATE_BEGIN:
            update_date_end(ids)
        elif column == DATE_END:
            update_date_begin(ids)

        self.log_sequences(ids, 'edit_sequence')
        
        if notify:
            self.notify_changes('notify_synchronize', source=source)
        if self.save_auto:
            self.dump()

    def set_inconsistent_on_ascendants(self, id, notify=True, source=None):
        ascendants = self.get_ascendants(id, recursive=True)
        if len(ascendants) > 0:
            self.edit_sequence(ascendants, INCONSISTENT, True, notify=False)
        if notify:
            self.notify_changes('notify_synchronize', source=source)

    def shift_offsets(self, parent_id, child_ids=None, notify=True):
        """
        Get children of `parent_id` and shift the children offsets to 0.
        """
        data = self.get_data(parent_id, max_depth=1)
        if child_ids is not None:
            data = data[data.index.get_level_values(ID_CHILD).isin(child_ids)]
        if data[OFFSET].isna().any():
            raise ValueError(f'DataSet.shift_offsets: one or more ({ID_PARENT}, {ID_CHILD}) contain NA values in {OFFSET} field.')
        ids = data.index.to_list()
        
        self.freeze_components(ids)
        self.components.loc[ids, OFFSET] -= data[OFFSET].min()
        self.log_components(ids, 'shift_offsets')
        if notify:
            self.notify_changes('notify_synchronize')

    def copy_dates_to_offsets(self, parent_id, child_ids=None, notify=True):
        """
        Get children of `parent_id`, copy dates to offsets and shift to 0 (if `shift` is True).
        """
        data = self.get_data(parent_id, max_depth=1)
        if child_ids is not None:
            data = data[data.index.get_level_values(ID_CHILD).isin(child_ids)]
        if data[DATE_BEGIN].isna().any():
            logger.warning(f'one or more ({ID_PARENT}, {ID_CHILD}) contain NA values in {DATE_BEGIN} field.')
        ids = data.index.to_list()
        self.freeze_components(ids)
        self.components.loc[ids, OFFSET] = data.loc[ids, DATE_BEGIN]
        self.log_components(ids, 'copy_dates_to_offsets')
        if notify:
            self.notify_changes('notify_synchronize')

    def set_offsets_to_dates(self, parent_id, child_ids=None, notify=True):
        """
        Get children of `parent_id`, copy dates to offsets and shift to 0 (if `shift` is True).
        """
        data = self.get_data(parent_id, max_depth=1)
        if child_ids is not None:
            data = data[data.index.get_level_values(ID_CHILD).isin(child_ids)]
        if data[OFFSET].isna().any():
            raise ValueError(f'DataSet.set_offsets_to_dates: one or more ({ID_PARENT}, {ID_CHILD}) contain NA values in {OFFSET} field.')
        min_offset = data[OFFSET].min()
        min_date = data.at[(data[OFFSET] == min_offset).idxmax(), DATE_BEGIN]
        if pd.isna(min_date):
            raise ValueError(f'DataSet.set_offsets_to_dates: {DATE_BEGIN} corresponding to min {OFFSET} contains NA value.')
        data[OFFSET] -= min_offset
        ids = data.index.get_level_values(ID_CHILD).to_list()
        self.freeze_sequences(ids)
        self.sequences.loc[ids, DATE_BEGIN] =  data.reset_index().set_index(ID_CHILD)[OFFSET] + min_date
        self.sequences.loc[ids, DATE_END] = self.sequences.loc[ids, DATE_BEGIN] + self.sequences.loc[ids, DATA_LENGTH] - 1        
        self.log_sequences(ids, 'set_offsets_to_dates')
        if notify:
            self.notify_changes('notify_synchronize')

    def set_date_begin(self, parent_id, child_ids=None, notify=True):
        data = self.get_data(parent_id, max_depth=1)
        if child_ids is not None:
            data = data[data.index.get_level_values(ID_CHILD).isin(child_ids)]
        if data[DATE_END].isna().any():
            raise ValueError(f'DataSet.set_date_begin: one or more ({ID_PARENT}, {ID_CHILD}) contain NA values in {DATE_END} field.')
        if data[DATA_LENGTH].isna().any():
            raise ValueError(f'DataSet.set_date_begin: one or more ({ID_PARENT}, {ID_CHILD}) contain NA values in {DATA_LENGTH} field.')
        ids = data.index.get_level_values(ID_CHILD).to_list()
        self.freeze_sequences(ids)
        self.sequences.loc[ids, DATE_BEGIN] =  self.sequences.loc[ids, DATE_END] - self.sequences.loc[ids, DATA_LENGTH] + 1
        self.log_sequences(ids, 'set_date_begin')
        if notify:
            self.notify_changes('notify_synchronize')

    def set_date_end(self, parent_id, child_ids=None, notify=True):
        data = self.get_data(parent_id, max_depth=1)
        if child_ids is not None:
            data = data[data.index.get_level_values(ID_CHILD).isin(child_ids)]
        if data[DATE_BEGIN].isna().any():
            raise ValueError(f'DataSet.set_date_end: one or more ({ID_PARENT}, {ID_CHILD}) contain NA values in {DATE_BEGIN} field.')
        if data[DATA_LENGTH].isna().any():
            raise ValueError(f'DataSet.set_date_end: one or more ({ID_PARENT}, {ID_CHILD}) contain NA values in {DATA_LENGTH} field.')
        ids = data.index.get_level_values(ID_CHILD).to_list()
        self.freeze_sequences(ids)
        self.sequences.loc[ids, DATE_END] =  self.sequences.loc[ids, DATE_BEGIN] + self.sequences.loc[ids, DATA_LENGTH] - 1
        self.log_sequences(ids, 'set_date_end')
        if notify:
            self.notify_changes('notify_synchronize')


    def check_ring_count(self, parent_id):
        """
        Check the ring count of the given parent index.

        Args:
            parent_id (int): The index of the parent.

        Raises:
            ValueError: If the ring count does not match the length of the values.

        Returns:
            None
        """
        def length_(values):
            l = len(values) if values is not None else 0
            #logger.debug(f'{l}, {values}')
            return l
        data = self.get_data(parent_id, max_depth=1)
        ring_count = data[DATA_VALUES].apply(lambda x: length_(x))
        if not (ring_count == data[DATA_LENGTH]).all():
            raise ValueError(f'{DATA_LENGTH} does not match the length of {DATA_VALUES}.')

    def check_date_ring_count(self, id):
        """
        Checks the date and ring count consistency for a given parent index.

        Args:
            parent_id (int): The index of the parent node.

        Raises:
            ValueError: If the date and ring count are not consistent.

        Returns:
            None
        """
        self.check_ring_count(id)
        data = self.get_data(id, max_depth=1)
        min_date = data[DATE_BEGIN].min()
        data[DATE_BEGIN] -= min_date        
        data[DATE_END] -= min_date
        if not ((data[DATE_END] - data[DATE_BEGIN] + 1) == data[DATA_LENGTH]).all():
            for row in data.itertuples():
                db = row.DATE_BEGIN
                de = row.DATE_END
                dl = row.DATA_LENGTH
                dl2 = de - db + 1
                if dl2 != dl:
                    logger.warning(f' {row.KEYCODE} {row.DATE_BEGIN} {row.DATE_END} {row.DATA_LENGTH} {row.OFFSET} {dl2} != {dl}')
            raise ValueError(f'DataSet.check_date_ring_count: {DATE_BEGIN} / {DATE_END} and {DATA_LENGTH} are not consistent.')
    
    def check_offset_begin_date(self, id):
        """
        Check the consistency between the 'OFFSET' and 'DATE_BEGIN' columns in the dataset.

        Args:
            parent_id (int): The index of the parent dataset.

        Raises:
            ValueError: If the 'OFFSET' and 'DATE_BEGIN' columns are not consistent.

        Returns:
            None
        """
        data = self.get_data(id, max_depth=1)
        data[OFFSET] -= data[OFFSET].min()
        min_date = data[DATE_BEGIN].min()
        data[DATE_BEGIN] -= min_date
        if not(data[OFFSET] == data[DATE_BEGIN]).all():
            raise ValueError(f'DataSet.check_offset_begin_date: {DATE_BEGIN} and {OFFSET} are not consistent.')
        
    def check_date_offset_count(self, id):
        """
        Checks the date offset count for a given parent index.

        Parameters:
        - parent_id (int): The index of the parent.

        Returns:
        None
        """
        self.check_date_ring_count(id)
        self.check_offset_begin_date(id)

    def set_dates(self, id, date_begin, data_length=None, sequences=None, warning=True, notify=True, source=None):
        """
        Set DATE_END and DATE_BEGIN (if not NA) of `id` series given a `date_begin` 
        and a `ring_count`.

        Parameters:
        - id (int): The index of the series.
        - date_begin (datetime): The beginning date for the series.
        - data_length (int, optional): The length of the data. If not provided, it will be retrieved from the sequences.
        - sequences (pandas.DataFrame, optional): The sequences dataframe. If not provided, it will use the self.sequences.
        - warning (bool, optional): Whether to show a warning if there is a potential inconsistent mean. Default is True.
        """
        if sequences is None:
            sequences = self.sequences
        if pd.notna(date_begin):
            keycode = sequences.at[id, KEYCODE]
            date_first = sequences.at[id, DATE_BEGIN]
            if pd.notna(date_first) and (date_begin != date_first) and (warning):
                logger.warning(f'potential inconsistent mean, {keycode} {DATE_BEGIN} changed: {date_begin} ')
            self.freeze_sequences(id)
            if data_length is None:
                data_length = sequences.at[id, DATA_LENGTH]
            else:
                sequences.at[id, DATA_LENGTH] = data_length
            sequences.at[id, DATE_BEGIN] = date_begin                
            sequences.at[id, DATE_END] = date_begin + data_length - 1
            self.log_sequences(id, 'set_dates')
            if notify:
                self.notify_changes('notify_synchronize', source=source)

            
    def set_chononology_info(self, id, means, weights, offsets, signatures, data_type, data_samples, sequences=None):
        """
        Set the mean information for a given index in the dataset.

        Args:
            id (int): The index of the sequence to update.
            means (list): The mean values of the sequence.
            weights (list): The weights of the sequence.
            offsets (list): The offsets of the sequence.
            data_type (str): The type of data.
            data_samples (pandas.DataFrame): The data samples.
            sequences (pandas.DataFrame, optional): The sequences dataframe. Defaults to None.

        Returns:
            None
        """
        if sequences is None:
            sequences = self.sequences
        #self.freeze_sequences(id)
        sequences.at[id, DATA_VALUES] = means
        sequences.at[id, DATA_TYPE] = data_type
        sequences.at[id, DATA_LENGTH] = len(means)
        sequences.at[id, DATA_WEIGHTS] = weights
        sequences.at[id, DATA_INFO] = offsets
        sequences.at[id, DATA_SIGNATURES] = signatures
        sequences.at[id, DATE_SAMPLING] = datetime.now()
        sequences.at[id, INCONSISTENT] = False
        sequences.at[id, CAMBIUM] = False
        sequences.at[id, PITH] = False
        sequences.at[id, CAMBIUM_SEASON] = ''
        sequences.at[id, SAPWOOD] = pd.NA
        
        sequences.at[id, CATEGORY] = MEAN
        for key in [SITE_ELEVATION, SITE_CODE, SITE_LATITUDE, SITE_LONGITUDE, SPECIES, LABORATORY_CODE, PROJECT, URI]: 
            l = data_samples[key].unique()
            if len(l) == 1:
                sequences.at[id, key] = l[0]
        date_min = data_samples[DATE_BEGIN].min()
        self.set_dates(id, date_min, len(means), notify=False)
        sequences.at[id, COMPONENT_COUNT] = len(data_samples)
        
        #self.log_sequences(id, 'Mean update')
    
    def means(self, ids, date_as_offset=False, biweight=False, num_threads=1, check_mean_as_measure=False, slope_resolution=0, min_elements=4):
        """
        Compute means for the given indices.

        Args:
            ids (list): List of indices for which to compute means.
            date_as_offset (bool, optional): Whether to treat dates as offsets. Defaults to False.
            biweight (bool, optional): Whether to use biweight location and scale estimators. Defaults to False.
            num_threads (int, optional): Number of threads to use for computation. Defaults to 1.

        Returns:
            None
        """
        tree = self.get_descendants(ids, check_mean_as_measure=check_mean_as_measure)
        
        node_means = tree.filter(categories=[MEAN, SET], max_depth=1) 
        id_means = []
        data_dict = {}
        for node in node_means:
            id = node.id
            if id in ids: # Need in the return
                if (id not in id_means):  # Never computed 
                    id_means.append(id)
                    samples = {node.id: offset for node, offset in node.descendants[MEASURE].items()}
                    dt_data = self.get_sequences(list(samples.keys())).copy()
                    dt_data[OFFSET] = list(samples.values())
                    data_dict[id] = dt_data
        
        results = compute_means(data_dict, ring_type=RAW, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads, slope_resolution=slope_resolution, min_elements=min_elements)
        for id, values in results.items():
            means, weights, offsets, signatures = values
            self.set_chononology_info(id, means, weights, offsets, signatures, RAW, data_dict[id], sequences=None)
            self.set_inconsistent_on_ascendants(id, notify=False)           

        if self.save_auto:
            self.dump()

    def detrend(self, ids, ring_type, window_size=5, do_log=False, date_as_offset=False, biweight=False, slope_resolution=0, min_elements=4):
        """
        Detrends the data for the specified indices.

        Args:
            ids (list): List of indices to detrend.
            ring_type (str): Type of ring data.
            window_size (int, optional): Size of the moving window for detrending. Defaults to 5.
            do_log (bool, optional): Whether to apply logarithmic transformation. Defaults to False.
            date_as_offset (bool, optional): Whether to treat dates as offsets. Defaults to False.
            biweight (bool, optional): Whether to use biweight location and scale estimators. Defaults to False.
            num_threads (int, optional): Number of threads to use for parallel processing. Defaults to 1.

        Returns:
            pandas.DataFrame: Detrended data for the specified indices.
        """
        tree = self.get_descendants(ids)
        num_threads=1
        
        if MEASURE in tree.descendants:
            ids_samples = list(set([node.id for node in tree.descendants[MEASURE].keys()]))
            data_samples = self.get_sequences(ids_samples)
            dt_samples = detrend(data_samples, ring_type, window_size=window_size, do_log=do_log, num_threads=num_threads)
        dt_chonology = []
        if MEAN in tree.descendants:
            node_means = tree.filter(categories=[MEAN], max_depth=1)
            id_means = []
            data_dict = {}
            for node in node_means:
                id = node.id
                if id in ids: # Need in the return
                    if (id not in id_means):  # Never computed 
                        id_means.append(id)
                        samples = {node.id: offset for node, offset in node.descendants[MEASURE].items()}
                        dt_data = dt_samples.loc[list(samples.keys()), :]
                        dt_data[OFFSET] = list(samples.values())
                        data_dict[id] = dt_data
            results = compute_means(data_dict, ring_type=ring_type, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads, slope_resolution=slope_resolution, min_elements=4)
            for id, values in results.items():
                means, weights, offsets, signatures = values
                seq = self.get_sequences(id).copy()
                self.set_chononology_info(id, means, weights, offsets, signatures, ring_type, data_dict[id], sequences=seq)
                dt_chonology.append(seq)
        with warnings.catch_warnings():
            # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
            warnings.filterwarnings("ignore", category=FutureWarning)
            data_dt = pd.concat([dt_samples]+dt_chonology)
        return data_dt.loc[ids, :]

    def check(self, id):
        def check_children(node):
            children = node.get_children()
            id_children = [node.id for node in children.keys()]
            category_children = [node.category for node in children.keys()]
            offsets = pd.Series([offset for offset in children.values()], index=id_children)
            offset_nonan = offsets.notna()
            noffset = offset_nonan.sum()
            offsets_norm = offsets - offsets.min()
            keycodes = self.sequences.loc[id_children, KEYCODE]
            dates = self.sequences.loc[id_children, DATE_BEGIN]
            date_nonan = dates.notna()
            dates_norm = dates - dates.min()
            ndate = date_nonan.sum()
            norm = dates_norm.max()+offsets_norm.max()
            diff =  dates_norm.fillna(norm) != offsets_norm.fillna(norm) 
            equal =  dates_norm.fillna(norm) == offsets_norm.fillna(norm) 
            ndiff = diff.sum()
            if node.category == MEAN:
                if (ndiff == 0) and (ndate == len(dates)) and (noffset == len(offsets)): 
                    if SET not in category_children:
                        msg = '1: dates and offsets are consistent.'
                    else:
                        msg = '-1: dates and offsets are consistent. But some children are "set".'
                elif (ndate == len(dates)) and (noffset == 0):
                    # all dates, no offset
                    if SET not in category_children:
                        msg = '2: dates are available, no offsets. Offsets update required.'
                    else:
                        msg = '-2: dates are available, no offsets. Offsets update required. But some children are "set".'
                elif (noffset == len(offsets)) and (ndate == 0):
                    # all offsets, no date
                    msg = '3: offsets are available, no dates. Undated serie.'
                elif (noffset == len(offsets)) and (equal[dates != pd.NA].sum() == ndate):
                    # all offsets, subset of dates and offsets consistent
                    if SET not in category_children:
                        msg = '4: offsets are available, some empty dates. subset of dates and offsets are consistent. Years update required.'
                    else:
                        msg = '-4: offsets are available, some empty dates. But some children are "set".'
                elif (ndate == len(dates)) and (equal[offsets != pd.NA].sum() == noffset):
                    # all offsets, subset of dates and offsets consistent
                    if SET not in category_children:
                        msg = '5: Years are available, some empty offsets. subset of dates and offsets are consistent. Offsets update required.'
                    else:
                        msg = '-5: Years are available, some empty offset. But some children are "set".'
                else:
                    if SET not in category_children:
                        msg = '-6: Years and offsets are unconsistent. Undated serie. '
                    else:
                        msg = f'-7: Contain {SET}, dates and offsets are unconsistent. Undated serie.'
            else:
                msg = f'-7: Years and offsets are unconsistent. Parent is not a {MEAN}. Correction required'
            
            info = [(node.id, self.sequences.at[node.id, KEYCODE], self.sequences.at[node.id, CATEGORY],
                          self.sequences.at[node.id, DATE_BEGIN],  pd.NA,  pd.NA , pd.NA, pd.NA)]
            info += zip(id_children, keycodes.to_list(), category_children, dates.tolist(), offsets.tolist(), 
                        dates_norm.tolist(), offsets_norm.tolist(), equal)            
            df = pd.DataFrame(info, columns=[ID, KEYCODE, CATEGORY, DATE_BEGIN, OFFSET, DATE_BEGIN_NORM, OFFSET_NORM, 'date ~ offset'])          
            return (msg, df)
        
        def get(node):
            out[node.id] = check_children(node)
            for child_node in node.children:
                if child_node.category != MEASURE:
                    get(child_node)
        
        out = {}
        tree = self.get_descendants(id)
        for child_node in tree.children:
            get(child_node)        
        return out

    def get_keycodes(self, ids, fields=None):
            """
            Generate unique keycodes for each element stored in attributes of the Sequences DataFrame.

            Args:
                ids (list): A list of indices corresponding to the elements for which keycodes need to be generated.
                fields (list, optional): A list of fields to include in the generated keycodes. Defaults to None.

            Returns:
                dict: A dictionary containing the keycodes as keys and their corresponding values.
            """
            cols = [KEYCODE, PROJECT]
            if fields is not None:
                cols += fields
            data = self.sequences.loc[ids, cols]
            if fields == None:
                if len(data) == len(data[KEYCODE].unique()):
                    return {x:y for x, y in zip(data.index, data[KEYCODE])}
                if len(data) == len(data[[PROJECT, KEYCODE]].drop_duplicates()):
                    return {x:f'{x}/{y}/{z}' for x, y, z in zip(data.index, data[PROJECT], data[KEYCODE])}
                return {x:f'{x}/{y}' for x, y in zip(data.index, data[KEYCODE])}
            else:
                return {x:f'{x}/{y}' for x, y in zip(data.index, data[fields])}

    def detrend_package(self, package_key, ring_type, window_size=5, do_log=False, date_as_offset=False, biweight=False, 
                       slope_resolution=None, cambium_estimation=None):
        
        def info(df, ids):
            message_type = 'primary'
            message = f'Detrend data is {ring_type} '
            message += ', '.join([f'{index}: {valeur}' for index, valeur in df[CATEGORY].value_counts().items()]) +'.'
            if len(ids) != len(df[ID_CHILD]):
                message += 'Duplicate series.'
            if df[INCONSISTENT].any():
                message += ' one or more series is inconsistent.'
                message_type = 'warning'

            return message_type, message

        num_threads=1
        data = self.get_package_components(package_key, slope_resolution, cambium_estimation).reset_index()
        ids = data[ID_CHILD].unique().tolist()
        if len(ids) <= 0:
            return None, 'warning', 'Detrend data is empty set'
        elif (ring_type != RAW):
            dt_data = self.detrend(ids, ring_type, window_size=window_size, do_log=do_log, date_as_offset=date_as_offset, biweight=biweight, num_threads=num_threads)
            data_cols = [DATA_LENGTH, DATA_TYPE, DATA_VALUES, DATA_WEIGHTS, DATA_INFO, DATA_SIGNATURES, INCONSISTENT]
            other_cols = data.columns.difference(data_cols)
            data = data[other_cols].join(dt_data[data_cols], on=ID_CHILD, how='left')

        message_type, message = info(data, ids)
        return data, message_type, message

    def read_buffer(self, keycode_parent, buffer, mine_type=None):
        #perror('read_buffer', mine_type)
        suffix = '.p'
        if mine_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            suffix = '.xlsx'
        elif mine_type == 'text/csv':
            suffix = '.csv'
        elif mine_type == 'application/json':
            suffix = '.json'
        output_file = Path(self.cfg_tmp) / Path(keycode_parent).with_suffix(suffix)
        with open(output_file, 'wb') as f:
            f.write(buffer)  # Récupère le contenu binaire du buffer
        
        
        self.load(output_file) 
        output_file.unlink()
        return self   

def string_to_boolean(value):
    if isinstance(value, str):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        else:
            return pd.NA
    else:
        return value
 