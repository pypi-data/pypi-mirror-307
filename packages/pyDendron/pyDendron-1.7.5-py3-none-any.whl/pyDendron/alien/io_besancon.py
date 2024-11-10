""" I/O for Besançon format """

__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

from pathlib import Path
import pandas as pd
import numpy as np
import io

from pyDendron.dataname import *
from pyDendron.alien.io import IO
from pyDendron.dataset import Dataset
from pyDendron.app_logger import logger, perror

class IOBesancon(IO):
    SPECIES_MAPPING = {
        'Q': 'QU',
        'QU': 'QU',
        'CHENE': 'QU'
    }
    file_extension = ['.txt', '.bes', '.ne']
    
    def read_properties(self, buffer, meta):
        def species(word):
            return self.SPECIES_MAPPING.get(word, word)
            #if word in ['Q', 'QU', 'CHENE']:
            #    return 'QU';
            #else:
            #    return word
    
        def pith(word):
            return True
        
        def cambium(word): 
            return True if word == 'OUI' else False
        
        def integer_(word):
            return int(word)

        prop = {
            'ESP': (species, SPECIES), 
            #'MOE': (pith, PITH), 
            #'CAM': (cambium, CAMBIUM), 
            'POS': (integer_, OFFSET), 
            'ORI': (integer_, DATE_BEGIN), 
            'TER': (integer_, DATE_END), 
            #'MXTER': (integer_, DATE_END_ESTIMATED), 
            'AUB': (integer_, SAPWOOD)
        }
        meta[OFFSET] = pd.NA
        meta[CATEGORY] = MEASURE
        
        words = buffer.upper().split() + ['UNK']
        for i, word in enumerate(words):
            for key, (fct, k) in prop.items():
                if word.startswith(key):
                    meta[k] = fct(words[i+1])
                    key_found = True

        if meta[DATE_BEGIN] < 0: meta[DATE_BEGIN] += 1
        if meta[DATE_END] > 0: meta[DATE_END] += 1
                    
    def read_values(self, buffer, meta):
        words = buffer.upper().replace(';', '').split()   
        values = [int(word) if word not in [',', '!', '?', '*', '/'] else np.nan for word in words]
        #values = [] 
        #for word in words:
        #    if word not in[',', '!', '?', '*', '/', ';']:
        #        values.append(int(word))
        #    elif word == ',':
        #        values.append(np.nan)
        meta[DATA_VALUES] = np.array(values, dtype='float')
        meta[DATA_LENGTH] = len(np.array(values))
        
    
    def read_comps(self, buffer, meta, id_comps):
        lines = buffer.upper().split('\n')   
        for line in lines:
            c, keycode, offset = line.split()
            if keycode in id_comps:
                meta[id_comps[keycode]] = offset
            else:
                raise ValueError(f'{keycode} sequence is not in the file')
    
    def read_sequences(self, id_parent, lines):
        meta = {}
        state = 'start'
        buffer = ''
        id_comps = {}
        for line in lines:
            if line[0] == '.': # new sequences
                if state == 'value':
                    self.read_values(buffer, meta)
                elif state == 'comp':
                    self.read_comps(buffer, meta, id_comps)             
                if state != 'start':
                    self.components.append({ID_PARENT: id_parent, ID_CHILD: meta[ID], OFFSET: meta[OFFSET]})
                    del meta[OFFSET]
                    self.sequences.append(meta)

                meta = {ID: self.next_id()}
                meta[KEYCODE] = line.split()[1]
                id_comps[meta[KEYCODE]] = meta[ID]
                state = 'seq'
                buffer = ''
            elif line[0] == 'V': # new values
                if state != 'seq':
                    raise ValueError('inconsistent state: {state}')
                self.read_properties(buffer, meta)
                state = 'value'          
                ring_type = line.split()[1].upper()
                if not ring_type.startswith('NAT'):
                    logger.warning(f'{DATA_TYPE} is not raw')
                    meta[DATA_TYPE] = ring_type
                else:
                    meta[DATA_TYPE] = RAW
                buffer = ''
            elif line[0] == 'C': # new composent
                if state != 'value':
                    raise ValueError('inconsistent state: {state}')
                state = 'comp'
                self.read_values(buffer, meta)
                buffer = ''
            elif line[0] == ':': # end
                if state not in  ['value', 'comp']:
                    raise ValueError('inconsistent state: {state}')
                state = 'end'                
                break
            else:
                buffer += line
                
        if state != 'end':
            if state == 'value':
                self.read_values(buffer, meta)
            elif state == 'comp':
                self.read_comps(buffer, meta, id_comps)             
            self.components.append({ID_PARENT: id_parent, ID_CHILD: meta[ID], OFFSET:meta[OFFSET]})
            del meta[OFFSET]
            self.sequences.append(meta)
            

    def write_file(self, data: pd.DataFrame, means, filename: str):
        with open(Path(filename), mode='w', encoding=self.encoding, errors='ignore') as fd:
            for i, row in data.iterrows():
                if row[CATEGORY] in [MEASURE, MEAN]:
                    fd.write(f'. {row[KEYCODE].replace(" ", "_")}\n')
                    if pd.notna(row[DATA_LENGTH]):
                        fd.write(f'\tLON {row[DATA_LENGTH]}\n')
                    if pd.notna(row[OFFSET]):
                        fd.write(f'\tPOS {row[OFFSET]}\n')
                    if pd.notna(row[DATE_BEGIN]):
                        fd.write(f'\tORI {int(row[DATE_BEGIN])}\n')
                    if pd.notna(row[DATE_END]):
                        fd.write(f'\tTER {int(row[DATE_END])}\n')
                    
                    if row[CATEGORY] == MEASURE:
                        if row[SPECIES] != '':
                            fd.write(f'\tESP {row[SPECIES].replace(" ", "_")}\n')
                        #if pd.notna(row[DATE_END_ESTIMATED]):
                        #    fd.write(f'\tMXTER {int(row[DATE_END_ESTIMATED])}\n')
                        if pd.notna(row[SAPWOOD]):
                            fd.write(f'\tAUB {int(row[SAPWOOD])}\n')
                        if pd.notna(row[PITH]) and row[PITH]:
                            fd.write('\tMOE oui\n')
                        if pd.notna(row[CAMBIUM]) and row[CAMBIUM]:
                            fd.write('\tCAM oui\n')
                    
                    if row[DATA_VALUES] is not None:
                        fd.write(f'VALeurs {row[DATA_TYPE]}\n')
                        tmp = np.round(np.nan_to_num(row[DATA_VALUES], nan=-9999), 0).astype(int).tolist()
                        
                        #tmp = np.nan_to_num(row[DATA_VALUES], nan=-9999).astype(int)
                        tmp = np.array_split(tmp, len(tmp) // 10 + 1)
                        for i, line in enumerate(tmp):
                            lst = [',' if x == -9999 else str(x) for x in line.tolist() ]
                            s = ' '.join(lst)
                            s += ' ;\n' if i + 1 == len(tmp) else '\n'
                            fd.write(s)

                    if row[CATEGORY] == MEAN:
                        fd.write(f'Composante {row[KEYCODE].replace(" ", "_")}\n')
                        for keycode, offset in means[row[ID_CHILD]]:
                            fd.write(f'C    {keycode.replace(" ", "_")}    offset\n')
                    fd.write('\n') 
                    
            

    
    
    
    
