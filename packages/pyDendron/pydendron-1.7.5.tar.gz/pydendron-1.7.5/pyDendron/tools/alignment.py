"""
    Import Validation / check data consistency
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import numpy as np

from difflib import ndiff
import time

from pyDendron.dataname import *

import panel as pn
from panel.viewable import Viewer
import param

class Alignment(Viewer):
    rate = param.Integer(default=0, doc='number of computed results')

    @classmethod
    def _distance_levenshtein(cls, vector1, vector2):
        """Calculate the Levenshtein distance between two vectors."""
        len_s1, len_s2 = len(vector1), len(vector2)

        matrix = np.zeros((len_s1 + 1, len_s2 + 1), dtype=int)
        matrix[:, 0] = np.arange(len_s1 + 1)
        matrix[0, :] = np.arange(len_s2 + 1)

        for i in range(1, len_s1 + 1):
            for j in range(1, len_s2 + 1):
                cost = 0 if vector1[i - 1] == vector2[j - 1] else 1
                matrix[i, j] = min(matrix[i - 1, j] + 1,      # Deletion
                                   matrix[i, j - 1] + 1,      # Insertion
                                   matrix[i - 1, j - 1] + cost  # Substitution
                                )

        return matrix[len_s1, len_s2], max(len_s1/10, len_s2/10)
    
    @classmethod    
    def levenshtein_sequences(cls, data):
        """Compare data using Levenshtein distance and write results to a file."""
        data = []
        values = [(id, row[DATA_VALUES]) for id, row in data.iterrows()]
        start_t = time.time()
        
        with open('indices_levenshtein.txt', 'w') as fic:
            for i, (id_i, value_i) in enumerate(values[:-1]):
                if id_i < 70: 
                    continue
                current_time = time.time()
                #logger.debug(f'i, id_i:  {i}, {id_i}, {current_time-start_t}')
                start_t = current_time
                
                for j, (id_j, value_j) in enumerate(values[i+1:]):
                    dist, threshold = cls._distance_levenshtein(value_i, value_j)
                    if dist < threshold:
                        #logger.debug(f'{id_i}, {id_j}, {dist}')
                        data.append([id_i, id_j, dist])
                        fic.write(f'{id_i}, {id_j}, {dist}')

        return data
    
    def ndiff_sequences(self, data, n=5):
        def _cost(diff):
            insertions = sum(1 for line in diff if line.startswith('+'))
            deletions = sum(1 for line in diff if line.startswith('-'))
            substitutions = sum(1 for line in diff if line.startswith('?'))
            cost = insertions + deletions + substitutions
            return cost, insertions, deletions, substitutions
        
        def _ndiff(v0_utf8, v1_utf8, threshold):
            d = np.abs(len(v0_utf8) - len(v1_utf8))
            if d > threshold:
                return d, d, 0, 0, threshold
            return _cost(list(ndiff(v0_utf8, v1_utf8)))

        values = []   
        for id, row in data.iterrows():
            try:
                vec = [chr(x) for x in np.nan_to_num(row[DATA_VALUES] + 1).astype(int)]
                values.append([id, vec, len(vec), row[KEYCODE]])
            except:
                pass
            
        results = []
        values = sorted(values, key=lambda x: x[2])
        for i, (id_i, str_i, len_i, keycode_i) in enumerate(values[:-1]):
            self.rate = (i * 100) // (len(values) - 1)
            results1 = []
            for j, (id_j, str_j, len_j, keycode_j) in enumerate(values[i+1:]):
                if len_j > len_i + n:
                    break
                cost , insertions, deletions, substitutions = _ndiff(str_i, str_j, n)
                if cost < n:
                    if cost == 0:
                        ch = f'"{keycode_i}" and "{keycode_j}" are equal.'
                    else:
                        ch = f'"{keycode_i}" and "{keycode_j}" are equal to within {cost} values.'
                    #print(ch)
                    results1.append([id_i, id_j, cost , insertions, deletions, substitutions, n, ch])
            results.extend(results1)   
        return results

