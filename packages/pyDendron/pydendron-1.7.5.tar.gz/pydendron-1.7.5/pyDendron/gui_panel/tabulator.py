"""
Tabulator tools
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import numpy as np
import pandas as pd
import panel as pn
import os
from pathlib import Path

from bokeh.models.widgets.tables import (NumberFormatter, DateFormatter, StringFormatter,
                                         SelectEditor, NumberEditor, BooleanFormatter)

from pyDendron.dataname import *
from pyDendron.app_logger import logger, perror

def unique_filename(filename):
    filename = Path(filename)  
    directory = filename.parent  
    base, extension = filename.stem, filename.suffix  
    unique_fn = filename
    n = 1

    while unique_fn.exists():
        unique_fn = directory / f"{base}({n}){extension}"
        n += 1

    return unique_fn

def get_download_folder():
    # Pour Windows
    if os.name == 'nt':
        download_folder = Path(os.getenv('USERPROFILE')) / 'Downloads'
    # Pour macOS et Linux
    else:
        download_folder = Path.home() / 'Downloads'
    
    return download_folder

def _cell_transform(data):
    if data is None:
        return data
    data_out = pd.DataFrame()
    for col, dtype in data.dtypes.to_dict().items():
        if col not in [ICON, ID, ID_CHILD, ID_PARENT]:                    
            if str(dtype).lower().startswith('int'):
                data_out[col] = data[col].fillna(np.nan).astype('float')
            elif str(dtype).lower().startswith('float'):
                data_out[col] = data[col].fillna(np.nan).astype('float')
            elif str(dtype).lower().startswith('bool'):
                data_out[col] = data[col].astype('string').fillna('NA')
            elif str(dtype).lower().startswith('string'):
                data_out[col] = data[col].fillna('')
            elif str(dtype).lower().startswith('date'):
                data_out[col] = data[col]
            elif str(dtype).lower().startswith('obj') and not isinstance(data[col], np.ndarray):
                data_out[col] = data[col].fillna('')
            elif str(dtype).lower().startswith('obj') :
                data_out[col] = data[col]
            else:
                logger.warning(f'Unknown dtype {dtype} for column {col}')            
                #data_out[col] = data[col]
        else:            
            data_out[col] = data[col]
    return data_out
            
def _cell_text_align(dtype_dict):
    aligns = {} 
    for key, dtype in dtype_dict.items():
        aligns[key] = 'left' if (dtype == 'string') or (dtype == 'object') else 'center' 
    if (ICON in aligns) :
        aligns[ICON] = 'center'
    return aligns

def _cell_formatters(dtype_dict, bool_formater=False):
    formatters = {} 
    for key, dtype in dtype_dict.items():
        if str(dtype).lower().startswith('int'): 
            formatters[key] = NumberFormatter(format='0')
        elif str(dtype).lower().startswith('float'): 
            formatters[key] = NumberFormatter(format='0.000')
        elif str(dtype).lower().startswith('bool') and bool_formater:
            formatters[key] = BooleanFormatter(icon='check-square')
            #if dtype == 'boolean': formatters[key] = StringFormatter(nan_format = 'NA') #BooleanFormatter() #{'type': 'tickCross', 'allowEmpty': True, 'tickElement': "<i class='fa fa-check'></i>",'crossElement':"<i class='fa fa-times'></i>"} #BooleanFormatter(icon='check-square')
        elif str(dtype).lower().startswith('datetime)'): 
            formatters[key] = DateFormatter()
    if (ICON in dtype_dict):
        formatters[ICON] = {'type': 'html'}
    return formatters

def _header_filters(dtype_dict):
    filters = {}
    for key, dtype in dtype_dict.items():
        if key not in [ICON]:  
            if str(dtype).lower().startswith('int'):    
                filters[key] = {'type': 'number', 'func': '=='}           
            elif str(dtype).lower().startswith('float'): 
                filters[key] = {'type': 'number', 'func': '=='}
            elif str(dtype).lower().startswith('bool') :
                filters[key] =  {'type': 'input', 'func': 'like', 'placeholder': 'Like..'}
                #filters[key] = {'type': 'tickCross', 'tristate': True, 'indeterminateValue': None}
                #filters[key] = {'type': 'list', 'valuesLookup': True}
            elif str(dtype).lower().startswith('string'): 
                filters[key] =  {'type': 'input', 'func': 'like', 'placeholder': 'Like..'}
    return filters

def _header_filters_crossdating(dtype_dict):
    filters = {}
    for key, dtype in dtype_dict.items():
        if str(dtype).lower().startswith('int'):    
            filters[key] = {'type': 'number', 'func': '=='}           
        elif str(dtype).lower().startswith('float'): 
            filters[key] = {'type': 'number', 'func': '>='}
        elif str(dtype).lower().startswith('bool') :
            filters[key] = {'type': 'tickCross', 'tristate': True, 'indeterminateValue': None}
        elif str(dtype).lower().startswith('string'): 
            filters[key] =  {'type': 'list', 'func': 'in', 'valuesLookup': True, 'sort': 'asc', 'multiselect': True}
    return filters

def _cell_editors(dtype_dict, edit=False):
    if edit == False:
        editors = {x:None for x in dtype_dict.keys()}
    else:
        editors = {}
        for key, dtype in dtype_dict.items():
            editors[key] = None
            if str(dtype).lower().startswith('int'):    
                editors[key] = NumberEditor(step=1)            
            elif str(dtype).lower().startswith('float'): 
                editors[key] = NumberEditor()
            elif str(dtype).lower().startswith('datetime64'): 
                editors[key] = 'date'
            elif str(dtype).lower().startswith('bool') :
                editors[key] = SelectEditor(options=['True', 'False', 'NA'])
            elif str(dtype).lower().startswith('string'): 
                editors[key] =  {'type': 'list', 'valuesLookup': True, 'autocomplete':True, 'freetext':True, 'allowEmpty':True, }
            else :
                logger.warning(f'Unknown dtype {dtype} for column {key}')
        if CATEGORY in dtype_dict:
            editors[CATEGORY] = SelectEditor(options=[SET, MEAN, MEASURE])
        for col in [ICON, ID, ID_CHILD, ID_MASTER, DATE_BEGIN_CE, DATE_END_CE, INCONSISTENT, ID_PARENT, COMPONENT_COUNT, 
                    DATA_INFO, DATA_LENGTH, DATA_TYPE, DATA_WEIGHTS, DATA_VALUES, DATA_SIGNATURES]:
            if col in dtype_dict:
                editors[col] = None            
    return editors

def tabulator(data):    
    return pn.widgets.Tabulator(data.reset_index(),
        pagination='local',
        header_filters=True, 
        sizing_mode='stretch_width',
        ) 
"""
def _hidden_columns(column_list=[ICON, KEYCODE, DATE_BEGIN, DATE_END, OFFSET], dtype_view=dtype_view):
    return list(set(dtype_view.keys()) - set(column_list)) 

def _position_columns(columns, hidden_columns):
    return columns + hidden_columns
"""

def computed_filed(data, icon, date):
    if date:
        data[DATE_BEGIN_CE] = data.apply(lambda x: row_date_ce(x, DATE_BEGIN), axis=1)
        data[DATE_END_CE] = data.apply(lambda x: row_date_ce(x, DATE_END), axis=1)
    if icon:
        data[ICON] =  data.apply(lambda x: category_html(x), axis=1)

def _get_selection(wtabulator) -> pd.DataFrame:
    """
    Returns the view of selectionned rows. 
    """
    if wtabulator.pagination == 'remote':
        selection = wtabulator.value.iloc[wtabulator.selection]
    else: # 'local'
        ids = [x for k, x in wtabulator._index_mapping.items() if k in wtabulator.selection]
        selection = wtabulator._processed.loc[ids,:]
    return selection
    
VALUES_PER_LINE = 20

def array2html(v):
    l = len(v)
    nl = (l + 1) // VALUES_PER_LINE + 2
    tmp = np.array([0.0] * nl * VALUES_PER_LINE, dtype=object)
    tmp[0:l] = v
    tmp[tmp == 0] = pd.NA
    tmp[len(v)] = ';'
    c = list(range(0, nl * VALUES_PER_LINE, VALUES_PER_LINE))
    return pd.DataFrame(tmp.reshape(-1, VALUES_PER_LINE).T, columns=c).T.style.format(precision=2)

def category_utf8(category):
    if category == SET:
        return '\U0001F4C1' # file folder
    elif category == MEASURE:
        return '\U0001F33F' # mapple leaf, seedling, 1F331, herbe : 1F33F, 219F, 100C9
    elif category == MEAN:
        return '\U0001F332' # Evergreen Tree 1F332, U0001F333 tree, 21C8

def category_html(row):
    if pd.notna(row[CATEGORY]):
        if row[CATEGORY] == MEASURE:
            return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAABoElEQVR4nGNgQAKhqwo5Y2ZXqERNqxBMWlhuWLmxZ2rF+q65xauaFRkIgaxlTdodu2dcXXBm1ZdpRxa8WHR+5ddd9/f+B+HWHVNuFa1oLYtdWC6HVXN9fT1Txfruxbse7P2PFd/f+3/b3V3/px5d8LByfdeS0tXtSSiaazb17Vp2cd0PnAag4e49M26FrgplBhuQMK9UdeG5lV+J1QzCG29s+1u3pXcvKMwY4hZUSU8/tuAlKQaA8NY7O/+XrmutY6ja0D1px709JGmG4fpNfXMYqtZ3T9l5nzwDyjd0TWYoXNVUvPba5r+kal5/Y+vv8nWdNQyV6zr7N9/e/o9UAxadW/09fmalBkPazDTWxq0T96MrIOStvgOzb8TPr+cAR2XBqhbvKYfnP9l6Z9f/hWdXvu/dP+tGxcbuffOOL/oNSkCzTy1907dv1rWefbMugeiO3dNPlK7vDEBJjTmrqhULV7UX561oNIWJteb7n2toT72XtrxamWBewAb64x0OgTBZmlsCbY0mJjjdAGEQm2QDGkMtVnTH2C0GYRAbl0IAsZMayBZxUF0AAAAASUVORK5CYII=">'
        elif row[CATEGORY] == MEAN:
            if not row[INCONSISTENT]:
                return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAACQElEQVR4nGNgQAKhqwo5Y2dVqJWsaAxu3dQ6v3JNfRnDfwZGmHzCvHJdBlwgd3Gl1qRdnVc3nJ/2dful6V/PPVj4f/e1Wb/KVzcsL1lVlxs/v16gaHXbnYzFNepYDWja1DILpAkdH7s9D4yr17Xe33hj29/azb2LMDQ3bmpumrK36zo2A2C4eWvP35339/xv2j7xbtKcUl645vj55QqrTk9+j08zCLdu7/u868He/917Z1zMnZjLDjcgbUGJ8oqTE9/h07zt0sz/i86u+gsyYOOtbf/K1nXUww1o2NA8+cy9BXhtn7q///+6a5v/gwzYdnfn/9K1nYfhBtSvb5py9j5+A2Yfnvx/651dYANAuGHrhN1wA0pX1RXvvTb7Ly7Nu67M+r/wzDK4ZhBec23zz7K1bXlgA2rWN0wHRRMuAybv6/+/8vJ6FAPWXd/yu3Rt+xFwIoufX89RsKxu/qEbc/5hM2DrpZn/l5xfhWLAppvb/pat76hFpMKJueztW1sOHLwx+9+BG7P/Td7c/H3/9dn/91+f87d1x8RPyJphuHf/7JtpM8v5EdE5M421eGVdPAj3Jjkdaa6PupGzvLaqbefUBxtvbUfRDIqJyYfnvcxZ3piDNVn3xzscAmGIweX8ecub0mqXNq7snln6v25W+dni1e3l6QuqpLFqbgm0NZqY4HQDhEFsqDBjY6hl24Icr/+t4dZb6+3tObBqBueLUIsV3TF2i0EYxAaJ1QZZWLdEWK8HibVF2axpCLVIhmkAAPbPI+veSxwUAAAAAElFTkSuQmCC">'
            else:
                return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAACPElEQVR4nGNgQAKhqwo5Y2dVqNUuSgqevCJsfvOyxDKG/wyMMPm0mYW6DLhA8dxcrWXrvK9e3mn49fYe7a9/jkj+f7RX7VfjkoTlDYuTcuPn1wuUz429kz8nQx2rARNXhM8CaULHHw/Kg3Hroqj7h+eJ/W2ZHbgIQ3P/iqimVes9rmMzAIb7FgX8PTeP53/XHJ+7SXNKeeGa4+eXK5zabvoen2YQnrDQ5/P5edz/p8xxvpg7MZcdbkDaglzlY9st3uHTfHOXzv9N89T/ggw4Olf4X9WciHq4AX0roib/PCyN1/aVa1z+H5gv9R9kwMl5Av+r5kQdhhvQuyJyyq8jUngN2LjWDqwRZAAIt8/x3w03oGFJcvHTfWp/cWm+v0fj/6aFOnDNILxvrtTPqrlReWADOpZHT/9wUAGn7ctWuf7fM18BxYBD8yR+V82JPgJOZPHz6zkqFqbNf71f6R82A67v0vm/fb4qigFH5on+rZobWQv3Ru7EXPbpq4MPvNqv9O/lfuV/K5a5f3++T+X/i/2qfycu8PqErBmGZ8y1u5k2s5wfEZ0z01irF6fFg3BvktOR9lr/G0UL0qr657o/ODJPFEUzKEDnzzV7WTg7OQdrsu6PdzgEwhCDy/mLZyemNU7yWzmhy/t/c4fX2Yo5ceXpCwqlsWpuCbQ1mpjgdAOEQWyoMGNjqGXbghyv/63h1lvr7e05sGoGgcZQixXdMXaLQRjEBonVBllYt0RYrweJtUXZrGkItUiGaQAAqI/Yr37DSpMAAAAASUVORK5CYII=">'
        elif row[CATEGORY] == SET: 
            return '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAb0lEQVR4nO2SMQqAMAxFi7uLnf6jt1U8iCfxWLpYKThYOtgogoMfMmTIyyf5zn1CwChpBSKwAbP3vq0GSFpDCN3RNsCUoBYH0VJpoaQhAziDkltJy21AMcMPcI9voDxIlyremEJxinJtkHqr63e0AxiSQjEOWJW+AAAAAElFTkSuQmCC">'
    return ''

def date_ce(date):
    if pd.notna(date):
        return str(int(date) -1)+' BCE' if date < 0 else str(int(date))+' CE'
    return ''

def row_date_ce(row, key):
    if pd.notna(row[key]):
        return date_ce(row[key])
    return ''
