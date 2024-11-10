"""
Parametre classes for the sidebar
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import os
import param
import copy
import panel as pn
from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.crossdating import CrossDating
from pyDendron.detrend import detrend_types
from pyDendron.gui_panel.tabulator import _cell_transform


class ParamColumns:
    def __init__(self, selections=[ICON, KEYCODE, DATE_BEGIN, DATE_END, OFFSET], dtype=dtype_view, title='Columns'):
        self.dtype = dtype
        options_list = selections + list(set(dtype.keys()) - set(selections)) 
        
        self.columns = self.columns = pn.widgets.MultiChoice(name='Columns', value=selections, options=options_list, 
                                     sizing_mode='stretch_width', search_option_limit=25, description='Select columns to display in table.')
        self.title = title
        self.move_field = pn.widgets.Select(name='Move field', options=selections, value='', sizing_mode='stretch_width') 
        self.columns.param.watch(self.on_columns, ['value'], onlychanged=True, queued=True)
        
        self.bt_up = pn.widgets.Button(name='Up', icon="arrow-up", align=('start', 'end'))
        self.bt_up.on_click(self.on_up)
        
        self.bt_down = pn.widgets.Button(name='Down', icon="arrow-down", align=('start', 'end'))
        self.bt_down.on_click(self.on_down)

        self.card = pn.Card(self.columns, pn.Row(self.move_field, self.bt_up, self.bt_down), title=self.title, sizing_mode='stretch_width', margin=(5, 0), collapsed=True)
        
    def on_columns(self, event):
        sv = self.move_field.value
        self.move_field.options = event.new
        self.move_field.value = sv if sv in event.new else ''
    
    def on_up(self, event):
        move_field = self.move_field.value
        columns = copy.deepcopy(self.columns.value)
        if move_field is not None:
            i = columns.index(move_field)
            if i > 0:
                columns[i], columns[i-1] = columns[i-1], columns[i]
                self.columns.options = columns + list(set(self.columns.options) - set(columns))                
                self.columns.value = columns
                self.move_field.value = move_field                
    
    def on_down(self, event):
        move_field = self.move_field.value
        columns = copy.deepcopy(self.columns.value)
        if move_field is not None:
            i = columns.index(move_field)
            if i < len(columns)-1:
                columns[i], columns[i+1] = columns[i+1], columns[i]
                self.columns.options = columns + list(set(self.columns.options) - set(columns))                
                self.columns.value = columns
                self.move_field.value = move_field
                   
    def handle_columns(self, change):
        self.columns_hide.value = change.new

    def get_dtype(self):
        return self.dtype

    def get_hiddens(self):
        return list(set(self.get_options()) - set(self.get_columns())) 

    def get_columns_hiddens(self):
        return self.get_columns() + self.get_hiddens()

    def get_columns(self):
        return  self.columns.value
    
    def get_options(self):
        return  self.columns.options

    def get_widgets(self):
        return self.columns
        
    def get_sidebar(self):    
        return self.card  
    
    def update_tabulator(self, wtabulator, data=None, add_statistics=False):
        wtabulator.hidden_columns=self.get_hiddens() 
        if wtabulator.value is not None:
            if data is None:
                data = wtabulator.value
            col = self.get_columns_hiddens() 
            if add_statistics:
                col += stat_dtype_dict.keys()
            col = [c for c in col if c in data.columns]
            wtabulator.value = _cell_transform(data[col])         

class ParamColumnPackage(ParamColumns):
    def __init__(self, selections=[ICON, KEYCODE, DATE_BEGIN, DATE_END, OFFSET], dtype=dtype_package, title='Package Columns'):
        super().__init__(selections, dtype, title)

class ParamColumnCrossDating(ParamColumns):
    def __init__(self, selections=list(set(CrossDating.COLS.keys())- set([ID, ID_MASTER])), dtype=CrossDating.COLS, title='Statistic Columns'):
        super().__init__(selections, dtype, title)


class ParamMean(param.Parameterized):
    #num_threads = param.Integer(default=1, bounds=(1, os.cpu_count()), step=1, doc='Number of threads.')
    biweight_mean =  param.Boolean(False, doc='Biweight mean method for computing the mean.')
    date_as_offset =  param.Boolean(True, doc='Dates are used as offsets for computing the mean.')
    check_mean_as_measure = param.Boolean(False, doc='Check if Mean is considered as a measure.')
    min_elements = param.Integer(default=4, bounds=(1, 30), step=1, doc='Minimal number of elements for computing the mean.')
    def get_sidebar(self):    
        return pn.Card(pn.Param(self, show_name=False), title='Mean', sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  

class ParamDetrend(param.Parameterized):
    #num_threads = param.Integer(default=1, bounds=(1, 10), step=1, doc='Number of threads.')
    detrend = param.Selector(objects=detrend_types, doc='Detrend method apply to the series.')
    window_size = param.Integer(default=5, bounds=(3, 15), step=2, doc='Size of the sliding window for detrending.')
    log = param.Boolean(True, doc='Perform a logarithm transformation at the end of detrending.')
            
    def __init__(self, **params):
        super(ParamDetrend,self).__init__(**params)
    
    def get_sidebar(self):
        return pn.Card(pn.Param(self, show_name=False), title='Detrend', sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  

class ParamPackage(param.Parameterized):
    #show_data = param.Boolean(False, doc='Show data in selection view')
    cambium_estimation_method = param.Selector(default='Lambert', objects=['Lambert', 'log-log', 'user values'], doc='Method for cambium estimation.')
    lambert_parameters = param.Range(default=(12,23), bounds=(0, 60), step=1, doc='Lambert estimator range.')
    #pith_estimation = param.Boolean(False, doc='Draw pith estimation')
    slope_resolution = param.Integer(default=0, bounds=(0, 10), step=1, doc='Minimal GLK resolution')
            
    def __init__(self, **params):
        super(ParamPackage,self).__init__(**params)
    
    def get_sidebar(self):
        return pn.Card(pn.Param(self, show_name=False), title='Package', sizing_mode='stretch_width', margin=(5, 0), collapsed=True)  
