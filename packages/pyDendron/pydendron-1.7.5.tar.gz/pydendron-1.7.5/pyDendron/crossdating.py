
"""
    Crossdating module
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
 

try:
    from concurrent.futures import ProcessPoolExecutor
except:
    ProcessPoolExecutor = None
    
import time
import warnings
import os
import copy
import sys
import numba
import math

from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import networkx as nx
import seaborn as sns
from scipy import stats, spatial
from scipy.stats import gaussian_kde
from sklearn.neighbors import KernelDensity

import param
import panel as pn
from bokeh.palettes import RdYlBu9, Category20, Category10
from bokeh.palettes import Blues256, Reds256, Turbo256
from bokeh.plotting import figure
from bokeh.models import (PrintfTickFormatter, RangeTool, ColumnDataSource, Range1d,
                            Legend, LegendItem, Label, FixedTicker) 
from bokeh.transform import factor_mark 
from bokeh.palettes import brewer 
from bokeh.layouts import gridplot
from bokeh.events import DoubleTap
import xyzservices.providers as xyz

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *

COLS_R = {CORR_OVERLAP: 'Int32', CORR_OVERLAP_NAN: 'Int32', CORR: 'float32', 
          T_SCORE: 'float32', TP_VALUE: 'float32', T_RANK: 'Int32'}

COLS_GLK = {GLK_OVERLAP: 'Int32', GLK_OVERLAP_NAN: 'Int32', GLK: 'float32', 
            Z_SCORE: 'float32', ZP_VALUE: 'float32', Z_RANK: 'Int32'}

COLS_D = {DIST_OVERLAP: 'Int32', DIST_OVERLAP_NAN: 'Int32', DISTANCE: 'float32', D_RANK: 'Int32'}

COLS_BASE = {ID_MASTER: 'Int32', ID: 'Int32', 
        KEYCODE_MASTER: 'string', KEYCODE: 'string', 
        DATA_TYPE: 'string', 
        OFFSET: 'Int32', DATE_BEGIN_ESTIMATED: 'Int32', DATE_END_ESTIMATED: 'Int32', SYNC: 'boolean', 
        }

COLS = {**COLS_BASE, **COLS_R, **COLS_GLK, **COLS_D}

(RES_ID_MASTER, RES_ID, 
RES_KEYCODE_MASTER, RES_KEYCODE, RES_DATA_TYPE, 
RES_OFFSET, RES_DATE_BEGIN_ESTIMATED, RES_DATE_END_ESTIMATED, 
RES_SYNC, 
RES_CORR_OVERLAP, RES_CORR_OVERLAP_NAN, RES_CORR, RES_T_SCORE, RES_TP_VALUE, RES_T_RANK, 
RES_GLK_OVERLAP, RES_GLK_OVERLAP_NAN, RES_GLK, RES_Z_SCORE, RES_ZP_VALUE, RES_Z_RANK, 
RES_DIST_OVERLAP, RES_DIST_OVERLAP_NAN, RES_DIST, RES_D_RANK) = range(25) 

DEFAULTS = [pd.NA, pd.NA, 
            '', '', '', 
            pd.NA, pd.NA, pd.NA, 
            '', 
            pd.NA, pd.NA, -np.inf, -np.inf, -np.inf, -1,
            pd.NA, pd.NA, -np.inf, -np.inf, -np.inf, -1,
            pd.NA, pd.NA, -np.inf, -1]

class MapValueError(ValueError):
    # Initialize the exception with a custom message
    def __init__(self, message):
        # Call the base class constructor with the custom message
        super().__init__(message)

def start_profiler():
        import cProfile
        cp = cProfile.Profile()
        cp.enable()
        return cp
        
def stop_profiler(cp):
    import cProfile, pstats, io
    from pstats import SortKey
    cp.disable()
    s = io.StringIO()
    sortby = SortKey.CUMULATIVE
    ps = pstats.Stats(cp, stream=s).sort_stats(sortby)
    ps.print_stats()
    #logger.info(s.getvalue())

def worker_it(instance, row, master_data):
    return instance.run_it(row, master_data)

#@numba.jit(nopython=True, fastmath=True, cache=True)
def seg_validatation(seg_x, seg_y):
    valid_data_points = (~np.isnan(seg_x)) & (~np.isnan(seg_y))
    n = np.sum(valid_data_points)
    nnan =  valid_data_points.size - n # number of nan
    x, y = seg_x[valid_data_points], seg_y[valid_data_points]
    
    return n, nnan, x, y

@numba.jit(nopython=True, fastmath=True, cache=True)
def r(n, x, y):
    xn = x - np.mean(x)
    yn = y - np.mean(y)
    d = (np.linalg.norm(xn) * np.linalg.norm(yn))
    if d == 0:
        return -np.inf, -np.inf, 0
    r = np.dot(xn, yn) / d
    # Wikipedia : https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    # For pairs from an uncorrelated bivariate normal distribution, the sampling distribution of the studentized 
    # Pearson's correlation coefficient follows Student's t-distribution with degrees of freedom n − 2. 

    if r >= 0.9999:
        r = 0.9999
        t_score = np.inf
    elif r <= -0.9999:
        r = -0.9999
        t_score = -np.inf
    else:
        t_score = r * np.sqrt((n - 2) / (1.0 - r ** 2))  # Calculate t-score
    return r, t_score, 0

#@numba.jit(nopython=True, fastmath=True, cache=True)
def glk(seg_x, seg_y, min_overlap):
    diff = np.abs(seg_x + seg_y)
    n = np.sum(~np.isnan(diff))
    nnan =  diff.size - n # number of nan

    if n < min_overlap:
        return n, nnan, -np.inf, -np.inf, 0
    sgc = np.sum(diff == 2.0) / n
    z_score = (sgc - 0.5) * 2.0 * np.sqrt(n)
    return n, nnan, sgc * 100, z_score, 0
    
class CrossDatingWorker:
    def __init__(self, min_overlap, method, distance, data_type=''):
        self.offsets = None
        self.data_type = data_type
        self.min_overlap = min_overlap
        self.method = method
        self.distance = distance
            
    def _init(self, data, master_data):
        self.self_crossdating = True if master_data is None else False
        self.data = data
        self.master_data = master_data if master_data is not None else data

    def run_it(self, row, master_data):        
        results = []
        for id_master, row_master in master_data.iterrows():
            results += self.run_series(row, row_master) 
        return results
    
    def run(self, data=None, master_data=None, progress=None, stop_event=None):
        self._init(data, master_data)
        if self.data is None:
            raise ValueError('cross dating.run: no data')
        
        results = []
        last_data = len(self.data) if self.master_data is not None else len(self.data) - 1
        if progress:
            progress.reset(last_data)
        
        progress.reset(last_data)
        for i, id in enumerate(self.data.index[:last_data]):
            row = self.data.iloc[i]
            master_start = i + 1 if self.self_crossdating else 0
            for id_master, row_master in self.master_data.iloc[master_start:].iterrows():
                results += self.run_series(row, row_master) 
                if stop_event is not None and stop_event.is_set():
                    #perror('run; stop_event')
                    return results
            if progress:
                progress.inc()
        
        return results

    def run_series(self, series, master_series):
        """
        Perform dating analysis between two data series.

        :param series: A dictionary representing the first data series.
        :param seriesMaster: A dictionary representing the second data series.
        :return: A Pandas DataFrame containing the dating results.
        """
        
        def add_rank(data, key_score, key_rank, reverse=False):

            sorted_data = sorted(data, key=lambda x: (math.isnan(x[key_score]), x[key_score] if not math.isnan(x[key_score]) else float('inf')), reverse=reverse)
            for i, res in enumerate(sorted_data):
                res[key_rank] = i +1
                      
            return sorted_data

        results_lst = []
        master_id, series_id = master_series[ID_CHILD], series[ID_CHILD]
        master_keycode, series_keycode = master_series[KEYCODE], series[KEYCODE]
        master_values, values = master_series[DATA_VALUES], series[DATA_VALUES]
        master_values_slope, values_slope = master_series[SLOPE], series[SLOPE]
        master_begin, series_begin = master_series[DATE_BEGIN], series[DATE_BEGIN]
        ring_count = series[DATA_LENGTH]
        
        estimate_date = pd.notna(master_begin)
        
        # Generate offsets and windows for the 2 series
        #perror('run_series; generate_dating_index', len(values), len(master_values), self.min_overlap)
        offsets, windows, master_windows = self._generate_dating_index(values, master_values, self.min_overlap)
        #perror('run_series; generate_dating_index', list(zip(offsets, windows, master_windows)))
        res_default = copy.copy(DEFAULTS)
        res_default[RES_ID_MASTER:RES_DATA_TYPE+1] =  master_id, series_id,  master_keycode, series_keycode, self.data_type
        for pos, window, master_window in zip(offsets, windows, master_windows):
            # Calculate the estimated first date
            if estimate_date:
                date_begin_estimated = master_begin + pos
                date_end_estimated = date_begin_estimated + ring_count - 1
            else:
                date_begin_estimated = pd.NA
                date_end_estimated = pd.NA

            #dated = str(series_begin == date_begin_estimated).lower() if estimate_date else ''
            dated = series_begin == date_begin_estimated
            res = copy.copy(res_default)
            res[RES_OFFSET:RES_SYNC+1] =  pos, date_begin_estimated, date_end_estimated, dated
            if CORRELATION in self.method or DISTANCE in self.method:
                #perror('run_series; CORRELATION', series_keycode, window, master_keycode, master_window)
                segment, master_segment = values[window[0]:window[1]], master_values[master_window[0]:master_window[1]]
                n, nnan, x, y = seg_validatation(segment, master_segment)
                if n >= self.min_overlap:
                    if CORRELATION in self.method:
                        res[RES_CORR_OVERLAP:RES_TP_VALUE+1] = n, nnan, *r(n, x, y)
                    if DISTANCE in self.method:
                        res[RES_DIST_OVERLAP:RES_DIST+1] = n, nnan, self._distance(x, y, distance=self.distance)
                else:
                    res[RES_CORR_OVERLAP:RES_CORR_OVERLAP_NAN+1] = n, nnan
                    res[RES_DIST_OVERLAP:RES_DIST_OVERLAP_NAN+1] = n, nnan
            if GLK in self.method:
                segment_slope, master_segment_slope = values_slope[window[0]:window[1]], master_values_slope[master_window[0]:master_window[1]]
                #perror('run_series; GLK', series_keycode, window, master_keycode, master_window)
                n, nnan, sgc, z_score, _ = glk(segment_slope, master_segment_slope, self.min_overlap)
                if n >= self.min_overlap:
                    res[RES_GLK_OVERLAP:RES_ZP_VALUE+1] = n, nnan, sgc, z_score, _ 
                else:
                    res[RES_GLK_OVERLAP:RES_GLK_OVERLAP_NAN+1] = n, nnan
            results_lst.append(res)
            
        if DISTANCE in self.method:
            results_lst = add_rank(results_lst, RES_DIST, RES_D_RANK, reverse=True)
        if GLK in self.method:
            results_lst = add_rank(results_lst, RES_Z_SCORE, RES_Z_RANK, reverse=True)
        if CORRELATION in self.method:
            results_lst = add_rank(results_lst, RES_T_SCORE, RES_T_RANK, reverse=True)
        return results_lst

    def _offset(self, offsets, windows, master_windows):
        # Check if a specific offset is provided for analysis
        if self.offsets is not None:
            lst = list(offsets)
            # If the specified offset exists in the list, narrow down the analysis to that offset
            if self.offsets in lst:
                i = lst.index(self.offsets)
                offsets = offsets[i:i+1]
                windows = windows[i:i+1]
                master_windows = master_windows[i:i+1]
            else:
                # If the specified offset does not exist, dating will be empty
                self.offsets = windows = master_windows = np.array([])
        return offsets, windows, master_windows

    def _generate_dating_index(self, series: np.ndarray, master: np.ndarray, min_overlap: int = 1):
        def generate_windows_offset(series_length: int, window_size: int, min_overlap: int = 1, flip: bool = False):
            if min_overlap < 1:
                raise ValueError('cross dating._generate_dating_index: min_periods must be > 0')
            # Calculate the ending offsets of the sliding window
            end = np.arange(1, series_length + window_size)
            start = end - window_size
            # Clip the end and start offsets to ensure they stay within the valid range
            end = np.clip(end, 0, series_length)
            start = np.clip(start, 0, series_length)
            if flip:
                # Optionally, flip the offsets
                end = np.flip(end)
                start = np.flip(start)
            # Identify offsets where the window size meets the minimum period requirement
            keep = np.where((end - start) >= min_overlap)
            return list(zip(start[keep], end[keep])), keep

        # Get the lengths of the 'master' and 'series' numpy.array
        length_master = len(master)
        length_series = len(series)
        # Calculate windows and offsets for 'series'
        series_windows, keep1 = generate_windows_offset(length_series, length_master, min_overlap)
        # Calculate windows and offsets for 'master' while optionally flipping them
        master_windows, _ = generate_windows_offset(length_master, length_series, min_overlap, True)
        # Generate offsets that correspond to the 'master' and 'series' windows
        offsets = -1*np.arange(-length_master + 1, length_series + 1)[keep1]

        return self._offset(offsets, series_windows, master_windows)
        
    def _distance(self, segment: np.ndarray, master_segment: np.ndarray, distance: str = COSINE):
        if EUCLIDEAN == distance:
            d = -1*spatial.distance.euclidean(segment, master_segment)
        elif CITYBLOCK == distance:
            d = -1*spatial.distance.cityblock(segment, master_segment)
        elif COSINE == distance:
            d = spatial.distance.cosine(segment, master_segment)
        else:
            raise ValueError(f'cross dating._distance: Unavailable distance method: {distance}')

        return d

class CrossDating(param.Parameterized):
    num_threads = param.Integer(default=1, bounds=(1, os.cpu_count()), step=1, doc='number of threads')
    min_overlap = param.Integer(default=50, bounds=(10, 100), step=1, doc='Minimal number of overlap ring')
    method = param.ListSelector([CORRELATION, GLK] , objects=crossdating_method, doc='Crossdating method')
    distance = param.Selector(objects=crossdating_distance, doc='Crossdating distance')
    
    class ParamProgress(param.Parameterized):
        start_time = param.Number(default=0, doc='start time of the run')
        current_time = param.Number(default=0, doc='current time of the run')
        max_count = param.Integer(default=0, doc='number of computed results to count')
        count = param.Integer(default=0, doc='number of computed results')
        
        def __init__(self):
            self.reset()
        
        def reset(self, max_count=0):
            self.max_count = max_count
            self.current_time = self.start_time = time.time()
            self.count = 0 
        
        def inc(self):
            self.current_time = time.time()
            self.count = self.count + 1 if self.count < self.max_count else self.max_count 
            # self.ring_type = None
            
        def info(self):
            if self.max_count <= 0:
                return 0, ''
            t = self.current_time - self.start_time
            r = round(self.count/self.max_count*100, 2)
            return int(r), f'{r}%, {self.count}/{self.max_count}' 
    progress = ParamProgress()
    
    class ParamMatrix(param.Parameterized):
        metric = param.Selector(default='euclidean', objects=['cityblock', 'correlation', 'cosine', 'euclidean', 'mahalanobis',  
                                                'seuclidean',  'sqeuclidean'], doc='Dendrogram metric')
        method = param.Selector(default='ward', objects=['single', 'complete', 'average', 'weighted', 'centroid', 
                                                'median', 'ward', ], doc='Dendrogram method to merge two clusters')
        sorted = param.Boolean(default=True, doc='Sort the matrix')
        size_scale = param.Number(default=0.5, bounds=(0.1, 1), step=0.1, doc='figure h/w scale')
        font_scale = param.Number(default=0.5, bounds=(0.1, 2), step=0.1, doc='figure font scale')
        color_map = param.Selector(default='viridis', objects=['viridis', 'crest', 'flare', 'magma', 'mako', 'rocket_r', 'rocket'], doc='Color map')
    
    param_matrix = ParamMatrix(name='Matrix')

    class ParamStem(param.Parameterized):
        height = param.Integer(default=500, bounds=(50, 1000), step=25)
        keycode_nrows = param.Integer(default=3, bounds=(1, 10), step=1)
        window_size = param.Integer(default=25, bounds=(5, 50), step=5)

    param_stem = ParamStem(name='Timeline')

    class ParamDensity(param.Parameterized):
        height = param.Integer(default=500, bounds=(50, 1000), step=10)
        width = param.Integer(default=800, bounds=(50, 1000), step=10)
        keycode_nrows = param.Integer(default=6, bounds=(1, 10), step=1)
        font_size = param.Integer(default=10, bounds=(1, 20), step=1)
        bullet_size = param.Integer(default=5, bounds=(1, 20), step=1)
        method = param.Selector(default='histogram', objects=['kde', 'histogram'], doc='Density method')
        bins_size = param.Number(default=0.5, bounds=(0.1, 2), step=0.1, doc='Histogram bins size')

    param_density = ParamDensity(name='Density')

    class ParamMap(param.Parameterized):
        providers = {'OpenStreetMap': xyz.OpenStreetMap.Mapnik, 
                    'OSMBright': xyz.Stadia.OSMBright,
                    'AlidadeSmooth': xyz.Stadia.AlidadeSmooth,
                    'StamenTerrainBackground': xyz.Stadia.StamenTerrainBackground,
                    'Positron': xyz.CartoDB.Positron,
                    'PositronNoLabels': xyz.CartoDB.PositronNoLabels,
                    'GeoportailFrance': xyz.GeoportailFrance.plan,
                    'SwissFederalGeoportal': xyz.SwissFederalGeoportal.NationalMapColor
                }
        providers_list = list(providers.keys())
        map_provider = param.Selector(default=providers_list[0], objects=providers_list, doc='Map provider')

        map_type = param.Selector(objects={'only master nodes':0, 'all nodes':1, 'nodes & edges':2}, doc='Map type')
        #nodes = param.Boolean(default=True, doc='Display nodes')
        height = param.Integer(default=1000, bounds=(250, 2000), step=10)
        width = param.Integer(default=1000, bounds=(250, 2000), step=10)
        map_center = param.XYCoordinates((3.0, 46.0), doc='Longitude and latitude of the center of the map. Double click on map to update.')
        map_radius = param.Integer(default=500, bounds=(10, 2000), step=10, doc='Radius of the map in Km')
        font_size = param.Integer(default=14, bounds=(1, 20), step=1)
        label_distance = param.Integer(default=5, bounds=(5, 20), step=1)
        line_ratio = param.Number(default=1, bounds=(0.1, 2), step=0.1)
        bullet_ratio = param.Number(default=1, bounds=(0.1, 10), step=0.1)
        alpha = param.Number(default=0.5, bounds=(0.1, 1), step=0.1)
            
    param_map = ParamMap(name='Map')

    class ParamGraph(param.Parameterized):
        height = param.Integer(default=1000, bounds=(250, 2000), step=10)
        width = param.Integer(default=1000, bounds=(250, 2000), step=10)
        font_size = param.Integer(default=14, bounds=(1, 20), step=1)
        line_ratio = param.Number(default=0.5, bounds=(0.1, 2), step=0.1)
        bullet_ratio = param.Number(default=0.5, bounds=(0.1, 2), step=0.1)
            
    param_graph = ParamGraph(name='Graph')

    results = None
    
    COLS = COLS

    def __init__(self, **params):

        super(CrossDating, self).__init__(**params)   

        self.offsets = None
        self.results = []
        self.df_results = None
        self.data = None
        self.master_data = None
        self.data_type = ''
        self.self_crossdating = False
    
    def run(self, data_type, data, master_data=None, force_process=False, stop_event=None, end_action=None):
        self.results = []
        self.df_results = None
        self.data_type = data_type
        if master_data is None: 
            self.self_crossdating = True
        worker_class = CrossDatingWorker(self.min_overlap, self.method, self.distance, self.data_type)
            
        t = time.time()
        if (self.num_threads == 1) or ProcessPoolExecutor is None:
            self.results = worker_class.run(data, master_data, self.progress, stop_event=stop_event)
        else:
            #if (self.num_threads > 1) or (force_process == True):
            self.results = self._run_thread(data, master_data, worker_class, stop_event=stop_event)
        logger.info(f'Elapsed time: {time.time() - t}')
        
        if stop_event is not None and stop_event.is_set():
            self.results = None
            
        if end_action is not None:
            end_action()

        return self.results        
    
    def _run_thread(self, data, master_data, worker_class, stop_event=None):
        self_crossdating = False
        if master_data is None:
            master_data = data
            self_crossdating = True
        last_data = len(data) if master_data is not None else len(data) - 1
        
        self.progress.reset(last_data)
        results = []
        with ProcessPoolExecutor(max_workers=self.num_threads) as executor:
            futures = [executor.submit(worker_it, worker_class, data.iloc[i], master_data.iloc[(i + 1 if self_crossdating else 0):]) for i in range(last_data)]
            for future in futures:
               self.progress.inc()
               if stop_event is not None and stop_event.is_set():
                   future.cancel()
               results += future.result()
        
        return results

    def results_to_df(self):
        if (self.results is None) or (len(self.results) == 0):
            logger.warning('cross dating.concat_results: no results')
            return None
        if self.df_results is None:
            cols = self.get_cols_method(all=True)
            self.df_results = pd.DataFrame(np.array(self.results), columns=list(cols.keys()))
            self.df_results = self.df_results.astype(cols, copy=True, errors='ignore')

        return self.df_results

    def get_cols_method(self, all=False):
        cols = copy.copy(COLS_BASE)
        if all == True:
            return cols | COLS_R | COLS_GLK | COLS_D
        if CORRELATION in self.method:
            cols = cols | COLS_R
        if GLK  in self.method:
            cols = cols | COLS_GLK
        if DISTANCE in self.method:
            cols = cols | COLS_D
        return cols

    def concat_results(self, score=None, threshold=None, max_rank=None, sync=None, incorrect_date=None):
        #if score is None:
        #    score = self.method[0]
        
        if self.results_to_df() is None:
            return None
        #perror(self.df_results.info())
        
        mask = np.array([True] * len(self.df_results))
        if (max_rank is not None):
            rank_key = self.get_rank_key(score)
            #perror('concat_results; max_rank', max_rank, rank_key)
            mask = (self.df_results[rank_key] <= max_rank) & mask
        if threshold is not None:
            mask = (self.df_results[score] >= threshold) & mask
        if sync is not None:
            mask = (self.df_results[SYNC] == sync) & mask
            #mask = (self.df_results[SYNC] == str(sync).lower()) & mask
        if incorrect_date is not None:
            year = datetime.now().year + 1
            mask = (self.df_results[DATE_BEGIN_ESTIMATED] < year) & mask
            mask = (self.df_results[DATE_END_ESTIMATED] < year) & mask

        cols = self.get_cols_method().keys()
        return self.df_results.loc[mask, cols]

    def discounted_cumulative_gain(self, rank_key=T_RANK, score_key=T_SCORE, max_rank=None):
    # Discounted Cumulative Gain 
    # https://en.wikipedia.org/wiki/Discounted_cumulative_gain

        sdcg = srank = n = 0
        res = []
        results = self.results_to_df()
        dated = results[results[SYNC]]
        n = len(dated)
        if max_rank is not None:
            dated = dated[dated[rank_key] <= max_rank]
        dated['DCG'] = dated[score_key] / np.log2(dated[rank_key].to_numpy(dtype='float') + 1)
        if dated['DCG'].sum() == np.inf:
            for id, row in dated[[KEYCODE, KEYCODE_MASTER, score_key, rank_key, 'DCG']].iterrows():
                print(row.to_list())
        return dated, n, dated['DCG'].sum(), dated[rank_key].sum()
    
    
    """def det_curve(self, key_score=SCORE):
        df = self.concat_results()[[key_score, SYNC]]
        fpr, fnr, thresholds = det_curve(y_score=df[key_score].to_numpy(), y_true=df[SYNC].to_numpy(dtype='Int32') )
        det = DetCurveDisplay(fpr=fpr, fnr=fnr, estimator_name=key_score+' / '+self.ring_type)
        return fpr, fnr, thresholds, det"""
    
    def matrix(self, data, score, col_keys=[KEYCODE_MASTER, KEYCODE]):#, score=None, threshold=None):
        if (data is None) or (len(self.results) == 0):
            raise ValueError('no dated results')
        if score not in data.columns:
            raise KeyError(f'cross dating.matrix: {score} not in results')

        columns = data[col_keys[1]].unique().tolist()
        index = data[col_keys[0]].unique().tolist()
        df = data.loc[:, col_keys + [score]]
        if self.self_crossdating:
            ids = list(set(columns + index))    
            mat = pd.DataFrame(columns=ids, index=ids, dtype='float')
            for _, (id1, id2, value) in df.iterrows():
                mat.at[id1, id2] = mat.at[id2, id1] = float(value)
        else:
            mat = pd.DataFrame(columns=columns, index=index, dtype='float')
            for _, (id1, id2, value) in df.iterrows():
                mat.at[id1, id2] = float(value)
        return mat

    def get_rank_key(self, score):
        if score in [DISTANCE]:
            return D_RANK
        elif score in [Z_SCORE, GLK]:
            return Z_RANK
        else:
            return T_RANK
    
    def fillmat(self, mat):
        finite_values = mat.replace([np.inf, -np.inf], np.nan)
        max_with_eps = np.nextafter(finite_values.max(axis=None), np.inf)
        min_with_eps = np.nextafter(finite_values.min(axis=None), -np.inf)
        mat.replace([np.inf, -np.inf], [max_with_eps, min_with_eps], inplace=True)
        if self.self_crossdating:
            np.fill_diagonal(mat.values, np.nan)
        mask = mat.isna()
        
        return mat.fillna(min_with_eps), mask
        
    
    def heat_matrix(self, score, threshold=None, col_keys=[KEYCODE_MASTER, KEYCODE], 
                    metric=None, method=None):
        sns.set_theme(font_scale=0.5, palette='colorblind')

        if metric is None: metric = self.param_matrix.metric
        if method is None: method = self.param_matrix.method
        
        data = self.concat_results(score=score, threshold=threshold, max_rank=None, sync=True)
        data = self.matrix(data, score, col_keys)  
        mat, mask = self.fillmat(data)  
        
        size_h = np.ceil(data.shape[0]) * self.param_matrix.size_scale
        size_w = np.ceil(data.shape[1]) * self.param_matrix.size_scale
        sns.set_context("notebook", font_scale=self.param_matrix.font_scale)
        
        #cm = sns.light_palette("#79C", n_colors=mat.stack().nunique(), reverse=False, as_cmap=True)
        cm = sns.color_palette(self.param_matrix.color_map, n_colors=mat.stack().nunique(), as_cmap=True)
        if self.param_matrix.sorted:
            fig = sns.clustermap(mat, metric=metric ,method=method, cmap=cm, linewidths=.5, 
                                 figsize=(size_h, size_w), mask=mask, annot=data)._figure
        else: 
            fig, ax = plt.subplots(figsize=(size_h, size_w))
            ax = sns.heatmap(mat, cmap=cm, linewidths=.5, ax=ax, mask=mask, annot=data)
        plt.close(fig)
        return fig
    
    def stem(self, score, threshold=None, max_rank=None, keycode=''):    
        rank_key = self.get_rank_key(score)
        data = self.concat_results(score=score, threshold=threshold, max_rank=max_rank)
        if max_rank is None:
            max_rank = data[rank_key].max()
            
        if len(data) == 0:
            raise ValueError(f'cross dating.stem: The results matrix is empty after applying the threshold and max_rank.')
        if data[DATE_END_ESTIMATED].isna().all():
            raise ValueError(f'cross dating.stem: no {DATE_END_ESTIMATED}')

        keycodes = sorted(data[KEYCODE].unique().tolist())
        ranks = [f'rank {x}' for x in range(max_rank)]
        MARKERS = ['circle', 'square', 'diamond', 'hex', 'star', 'triangle', 'inverted_triangle', 'asterisk',
                   'circle_cross', 'square_cross', 'diamond_cross', 
                   'circle_dot', 'square_dot', 'diamond_dot', 'hex_dot', 'star_dot', 'triangle_dot',
                   'circle_x', 'circle_y', 'dash', 'plus', 'square_pin', 'square_x', 'triangle_pin', 'x', 'y', 'dot', 'cross', ]
        h = self.param_stem.height
        win = self.param_stem.window_size//2
        date_max = data.loc[data[rank_key] == 1, DATE_END_ESTIMATED].value_counts().idxmax()
        nranks = len(ranks) if len(ranks) < 11 else 11
        colors = brewer['RdYlBu'][nranks]
        fig = figure(title=keycode, background_fill_color="#fafafa", 
                   x_range=(date_max-win, date_max+win), height=h, sizing_mode='stretch_width',
                   tools="pan,wheel_zoom,box_zoom,reset,hover,save", toolbar_location="left",
                   tooltips=[(KEYCODE, f'@{KEYCODE}'), ('keycode master', '@MASTER'), (f'{score}', '@score'), (f'{rank_key}', '@rank')])
        fig.output_backend = "svg"

        fig.xaxis.axis_label = DATE_END_ESTIMATED
        fig.yaxis.axis_label = score
        
        for rank, df in data.groupby(rank_key):
            df2 = df.rename(columns={KEYCODE_MASTER: 'MASTER', score:'score', rank_key: 'rank'})
            c = colors[rank-1] if rank < nranks else colors[nranks-1]
            fig.scatter(DATE_END_ESTIMATED, 'score', source=ColumnDataSource(df2), 
                    fill_alpha=0.8, size=12, marker=factor_mark(KEYCODE, MARKERS, keycodes), color=c) #legend_group=KEYCODE,
            
        # Add keycodes legend
        # create an invisible renderer to drive shape legend
        rs = fig.scatter(x=0, y=0, color="grey", size=6, marker=MARKERS[:len(keycodes)])
        rs.visible = False

        # add a shape legend with explicit index, set labels to fit your needs
        legend = Legend(
            items=[LegendItem(label=s, renderers=[rs], index=i) for i, s in enumerate(keycodes)],
            location='center_left', orientation='horizontal', nrows=self.param_stem.keycode_nrows, title=KEYCODE)
        fig.add_layout(legend, 'above')
        
        # Add rank legend
        # create an invisible renderer to drive color legend
        rc = fig.rect(x=0, y=0, height=1, width=1, color=colors[:nranks])
        rc.visible = False

        # add a color legend with explicit index, set labels to fit your need
        labels = [f'rank {i}' if i < nranks -1 else f'rank \u2265 {i}' for i, c in enumerate(colors[:nranks])]
        legend = Legend(items=[LegendItem(label=labels[i], renderers=[rc], index=i) for i, c in enumerate(colors[:nranks])], 
                location='center_left', orientation='horizontal', nrows=1, title=rank_key)
        fig.add_layout(legend, 'above')
        
        # Add ZOOM
        zoom_fig = figure(sizing_mode='stretch_width', height=round(h / 4), y_range=fig.y_range,
            background_fill_color="#fafafa", tooltips='',
            tools="save", toolbar_location="left",)
        zoom_fig.output_backend = "svg"
        
        for rank, df in data.groupby(rank_key):
            c = colors[rank-1] if rank < nranks else colors[nranks-1]
            zoom_fig.scatter(DATE_END_ESTIMATED, score, source=ColumnDataSource(df), fill_alpha=0.8, 
                                size=3, marker=factor_mark(KEYCODE, MARKERS, keycodes), color=c)

        zoom_fig.x_range.range_padding = 0
        zoom_fig.ygrid.grid_line_color = None
        zoom_fig.xaxis.axis_label = DATE_END_ESTIMATED
        zoom_fig.yaxis.axis_label = score

        range_tool = RangeTool(x_range=fig.x_range)
        range_tool.overlay.fill_color = "navy"
        range_tool.overlay.fill_alpha = 0.2
        zoom_fig.add_tools(range_tool)
        
        return fig, zoom_fig
                
    def density(self, score=None):
        def get_param(data):
            data[score] = data[score].replace([np.inf, -np.inf], np.nan)
            height = self.param_density.height
            width = self.param_density.width
            font_size = f'{self.param_density.font_size}pt'
            smin, smax = data[score].min() , data[score].max() 
            d = (smax - smin) * 0.01
            smin, smax = smin - d, smax + d
            n = round((smax - smin) * 10)
            x = np.linspace(smin, smax, n)
            x_range = Range1d(smin, smax)
            formater = PrintfTickFormatter(format="%5.1f")
            
            return x, [width, height, x_range, formater, font_size], [font_size]
        
        def get_figure(id, keycode, y_range, width, height, x_range, formater, font_size):
            p = figure(title=keycode, width=width, height=height, tools='save', x_range=x_range, y_range=y_range)
            p.output_backend = "svg"
            p.xaxis[0].formatter = formater
            p.xaxis.visible = True
            p.yaxis.visible = True
            p.title.text_font_size = font_size
            p.title.text_font_style = "bold"
            p.xaxis.major_label_text_font_size = font_size
            p.yaxis.major_label_text_font_size = font_size
            p.ygrid.grid_line_color = None
            
            return p
        
        def set_legend(items, font_size):
            legend = Legend(items=items, 
                            location='center_left', 
                            orientation='horizontal',
                            nrows=self.param_density.keycode_nrows,
                            label_text_font_size = font_size,
                            click_policy="hide"
                            )
            p.add_layout(legend, 'above')
            return legend
        
        def get_n_colors(n, palette):
            d = 25
            p = palette[d:-d]

            n = len(p) if n > len(p) else n
            step = len(palette) // n
            colors = p[::step][:n]
            #perror('get_n_colors', n, len(p), step, colors)
            return colors

        method = self.param_density.method
        bins_size = self.param_density.bins_size
        data = self.concat_results(score=score)
        mask = data[score].notna() & ~data[score].isin([np.inf, -np.inf])
        data = data.loc[mask]
        
        if len(data) == 0:
            raise ValueError(f'cross dating.hist: The results matrix is empty after applying the threshold and max_rank.')
        x, param, param_legend = get_param(data)
        
        master_keycodes = {x: data.loc[data[ID_MASTER] == x, KEYCODE_MASTER].iloc[0] for x in data[ID_MASTER].unique()}
        legends = []
        rows = []
        source_vect = {}
        source = {}
        y_max = 0
        for id, id_data in data.groupby(ID):
            colors_b = get_n_colors(len(id_data[ID_MASTER].unique()), Blues256)
            n_colors_b = len(colors_b)
            colors_r = get_n_colors(len(id_data[ID_MASTER].unique()), Turbo256)
            n_colors_r = len(colors_r)
            source_vect[id] = {}
            source[id] = {}
            for i, (id_master, master_data) in enumerate(id_data.groupby(ID_MASTER)):
                #perror('density', id, id_master, score, master_data.info())
                master_data_nan = master_data[score]
                #perror('density', id, id_master, score, len(master_data_nan))
                
                if method == 'kde':
                    pdf = gaussian_kde(master_data_nan)
                    y = pdf(x)
                    y[0] = y[-1] = 0
                else:
                    min_score, max_score = int(np.floor(master_data_nan.min())), int(np.ceil(master_data_nan.max()))
                    bins = np.arange(min_score, max_score, bins_size)
                    y, bin_edges = np.histogram(master_data_nan, bins=bins, density=False)  # Ajustez le nombre de bins selon vos besoins
                    x = (bin_edges[:-1] + bin_edges[1:]) / 2  # Centres des bins pour l'affichage
                ly_max = np.nanmax(y)
                y_max = max(ly_max, y_max) 
                dx = dy = ey = np.nan
                
                if not master_data[SYNC].isna().any():
                    mask = master_data[SYNC]
                    ey = master_data.loc[mask, DATE_END_ESTIMATED].max()
                    dx = master_data.loc[mask, score].max()
                    if not np.isnan(dx):
                        if method == 'kde':
                            dy = pdf(dx)[0]
                        else:
                            dy = y[np.where(x == dx)]
                source_vect[id][id_master] = ColumnDataSource(data={'x': x, 'y': y}) 
                source[id][id_master] = ColumnDataSource(data={'dx': [dx], 'dy': [dy], 
                                                            'ey': [ey], 
                                                            'x0': [dx], 'x1': [dx], 
                                                            'y0': [0], 'y1': [dy], 
                                                            'color': [colors_r[i % n_colors_r]]})

        y_range = Range1d(0, y_max+0.2)
        for id, id_data in data.groupby(ID):
            items = []
            keycode = id_data[KEYCODE].iloc[0]
            p = get_figure(id, keycode, y_range, *param)
            curve = []
            for i, (id_master, master_data) in enumerate(id_data.groupby(ID_MASTER)):
                if method == 'kde':
                    curve.append(p.patch(x='x', y='y', source=source_vect[id][id_master], alpha=0.2, color=colors_b[i % n_colors_b]))
                else:
                    curve.append(p.vbar(x='x', top='y', width=0.5, source=source_vect[id][id_master], alpha=0.2, color=colors_b[i % n_colors_b]))

            for i, (id_master, master_data) in enumerate(id_data.groupby(ID_MASTER)):
                score_dated=source[id][id_master].data['dx'][0]
                if not np.isnan(score_dated):
                    label = f'{master_keycodes[id_master]}: {round(float(score_dated), 3)}'
                    #dated = p.scatter(x='dx', y='dy', source=source[id][id_master], color='color', size=self.param_density.bullet_size)#, legend_label=f'{master_keycodes[id_master]}')
                    source[id][id_master].data['y1'] = [y_max]
                    dated_seg = p.segment(x0='x0', x1='x1', y0='y0', y1='y1', source=source[id][id_master], color='color')
#                    items.append((label, [dated, dated_seg, curve[i]]))
                    items.append((label, [dated_seg, curve[i]]))
                else:
                    label = f'{master_keycodes[id_master]}: undated'
                    items.append((label, [curve[i]]))
            
            if len(items) > 0:
                l = set_legend(items, *param_legend)
                legends.append(l)
            else:
                legends.append(None)
            
            rows.append(p)
            
        return rows, legends

    def map(self, score, data_dt=None, threshold=0, max_rank=None):
        
        def lnglat_to_meters(longitude: float, latitude: float) -> tuple[float, float]:
            """ Projects the given (longitude, latitude) values into Web Mercator
            coordinates (meters East of Greenwich and meters North of the Equator)."""
            origin_shift = np.pi * 6378137
            easting = longitude * origin_shift / 180.0
            northing = np.log(np.tan((90 + latitude) * np.pi / 360.0)) * origin_shift / np.pi
            #if pd.isna(easting) or pd.isna(northing):
            #    perror('+++ lnglat_to_meters', longitude, latitude, easting, northing)
            return (easting, northing)
        
        def meters_to_lnglat(easting: float, northing: float) -> tuple[float, float]:
            """ Converts Web Mercator coordinates (meters East of Greenwich and meters North of the Equator)
            back into (longitude, latitude) values. """
            origin_shift = np.pi * 6378137
            longitude = round(easting / origin_shift * 180.0, 3)
            latitude = round((2 * np.arctan(np.exp(northing / origin_shift * np.pi)) - np.pi / 2) * 180.0 / np.pi, 3)
            return (longitude, latitude)

        def callback(event):
            self.param_map.map_center = meters_to_lnglat(event.x, event.y)

        anchor_dict = {0:('center_left', -1, 0), 1:('center_right', 1 ,0), 2:('top_center', 0, -1), 3:('bottom_center',0, 1), 
                       4:('top_left', -1, -1), 5:('top_right', 1, -1), 6:('bottom_left', 1, -1), 7:('bottom_right', 1, 1)}
        
        def get_anchor(x, y, size, plotted_nodes):
            k = 0
            ld = self.param_map.label_distance
            radius = size / 2
            for p, anchor in plotted_nodes.items():
                #d = spatial.distance.euclidean((x, y), p)
                #perror('**** d', d, (x, y), p, radius + 20)
                if spatial.distance.euclidean((x, y), p) <= (radius + 20):
                    k = anchor if anchor < len(anchor_dict) else 0            
            name, dx, dy = anchor_dict[k]
            dx, dy = (ld + radius) * dx, (ld + radius) * dy
            return k, name, dx, dy
            
        #rank_key = self.get_rank_key(score)
        data = self.concat_results(score=score, threshold=threshold, max_rank=max_rank, sync=True)
        
        if len(data) == 0:
            raise MapValueError('The data is empty after applying the threshold and the max_rank.')
        if data_dt is None:
            raise MapValueError('The data is empty after applying the threshold and the max_rank.')  
          
        if data_dt[SITE_LONGITUDE].isna().any():
            raise MapValueError(f'{SITE_LONGITUDE} are empty.')
        if data_dt[SITE_LATITUDE].isna().any():
            raise MapValueError(f'{SITE_LATITUDE} are empty.')

        nodes = data.groupby(ID_MASTER)[score].sum().to_dict()
        keycodes = data[[ID_MASTER, KEYCODE_MASTER]].drop_duplicates().set_index(ID_MASTER).to_dict()[KEYCODE_MASTER]
        if self.param_map.map_type > 0:        
            nodes.update(data.groupby(ID)[score].sum().to_dict())
            keycodes.update(data[[ID, KEYCODE]].drop_duplicates().set_index(ID).to_dict()[KEYCODE])
        
        geo = {row[ID_CHILD]: lnglat_to_meters(row[SITE_LONGITUDE], row[SITE_LATITUDE]) for _, row in data_dt.iterrows()}
        
        map_center = lnglat_to_meters(*self.param_map.map_center) # Map center
        delta = self.param_map.map_radius * 1000 # (m)  plus-and-minus from map center

        fig = figure(x_range=(map_center[0] - delta, map_center[0] + delta), 
                    y_range=(map_center[1] - delta, map_center[1] + delta) , 
                    x_axis_type="mercator", y_axis_type="mercator",
                    height=self.param_map.height, width=self.param_map.width, 
                    tools="pan,wheel_zoom,box_zoom,reset,hover,save",toolbar_location="left",)
                    #tooltips=[(KEYCODE, f'@{KEYCODE}')])
        fig.add_tile(self.param_map.providers[self.param_map.map_provider])        
        fig.on_event(DoubleTap, callback)
        
        ft_size = str(self.param_map.font_size)+'px'
        plotted_nodes = {} 
        info = []
        for i, (id, value) in enumerate(nodes.items()):
            if (geo[id][0] is not None) and (geo[id][1] is not None) and (id in nodes.keys()):
                size = (value + 1) * self.param_map.bullet_ratio
                x, y = geo[id]
                anchor, anchor_str, dx, dy = get_anchor(x, y, size, plotted_nodes)
                    
                info.append({'i':i+1, ID: id, KEYCODE: keycodes[id], score: value, 
                             'x': x, 'y': y, 'dx': dx, 'dy': dy, 
                             'size': size, 'anchor_str': anchor_str,
                            'legend_label': f'{i+1}: {keycodes[id]} (sum of {score} = {round(value, 3)})'})
                plotted_nodes[(x, y)] = anchor

        source_nodes = ColumnDataSource(data=pd.DataFrame(info))
        fig.scatter(x='x', y='y', source=source_nodes, color=RdYlBu9[1], alpha=self.param_map.alpha, size='size', legend_group='legend_label')
        fig.text(x='x', y='y', source=source_nodes, text='i', x_offset='dx', y_offset='dy', anchor='anchor_str', text_font_size=ft_size)
        
        if self.param_map.map_type == 2:
            for _, row in data.iterrows():
                id_master = row[ID_MASTER]
                id = row[ID]
                value = row[score]
                lw = (value + 1) * self.param_map.line_ratio
                color = RdYlBu9[0] if value > 0 else RdYlBu9[8]
                x = [geo[id][0], geo[id_master][0]]
                y = [geo[id][1], geo[id_master][1]]
                fig.line(x, y, alpha=self.param_map.alpha, color=color, line_width=lw, line_cap='round')
        
        fig.legend.location = "top_left"
        fig.legend.padding = 1
        fig.legend.margin = 1
        fig.add_layout(fig.legend[0], 'left')
        
        return fig
    
    def graph(self, score, threshold=0, max_rank=None):
        def get_graph(G, scale=1):
            return from_networkx(G, nx.circular_layout, scale=scale, center=(0,0))
        
        #logger.info('graph')
        
        rank_key = self.get_rank_key(score)
        data = self.concat_results(score=score, threshold=threshold, max_rank=max_rank, sync=True)
        
        if len(data) == 0:
            raise ValueError(f'cross dating.stem: The results matrix is empty after applying the threshold and max_rank.')
        
        keycodes = data[[ID, KEYCODE]].drop_duplicates().set_index(ID).to_dict()[KEYCODE]
        keycodes.update(data[[ID_MASTER, KEYCODE_MASTER]].drop_duplicates().set_index(ID_MASTER).to_dict()[KEYCODE_MASTER])
        nodes = data.groupby(ID)[score].sum().to_dict()
        nodes.update(data.groupby(ID_MASTER)[score].sum().to_dict())

        from bokeh.palettes import Turbo256
        from bokeh.plotting import figure, from_networkx

        G = nx.Graph()
        elist = [(row[ID_MASTER], row[ID], row[score]) for _, row in data.iterrows()]
        G.add_weighted_edges_from(elist)
        
        fig = figure(x_range=(-2, 2), y_range=(-2, 2),
           x_axis_location=None, y_axis_location=None,
           height=self.param_graph.height, width=self.param_graph.width, toolbar_location="left",
           tools='pan,wheel_zoom,box_zoom,reset,hover,save', tooltips=f"{KEYCODE}: @{KEYCODE}")
        fig.grid.grid_line_color = None
        fig.output_backend = "svg"

        graph = get_graph(G)

        fig.renderers.append(graph)

        # Add some new columns to the renderers 
        color = []
        size = []
        value = []
        name = []
        d = max(256 // len(graph.node_renderer.data_source.data['index']), 1)
        for i, id in enumerate(graph.node_renderer.data_source.data['index']):
            color.append(Turbo256[min(i*d, 255)])
            size.append(int(max(nodes[id], 1) * self.param_graph.bullet_ratio))
            value.append(nodes[id])
            name.append(keycodes[id])
        graph.node_renderer.data_source.data['color'] = color
        graph.node_renderer.data_source.data['size'] = size
        graph.node_renderer.data_source.data['value'] = value
        graph.node_renderer.data_source.data['name'] = name
        
        ft_size = str(self.param_graph.font_size)+'px'

        width = []
        tmp = graph.edge_renderer.data_source.data
        for start, end, weight in zip(tmp['start'], tmp['end'], tmp['weight']):
            width.append(int((weight+1)*self.param_graph.line_ratio))

        graph.edge_renderer.data_source.data['width'] = width
        
        #print('-'*10)
        text_ds = ColumnDataSource()
        xs, ys, ids, keys, anchor, x_offset, y_offset = [], [], [], [], [], [], []
        for key, (x, y) in graph.layout_provider.graph_layout.items():
            xs.append(x)           
            ys.append(y) 
            ids.append(key) 
            keys.append(keycodes[key]) 
            if x > 0:
                a = 'top_left' if y < 0 else 'bottom_left'
            else:
                a = 'top_right' if y < 0 else 'bottom_right'
            #s = int(max(nodes[id], 1) * self.param_graph.bullet_ratio) + 10
            s = 10
            ox = s if x > 0 else -s
            oy = -s if y > 0 else s
            anchor.append(a)
            x_offset.append(ox)
            y_offset.append(oy)

            #label = Label(x=x, y=y, anchor=a, text=str(keycodes[key]), editable = True, 
            #        text_color='black', text_font_size=ft_size, x_offset=ox, y_offset=oy)
            #fig.add_layout(label)
            
        
        text_ds.data['x'], text_ds.data['y'] = xs, ys
        text_ds.data[ID], text_ds.data[KEYCODE] = ids, keys
        text_ds.data['anchor'], text_ds.data['x_offset'], text_ds.data['y_offset'] = anchor, x_offset, y_offset
        fig.text(x='x', y='y', text=KEYCODE, source=text_ds,  anchor='anchor', x_offset='x_offset', y_offset='y_offset', text_font_size=ft_size)
            

        graph.node_renderer.glyph.update(size="size", fill_color="color")
        graph.edge_renderer.glyph.update(line_width="width")
        
        return fig


