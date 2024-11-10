""" I/O for Dendron IV format """

__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"
import glob
import logging
import copy
import re
from lxml import etree as ET
import numpy as np
import pandas as pd
import pickle
import zipfile
import os
import shutil

from pyDendron.tools.location import reverse_geocode, get_elevation
from pyDendron.dataset import Dataset
from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pathlib import Path

class IODendronIV:
    """
    Represents a DendronIV object.

    Args:
        glob_str (str): The glob string used to search for files.
        source (str): The source of the data.
        laboratories (str): The laboratories associated with the data.
        places (str): The filename of the places file.
        get_place (bool): Flag indicating whether to get place information.
        get_altitude (bool): Flag indicating whether to get altitude information.

    Attributes:
        glob_str (str): The glob string used to search for files.
        uri (str): The URI of the file.
        filename (str): The filename.
        source (str): The source of the data.
        id (int): The index.
        ids (dict): A dictionary containing the indexes.
        sequences (list): A list of sequences.
        components (list): A list of components.
        get_place (bool): Flag indicating whether to get place information.
        get_altitude (bool): Flag indicating whether to get altitude information.
        reverses_location (dict): A dictionary containing reverse locations.
        elevations (dict): A dictionary containing elevations.
        laboratories (str): The laboratories associated with the data.
        places_fn (str): The filename of the places file.
        projects (dict): A dictionary containing the projects.

    Methods:
        _read_places(): Reads the places file.
        _write_places(): Writes the places file.
        _readall(): Reads all the data.
        get_components(seqs, card_dict): Retrieves the components from the given sequences and card dictionary.
        read_begin_table(root): Reads the begin table.
        _add_project(seqs, card_dict): Adds a project.
        _read_cards(root, card_dict): Reads the cards.
        _read_card(card, card_dict): Reads a card.
        _read_field(field, meta): Reads a field.
    """
    file_extension = ['.Dxml']
    
    def __init__(self, source=None, laboratories=None, base_directory='./', places='reverse_places.p', get_place=False, get_altitude=False):
        self.glob_str = '*'+IODendronIV.file_extension[0]
        self.uri = None
        self.filename = None
        self.source = source
        self.id = 0
        self.ids = {}
        self.sequences = []
        self.components = []
        self.get_place = get_place
        self.get_altitude = get_altitude
        self.reverses_location = {}
        self.elevations = {}
        self.laboratories = laboratories
        self.places_fn = places
        self.projects = {}
        self.base_directory = Path(base_directory)
        self.dataset = None

        #self._readall()

    def _read_places(self):
        """
        Reads the places file.
        """
        if (self.places_fn is not None) and Path(self.places_fn).exists():
            with open(self.places_fn , 'rb') as fic:
                self.reverses_location, self.elevations = pickle.load(fic)

    def _write_places(self):
        """
        Writes the places file.
        """
        with open(self.places_fn , 'wb') as fic:
            pickle.dump([self.reverses_location, self.elevations], fic)

    def _readall(self):
        """
        Reads all the data.
        """
        self._read_places()

        #lst = [x for x in glob.glob(self.glob_str, recursive=True)]
        lst = list(self.base_directory.rglob(self.glob_str))
        if len(lst) == 0:
            logger.error(f'No files found with {self.glob_str} in {self.base_directory}')
            return 
        #perror(f"self.base_directory: {self.base_directory}")
        #perror(f"self.glob_str: {self.glob_str}")
        #perror(f"lst: {lst}")
        card_dict = {}
        seqs = {}
        for i, self.filename in enumerate(lst):
            if self.filename.name.startswith('.'):
                continue
            #perror(f"filename: {self.filename}")
            self.uri = Path(self.filename).resolve().as_uri()
            if (i % 25) == 0:
                #logger.debug('_write_places')
                self._write_places()
            with open(self.filename, 'r', encoding='ISO-8859-1') as file:
                    data = file.read()
                    data = data.replace('&', '&amp;')
                    try:
                        root = ET.fromstring(data)
                    except Exception as inst:
                        #perror(f'XML error in {self.filename} {inst} ')
                        logging.warning(f'XML error in {self.filename} {inst} ')
                        root = ET.fromstring(data, ET.XMLParser(recover=True))
                    card_dict.update(self.read_begin_table(root))
                    fn_seqs = self._read_cards(root, card_dict)
                    #for key in fn_seqs:
                    #    perror(f"key: {key} {fn_seqs[key]}")
                    seqs.update(fn_seqs)

        diff =  set(card_dict.values()) - set(seqs.keys())
        if len(diff) > 0:
            logging.warning(f'\t missing sequences  {diff}')

        self.sequences = list(seqs.values())
        self.components = self.get_components(seqs, card_dict)
        self._write_places()

    def get_components(self, seqs, card_dict):
        """
        Retrieves the components from the given sequences and card dictionary.

        Args:
            seqs (dict): A dictionary containing the sequences.
            card_dict (dict): A dictionary containing the card information.

        Returns:
            list: A list of dictionaries representing the components.

        Raises:
            None

        """
        components = []
        for id_parent in seqs:
            meta = seqs[id_parent]
            if CATEGORY not in meta:
                logging.warning(f'\t undefined category for {meta[KEYCODE]}')
            elif (meta[CATEGORY] != MEASURE) and ('comps' in meta):
                tmp = []
                for comp in meta['comps']:
                    if comp in card_dict:
                        id_child = card_dict[comp]
                        if id_child != id_parent:
                            if id_child not in seqs:
                                logging.warning(f'\t remove missing sequences {id_child} in {id_parent}')
                            else:
                                offset = 0
                                if DATE_BEGIN in seqs[id_child]:
                                    offset = seqs[id_child][DATE_BEGIN]
                                    if pd.notna(offset) and (offset > 3000):
                                        ('Offset', offset)
                                        offset -= 3000
                                        seqs[id_child][DATE_BEGIN] = pd.NA
                                        seqs[id_child][DATE_END] = pd.NA

                                tmp.append({ID_PARENT:id_parent, ID_CHILD:id_child, OFFSET:offset})
                if len(tmp) == 0:
                    logging.warning(f"empty set {id_parent} {meta[KEYCODE]} ({meta[CATEGORY]})")
                components += tmp
        return components

    def read_begin_table(self, root):
        """
        Reads the begin table.

        Args:
            root (Element): The root element.

        Returns:
            dict: A dictionary containing the card information.

        Raises:
            None

        """
        card_dict = {}
        data = root.find('FirstTable/text').text
        for line in data.split('\n'):
            line = line.strip()
            fields = line.split()
            if (len(fields) == 4) and (fields[3] == 'Ok'):
                if fields[0] in card_dict:
                    logging.warning(f'\t duplicate card: {fields[0]}')
                card_dict[fields[0]] = self.id
                self.id += 1
        #print('card_dict', card_dict)
        return card_dict

    def _add_project(self, seqs, card_dict):
        """
        Adds a project.

        Args:
            seqs (dict): A dictionary containing the sequences.
            card_dict (dict): A dictionary containing the card information.

        Returns:
            tuple: A tuple containing the project and the components.

        Raises:
            None

        """
        fn = Path(self.filename)
        #project = fn.parent.name
        #perror(f"base_directory: {self.base_directory}")
        #perror(f"fn: {fn}")
        #perror(f"relative path: {fn.relative_to(self.base_directory)}")
        #perror(f"relative path parent: {fn.relative_to(self.base_directory).parent} {fn.relative_to(self.base_directory)}")
        project = fn.relative_to(self.base_directory).parent
        
        if project in self.projects:
            return project, self.projects[project]['comps']
        else:
            file_id = self.id
            meta = {ID: file_id, 
                    KEYCODE: project, 
                    PROJECT: project, 
                    #URI: self.filename,
                    CATEGORY: SET,
                    'comps': {} 
                    }
            seqs[file_id] = meta
            card_dict[file_id] = file_id
            self.id += 1
            self.projects[project] = meta
            return project, meta['comps']

    def _read_cards(self, root, card_dict):
        """
        Reads the cards.

        Args:
            root (Element): The root element.
            card_dict (dict): A dictionary containing the card information.

        Returns:
            dict: A dictionary containing the sequences.

        Raises:
            None

        """
        seqs = {}
        project, comps = self._add_project(seqs, card_dict)

        for card in root.findall("Card"):
            meta, key = self._read_card(card, card_dict)
            #print('meta', meta)
            if meta is not None:
                if meta[ID] in seqs:
                    logging.warning(f'\t duplicate sequences: {key} / {meta[KEYCODE]}')
                else:
                    meta[PROJECT] = project
                    meta[URI] = self.filename
                    seqs[meta[ID]] = meta
                    comps[meta['cardName']] = 'head'
        return seqs

    def _read_card(self, card, card_dict):
        """
        Reads a card.

        Args:
            card (Element): The card element.
            card_dict (dict): A dictionary containing the card information.

        Returns:
            tuple: A tuple containing the metadata and the card name.

        Raises:
            None

        """
        #print("-"*10)
        meta = {}
        card_name = card.find('name').text.strip()
        if card_name == '000_A':
            return None, None
        if card_name not in card_dict:
            logging.warning(f'\t Card not in list {card_name}')
            return None, None
        meta['cardName'] = card_name
        user_name = card.find('userName').text.strip()
        meta[ID] = card_dict[card_name]
        meta[KEYCODE] = user_name
        for field in card.findall("field"):
            self._read_field(field, meta)

        return meta, card_name

    def _read_field(self, field, meta):
        """
        Reads a field.

        Args:
            field (Element): The field element.
            meta (dict): A dictionary containing the metadata.

        Returns:
            None

        Raises:
            None

        """
        def _read_category():
            if text.startswith('indiv'):
                meta[CATEGORY] = MEASURE
            elif text.startswith('group'):
                meta[CATEGORY] = SET
            else:
                logging.warning(f'\t Unknown card type |{text}| {name}')
                meta[CATEGORY] = MEASURE

        def _read_values():
            values = []
            #perror(f"field.text: {text}")
            for line in text.split('\n'):
                line = line.strip()
                if line != '':
                    try:
                        values.append(float(line))
                    except Exception as inst:
                        logging.warning(f'\t* values error: |{line}|')
                else:
                    values.append(np.nan)
            
            #perror(f"values: {values}")
            
            if len(values) > 0:
                meta[DATA_VALUES] = np.array(values)
                meta[DATA_LENGTH] = len(values)
                meta[DATA_TYPE] = RAW
                if (CATEGORY in meta) and (meta[CATEGORY] == SET):
                    meta[CATEGORY] = MEAN

        def _read_location():
            f = text.split()
            try:
                meta[SITE_LATITUDE] = float(f[1])
                meta[SITE_LONGITUDE] = float(f[0])
            except Exception as inst:
                meta[SITE_LATITUDE] = pd.NA
                meta[SITE_LONGITUDE] = pd.NA
            meta[SITE_ELEVATION] = pd.NA
            meta[SITE_CODE] = ''
            if self.get_place:
                _, __, ___, ____, _____, meta[SITE_CODE] = reverse_geocode(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.reverses_location)
            if self.get_altitude: 
                meta[SITE_ELEVATION] = get_elevation(meta[SITE_LATITUDE], meta[SITE_LONGITUDE], self.elevations)

        def _read_working_list():
            #f = text.split()
            comps = {}
            for line in text.split('\n'):
                line = line.strip()
                f = line.split()
                if len(f) == 5:
                    comps[f[1]] = f
            meta['comps'] = comps

        name = field.find('name').text.strip()
        text = field.find('text').text.strip()

        if name == 'card type':
            _read_category()
        elif name == 'i_01':
            _read_values()
        elif name =='sample':
            v = text.split('\n')
            if len(v) > 3:
                if v[0] == '1':
                    meta[PITH] = True
                i = re.search(r'\d+', v[1])
                if i:
                    meta[SAPWOOD] = int(i.group()) - 1
                if v[2] == '1':
                    meta[CAMBIUM] = True
        elif (name == 'material') and (text != ''):
            meta[SUBCATEGORY] = text
        elif (name == 'creation date') and (text != ''):
            try:
                meta[CREATION_DATE] = pd.to_datetime(text, format="%Y%m%d")
            except Exception as inst:
                meta[CREATION_DATE] = ''
        elif (name == 'start date') and (text != ''):
            meta[DATE_BEGIN] = float(text)
        elif (name == 'stop date') and (text != ''):
            meta[DATE_END] = float(text)
        elif (name == 'location') and (text != ''):
            _read_location()
        elif (name == 'tree type') and (text != ''):
            meta[SPECIES] = text
        elif name == 'working list':
            _read_working_list()
        elif name == 'waiting list':
            if text != '':
                meta[DATA_INFO] = text
        elif name == 'comments':
            if text != '':
                meta[COMMENTS] = text
        elif name == 'labs authors':
            if text != '':
                meta[LABORATORY_CODE] = text
        elif name == 'people authors':
            if text != '':
                meta[PERS_ID] = text
        elif name == 'references':
            if text != '':
                meta[BIBLIOGRAPHY_CODE] = text
        elif name == 'source file':
            if text != '':
                meta[URI] = text
                    
    def to_dataset(self, keycode_parent='Dataset', root_id=ROOT, trash_keycode='Trash', workshop_keycode='Workshop', clipboard_keycode='Clipboard'):
        """
        Converts the current state of the object to a Dataset object.

        Args:
            keycode_parent (str): The keycode for the root node of the dataset. Default is 'Dataset'.
            root_id (int): The index of the root node. Default is ROOT.
            trash_keycode (str): The keycode for the trash node of the dataset. Default is 'Trash'.
            workshop_keycode (str): The keycode for the workshop node of the dataset. Default is 'Workshop'.
            clipboard_keycode (str): The keycode for the clipboard node of the dataset. Default is 'Clipboard'.

        Returns:
            Dataset: The converted Dataset object.
        """
        if len(self.sequences) == 0:
            return None
        
        self.dataset = Dataset(sequences=self.sequences, components=self.components, save_auto=False)

        for k, t in sequences_dtype_dict.items():
            if k not in self.dataset.sequences.columns:
                self.dataset.sequences[k] = ''
            if t == 'string':
                self.dataset.sequences[k] = self.dataset.sequences[k].fillna('')

        self.dataset.sequences[INCONSISTENT] = False
        self.dataset.sequences[SPECIES] = self.dataset.sequences[SPECIES].str.upper()
        mask = self.dataset.sequences[SPECIES].str.startswith('QU')
        self.dataset.sequences.loc[mask, SPECIES] = 'QU'

        logger.info(f'to_dataset roots: {self.dataset.get_roots()}')
        self.dataset.new_root(keycode_parent, root_id)
        self.dataset.new_clipboard(clipboard_keycode)
        self.dataset.new_trash(trash_keycode)
        self.dataset.new_workshop(workshop_keycode)

        return self.dataset
    
    def compact(self, drop_duplicate=False, mean_to_set=False):
        """
        Remove duplicate samples in the tree and keep deeper nodes.
        Parent categories are set to SET and RING_* are set empty.

        Parameters:
        - drop (bool): If True, remove the duplicate samples from the dataset. Default is False.

        Returns:
        - dataset: The modified dataset after removing duplicate samples.
        """
        def iterate(node):
            dup = [x for (x, y) in node.detect_duplicates(category=MEASURE, raise_error=False)]
            for child in node.children:
                if child.category != MEASURE:
                    iterate(child)
                else:
                    if child.id in dup:
                        remove_list.append((node.id, child.id))
                        mean_id_list.append(node.id)

        if self.dataset is None:
            return None
        
        if drop_duplicate:
            tree = self.dataset.get_descendants(self.dataset.get_roots())
            remove_list = []
            mean_id_list = []
            iterate(tree)
            #logger.info(f'compact remove_list: {remove_list}')
            self.dataset.components.drop(remove_list, inplace=True)
            
        if mean_to_set:
            mask = self.dataset.sequences.index.isin(set(mean_id_list))
            cols = [CATEGORY, DATA_LENGTH, DATA_INFO, DATA_TYPE, DATA_WEIGHTS, DATA_VALUES]
            self.dataset.sequences.loc[mask, cols] = SET, pd.NA, pd.NA, pd.NA, pd.NA, pd.NA

        return self.dataset
    
    def project_to_set(self, id_root=ROOT):
        def create_set(path, project_sets):
            id_parent = [id_root]
            #perror(f"path: {path}")
            for p in path.parts:
                #perror(f" p: {p}")
                if p not in project_sets:
                    self.id += 1
                    #perror(f"   new p: {p} {id_parent[-1]} {self.id}")
                    self.dataset.new(keycode=p, category=SET, id_parent=id_parent[-1], id=self.id)
                    id_parent.append(self.id)
                    project_sets[p] = copy.copy(id_parent)
                else:
                    id_parent = copy.copy(project_sets[p])
                    #perror(f"   get p: {p} {id_parent[-1]}")
            return id_parent
        
        if self.dataset is None:
            return None

        project_sets = {}
        for project, df in self.dataset.sequences.groupby(PROJECT):
            path = Path(project)
            last_project = create_set(path, project_sets)
            child_mask = self.dataset.components.index.get_level_values(ID_CHILD).isin(df.index)
            root_mask = self.dataset.components.index.get_level_values(ID_PARENT).isin([id_root])
            comps = self.dataset.components[child_mask & root_mask]
            #perror(f"last_project: {path} {last_project} {len(comps)}")
            #perror(f"comps.to_records: {comps.to_records(index=True)}")
            self.dataset.move(comps.to_records(index=True), last_project)
            
            
    
    def read(self, directory, keycode_parent='Dendron-IV'):
        self.base_directory = Path(directory)
        if not  self.base_directory.is_dir():
            raise ValueError(f'{ self.base_directory} is not a directory')
        #self.glob_str = '*.Dxml'
        
        #root_keycode = self.base_directory.parts[-1]
        self._readall()
        self.to_dataset(keycode_parent=keycode_parent)
        
        self.compact(drop_duplicate=True, mean_to_set=True)
        self.project_to_set()
        
        return self.dataset

    def read_buffer(self, keycode_parent, buffer, mine_type=None):
        if mine_type != 'application/zip':
            raise ValueError(f'Unsupported mine_type {mine_type}')
        
        output_directory = Path(self.base_directory) / keycode_parent
        os.makedirs(output_directory, exist_ok=True)
        
        output_file = output_directory / Path(keycode_parent).with_suffix(".zip")
        with open(output_file, 'wb') as f:
            f.write(buffer)  

        zip = zipfile.ZipFile(output_file)
        zip.extractall(output_directory)
        
        dataset = self.read(output_directory, keycode_parent=keycode_parent) 
        shutil.rmtree(output_directory)
        return dataset             
