"""
ComponentsTree class
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"




import logging

import pandas as pd
import numpy as np
import param

from collections import Counter
from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *

class ComponentsNode():
    def __init__(self, parent, id, keycode, category, offset, depth=0):
        self.id = id
        self.keycode = keycode
        self.parent = parent
        self.category = category
        self.offset = offset
        self.depth = depth
        self.descendants = {MEASURE:{}, MEAN:{}, SET:{}}
        if category in CATEGORIES:
            self.descendants[category][self] = self.offset
        self.children = []

    def append(self, node):
        self.children.append(node)
        for category in node.descendants:
            for child, offset in node.descendants[category].items():
                self.descendants[category][child] = self.offset + offset
        
    def get_children(self, current=False, max_depth=None):
        if max_depth is not None: 
            d = {node: node.offset+self.offset for node in self.children if node.depth <= max_depth}
        d = {node: node.offset+self.offset for node in self.children}
        if current:
            d[self] = self.offset
        return d

    def filter(self, categories=None, max_depth=pd.NA):
        def _descendants(category, depth):
            if pd.notna(max_depth): 
                return {node: offset for node, offset in self.descendants[category].items() if (node.depth-self.depth) <= depth}
            return self.descendants[category]
        
        d = {}
        if categories is None:
            categories = CATEGORIES
        for category in categories:
            d.update(_descendants(category, max_depth))
        return d

    def count_descendants(self, category=None):
        def count_category(category):
            lst = [node.id for node in self.descendants[category].keys()]
            keycodes = {node.id: node.keycode for node in self.descendants[category].keys()}
            cpt = Counter(lst)
            return cpt
        
        if category is not None:
            return count_category(category)
        else:
            l = {}
            for category in CATEGORIES:
                l.update(count_category(category))
            return l


    def detect_duplicates(self, category=None, raise_error=True):
        def duplicates(category, raise_error):
            lst = [node.id for node in self.descendants[category].keys()]
            keycodes = {node.id: node.keycode for node in self.descendants[category].keys()}
            if len(lst) != len(set(lst)):
                cpt = Counter(lst)
                dup = [(element, keycodes[element]) for element, count in cpt.items() if count > 1]
                if raise_error:
                    raise ValueError(f'detect_duplicates: duplicate samples : {dup}')
                return dup
            return []
        
        if category is not None:
            return duplicates(category, raise_error)
        else:
            l = []
            for category in CATEGORIES:
                l += duplicates(category, raise_error)
            return l

    def find(self, ids, depth=pd.NA):
        l = []
        sids = set(ids)
        for node in self.children + [self]:
            if node.id in sids:
                l.append(node.id)
        return l

    def print(self, descendants=False):
        print('\t'*self.depth, f'id: {self.id}, category: {self.category}, offset: {self.offset}, depth: {self.depth}') 
        if descendants : 
            print('\t'*self.depth,self.descendants)
        for n in self.children:
            n.print()

class ComponentsTree(ComponentsNode):
    def __init__(self):
        super(ComponentsTree, self).__init__(None, -1, 'Root', 'TreeNode', 0)   

    def stats(self):
        return pd.DataFrame([{
        'roots' : len(self.get_mean_ids(0)),
        'chonologies' : len(self.get_mean_ids()),
        'set' : len(self.get_set_ids()),
        'samples' : len(self.get_samples()),
        'duplicated chonologies' : len(self.detect_duplicated_means(raise_error=False)),
        'duplicated samples' : len(self.detect_duplicated_samples(raise_error=False))
        }])

    