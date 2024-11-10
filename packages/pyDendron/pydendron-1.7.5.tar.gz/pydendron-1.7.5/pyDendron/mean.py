"""
Mean
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"


import logging
import numpy as np
import pandas as pd
try:
    from concurrent.futures import ProcessPoolExecutor
except ImportError:
    ProcessPoolExecutor = None

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.detrend import signatures

epsilon = np.finfo(np.float64).tiny
biweight_factor = 9
#biweight_factor = 5

def data2col(data, key=ID, value_key=DATA_VALUES, use_offset=True, key_offset=OFFSET, raise_error=True, add_index=False):
    
    def length_(values):
        l = len(values) if values is not None else 0
        #logger.debug(f'{l}, {values}')
        return l
    
    data = data.copy()
    #data[DATA_LENGTH] = data[value_key].apply(lambda x: length_(x))
    #print('data2col : use_offset', use_offset)
    if use_offset:
        if data[key_offset].isna().any():
            raise ValueError(f'data2col: NA value(s) in {key_offset} column')
        begin = data[key_offset].min()
        data[key_offset] -= begin
        end = (data[key_offset]+data[DATA_LENGTH]).max()
    else:
        begin = 0
        end = data[DATA_LENGTH].max()

    d = {key_offset: np.arange(begin, end+begin)} if add_index else {}
    for id, row in data.iterrows():
        offset = row[key_offset] if use_offset else 0
        if value_key == DATA_WEIGHTS:
            values = row[value_key] if (row[value_key] is not None) else np.ones(row[DATA_LENGTH])
            #perror(f'{id} / {row[KEYCODE]}, ring {values} {row[DATA_LENGTH]}')
        else:
            values = row[value_key]
        if (values is not None) and (len(values) > 0):
            vec = np.full(end, np.nan)
            vec[offset:offset+len(values)] = values
            k = id if key == ID else row[key]
            d[k] = vec
        else:
            if raise_error:
                raise ValueError(f'data2col: {id} / {row[KEYCODE]}, ring {value_key} is missing')
            else:
                if value_key != DATA_WEIGHTS:
                    logger.warning(f'data2col: {id} / {row[KEYCODE]}, ring {value_key} is missing')
        
    return pd.DataFrame(d)


def compute_mean(data, date_as_offset=False, ring_type='raw', biweight=False, id_mean=None, slope_resolution=0, min_elements=4):
    """
        sequences: DataFrame of samples. `offset` column is need if offset_type is `offset`
    """

    #print('mean', id_mean)
    if OFFSET not in data.columns:
        raise ValueError('mean: no offset in sequences')
    
    if date_as_offset:
        data[OFFSET] = data[DATE_BEGIN]

    if data[OFFSET].isna().any():
        key = DATE_BEGIN if date_as_offset else OFFSET
        raise ValueError(f'mean: one or more {key} contain NA values')
    
    if not (data[CATEGORY] == MEASURE).all():
        mask = data[CATEGORY] != MEASURE       
        if not data.loc[mask, MEANAS_MEASURE].all():
            raise ValueError('mean : data need to contain sample only')
    
    if not (data[DATA_TYPE] == ring_type).all():
        raise ValueError("mean: ring type don't match data")
        
    data_col = data2col(data)
    if biweight:
        median = data_col.median(skipna=True, axis=1)
        data_center = data_col.sub(median, axis=0)
        kind_std = data_center.abs().median(skipna=True, axis=1)
        data_center_reduce = data_center.div((biweight_factor * kind_std) + epsilon, axis=0)
        data_weights = (1 - (data_center_reduce ** 2)) ** 2
        data_weights[np.abs(data_center_reduce) >= 1] = 0
        weights = np.sum(data_weights, axis=1)
        means = np.sum(data_weights*data_col, axis=1) / weights
    else:
        means = data_col.mean(axis=1)
        weights = data_col.count(axis=1)
    
    sig = signatures(data_col, slope_resolution, min_elements)
    offsets = [(id, row[OFFSET]) for id, row in data.iterrows()]
    return np.round(means, 3).to_numpy(), weights.to_numpy(), offsets, sig, id_mean

def compute_means(data_dict, date_as_offset=False, ring_type='raw', biweight=False, num_threads=1, slope_resolution=0, min_elements=4):
    res = dict()
    #if num_threads == 1 or ProcessPoolExecutor is None:
    for id, data in data_dict.items():
        means, weights, offsets, signatures, id = compute_mean(data, date_as_offset=date_as_offset, ring_type=ring_type, biweight=biweight, id_mean=id, slope_resolution=slope_resolution, min_elements=min_elements)
        res[id] = (means, weights, offsets, signatures)
    # else:
    #     #perror(f'means multithreading: num_threads {num_threads}')
    #     with ProcessPoolExecutor(max_workers=num_threads) as executor:
    #         futures = []
    #         # Start an asynchronous task (future) for each index
    #         for id, data in data_dict.items():
    #             future = executor.submit(mean, data, date_as_offset=date_as_offset, ring_type=ring_type, biweight=biweight, id_mean=id)
    #             futures.append(future)

    #         # Wait for all tasks to be completed
    #         for future in futures:
    #             means, weights, offsets, id = future.result()
    #             res[id] = (means, weights, offsets)
    return res

