"""
Package 
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import pandas as pd
import param
import numpy as np
import panel as pn
import copy
from panel.viewable import Viewer
from bokeh.models.widgets.tables import NumberEditor
from scipy.stats import  mode, kurtosis, skew, entropy

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters, array2html,
                                           _cell_formatters, _get_selection, _cell_transform, 
                                           category_html, row_date_ce, computed_filed)

class DatasetPackage(Viewer): 
    notify_package_change = param.Event()
    add_statistics = param.Boolean(default=ADD_STATISTICS, doc='Add statistics to the data')
    
    def __init__(self, dataset, parametres, editable=False, orderable=False, add_statistics=ADD_STATISTICS, **params): #param_columns, param_package, param_detrend=None, param_mean=None, editable=False, orderable=False, **params):
        super(DatasetPackage, self).__init__(**params)   
        #self.add_statistics = add_statistics
        self.param.watch(self.sync_data,  ['add_statistics'], onlychanged=True)

        self.param_column_package = parametres.column_package
        self.param_package = parametres.package
        self.param_detrend = parametres.detrend
        self.param_mean = parametres.mean
        
        dtype = self.param_column_package.get_dtype()
        columns_list = self.param_column_package.get_columns_hiddens()
        
        self._dt_data = pd.DataFrame(columns=columns_list)
        self._data = pd.DataFrame(columns=columns_list)
        self.dt_param = {}
        self.editable = editable
        self.accept_notification = True
        self.orderable = orderable
        self.bt_size = 100
        
        if self.param_detrend is not None:
            self.param_detrend.param.watch(self._sync_dt_data,  ['detrend', 'window_size', 'log'], onlychanged=True )
        
        if self.param_mean is not None:
            self.param_mean.param.watch(self._sync_dt_data,  ['biweight_mean', 'date_as_offset'], onlychanged=True)

        self.param_package.param.watch(self.sync_data, ['cambium_estimation_method', 'lambert_parameters', 'slope_resolution'], onlychanged=True)

        self.param_column_package.get_widgets().param.watch(self.sync_columns, ['value'], onlychanged=True)

        self.dataset = dataset
        self.dataset.param.watch(self.sync_dataset,  ['notify_reload', 'notify_synchronize', 'notify_packages'], onlychanged=True)

        self.wselection = pn.widgets.Select(name='Package: '+self.name, options=[], description='Select a package.')
        self.wselection.param.watch(self.sync_data,  ['value'], onlychanged=True)

        edit = _cell_editors(dtype, False)
        if self.editable:
            edit[TAG] = {'type': 'list', 'valuesLookup': True, 'autocomplete':True, 'freetext':True, 'allowEmpty':True, }

        self.wtabulator = pn.widgets.Tabulator(pd.DataFrame(columns=self.param_column_package.get_columns_hiddens()),
                                    hidden_columns=self.param_column_package.get_hiddens(), 
                                    text_align=_cell_text_align(dtype),
                                    editors=edit, 
                                    on_edit=self.on_edit,
                                    header_filters=_header_filters(dtype), 
                                    formatters=_cell_formatters(dtype),
                                    frozen_columns=[ICON, KEYCODE, 'index'], 
                                    show_index=False,
                                    pagination= 'local',
                                    page_size=100, #100000,
                                    selectable='checkbox', 
                                    sizing_mode='stretch_width',
                                    max_height=400,
                                    min_height=300,
                                    height_policy='max',
                                    row_content = self.get_row_content,
                                    ) 

        self.panel_tabulator = pn.Card(self.wtabulator, margin=(5, 0), collapsed=True, 
                                       sizing_mode='stretch_width',  
                                       title='Data '+self.name, collapsible=True,
                                       )
        
        stylesheet = 'p {padding: 0px; margin: 0px;}'
        self.dt_info = pn.pane.Alert('Detrend data is empty set', margin=(0, 0, 5, 5), align=('start', 'end'), stylesheets=[stylesheet])
        
        self._layout = pn.Column(pn.Row(self.wselection, self.dt_info), self.panel_tabulator)

    def set_package_name(self, package_name):
        """
        Set the package name in the GUI panel.

        Args:
            package_name (str): The name of the package to set.

        Returns:
            None
        """
        self.wselection.value = package_name

    def get_package_name(self):
        """
        Returns the name of the package selected in the GUI panel.
        
        Returns:
            str: The name of the selected package.
        """
        return self.wselection.value

    def get_row_content(self, series):
        """
        Returns a view of a datavalue.

        Parameters:
        - series: The series containing the data values.

        Returns:
        - pn.Tabs: A panel containing the data values in a tabular format.

        Raises:
        - Exception: If there is an error retrieving the data values.
        """        
        try:
            if isinstance(series[DATA_VALUES], np.ndarray):
                #perror(f'get_row_content {series.name}', series.info())
                lst = []
                lst.append((RAW, array2html(series[DATA_VALUES])))
                if SLOPE in series:
                    lst.append((SLOPE, array2html(series[SLOPE])))
                if self._dt_data is not None:
                    dt_type = self._dt_data.at[series.name, DATA_TYPE]
                    if dt_type != RAW:
                        lst.append((dt_type, array2html(self._dt_data.at[series.name, DATA_VALUES])))
                return pn.Tabs(*lst)
        except Exception as inst:
            return pn.pane.Markdown('Data error.')
        return pn.pane.Markdown('Data is missing.')

    def __panel__(self):
        return self._layout

    def sync_columns(self, event):
        """
        Set the hidden columns in the tabulator widget.

        Parameters:
        - event: The event object triggered by the column selector.

        Returns:
        None
        """
        self.param_column_package.update_tabulator(self.wtabulator)

    def sync_dataset(self, event):
        """
        Synchronizes the dataset with the GUI panel.

        This method updates the package selection options.

        Parameters:
            event (object): The event object triggered by the sync action.

        Returns:
            None
        """
        if not self.accept_notification:
            return
        lst = self.dataset.package_keys()
        columns_list = self.param_column_package.get_columns_hiddens()

        self._data = pd.DataFrame(columns=columns_list)
        self.wtabulator.value = pd.DataFrame(columns=columns_list)
        self._dt_data = pd.DataFrame(columns=columns_list)
        self.dt_param = {}
        self.wselection.options = ['None'] + lst
        if self.wselection.value not in self.wselection.options:
            self.wselection.value = 'None' 
        else:
            self.sync_data(event)
    
    def sync_data(self, event):
        """
        Synchronizes the data in the GUI panel with the dataset package.

        Args:
            event: The event object triggered by the synchronization action.

        Returns:
            None
        """
        if not self.accept_notification:
            return
        try:
            self._layout.loading = True
            columns_list = self.param_column_package.get_columns_hiddens()
            self._data = pd.DataFrame(columns=columns_list)
            package_name = self.get_package_name()
            if package_name != 'None':
                self._data = self.dataset.get_package_components(package_name, self.param_package.slope_resolution, self.param_package).reset_index()
                computed_filed(self._data, icon=True, date=True)
                self._data.reset_index(inplace=True)
                self._data = self._data.sort_values(by=KEYCODE)
        except Exception as inst:
            self._data = pd.DataFrame(columns=self.param_column_package.get_columns_hiddens())
        finally:
            #perror(f'sync_data:', self.name, self.add_statistics)
            if self.add_statistics:
                self.statistics()
            self.param_column_package.update_tabulator(self.wtabulator, self._data, self.add_statistics) 
            self._sync_dt_data(event)
            self._layout.loading = False

    def _sync_dt_data(self, event):
        """
        Synchronizes the detrended data with the current dataset.

        This method performs the detrending operation on the dataset based on the specified parameters.
        It updates the detrended data and the detrend information accordingly.

        Args:
            event: The event triggering the synchronization.

        Returns:
            None
        """
        def get_dt_param():
            dt_param = {}
            if self.param_detrend is not None:
                dt_param[DETREND] = self.param_detrend.detrend
                dt_param[DETREND_WSIZE] = self.param_detrend.window_size
                dt_param[DETREND_LOG] = self.param_detrend.log
                dt_param[MEANDATE_AS_OFFSET] = self.param_mean.date_as_offset
                dt_param[BIWEIGHT_MEAN] = self.param_mean.biweight_mean
            return dt_param
        
        try:
            self._layout.loading = True
            tmp_data = self.get_data()
            
            tmp_dt_data = tmp_data
            ids = tmp_data[ID_CHILD].unique().tolist()
            if len(ids) <= 0:
                tmp_dt_data = None
                tmp_data = None
                self.dt_info.object = 'Detrend data is empty set'
                self.dt_info.alert_type = 'warning'
            elif (self.param_detrend is  None) or (self.param_detrend.detrend == RAW):
                self.dt_info.object = 'Detrend data is raw data. '
                self.dt_info.alert_type = 'primary'
            else:
                if len(ids) != len(tmp_data[ID_CHILD]):
                    logger.warning(f'Duplicate series in package {self.name}')
                tmp_dt_data = tmp_data[[ID_CHILD, ID_PARENT, OFFSET, CAMBIUM_LOWER, CAMBIUM_ESTIMATED, CAMBIUM_UPPER, SLOPE]]
                res = self.dataset.detrend(ids, self.param_detrend.detrend, self.param_detrend.window_size, 
                                                    self.param_detrend.log, self.param_mean.date_as_offset, 
                                                    self.param_mean.biweight_mean, self.param_package.slope_resolution, self.param_mean.min_elements)      
                tmp_dt_data = tmp_dt_data.join(res, on=ID_CHILD, how='left')
                self.dt_info.alert_type = 'info'
                c = f'Detrend data is {self.get_data_type()} '
                c += ', '.join([f'{index}: {valeur}' for index, valeur in tmp_dt_data[CATEGORY].value_counts().items()]) +'.'
                self.dt_info.object = c
                
                if tmp_dt_data[INCONSISTENT].any():
                    self.dt_info.object += ' one or more series is inconsistent.'
                    self.dt_info.alert_type='warning'
                else:
                    self.dt_info.alert_type='primary'
        except Exception as inst:
            self.dt_info.object = f'Detrend data is {RAW} data'
            logger.error(f'_sync_dt_data: {inst}', exc_info=True)
        finally:
            self.dt_param = get_dt_param()
            self._dt_data = tmp_dt_data
            self.accept_notification = False
            self.param.trigger('notify_package_change')
            self.accept_notification = True
            self._layout.loading = False
    
    def on_cambium_estimation(self, event):
        """
        Handle the event when cambium estimation is triggered.

        Args:
            event: The event object representing the cambium estimation event.

        Returns:
            None
        """
        try:
            self._layout.loading = True
            edit = self.wtabulator.editors
            if self.param_package.cambium_estimation_method == 'user values':
                edit[CAMBIUM_LOWER] = NumberEditor(step=1)
                edit[CAMBIUM_ESTIMATED] = NumberEditor(step=1)
                edit[CAMBIUM_UPPER] = NumberEditor(step=1)
            else:
                edit[CAMBIUM_LOWER] = None
                edit[CAMBIUM_ESTIMATED] = None
                edit[CAMBIUM_UPPER] = None
            self.wtabulator.editors = edit

            self.do_cambium_estimation(self._data)
            self.wtabulator.value = _cell_transform(self._data)
            self.param.trigger('notify_package_change')
        except Exception as inst:
            logger.error(f'sync_data: {inst}', exc_info=True)
        finally:
            self._layout.loading = False

    def get_data(self):
        """
        Retrieves mean and tree from the wtabulator and returns it.

        If the wtabulator is empty, an empty DataFrame is returned.

        Returns:
            pandas.DataFrame: The retrieved data.
        """
        return self._data

    @property
    def data(self):
        """
        Returns the selected data from the tabulator widget.

        If there is no selection, returns the entire dataset.

        Returns:
            pandas.DataFrame: The selected data.
        """
        if (self._data is None) or len(self._data) == 0:
            return None
        d = _get_selection(self.wtabulator)
        
        ids = self.wtabulator.current_view.index if len(d) <= 0 else d.index
        df = self._data.loc[ids,:]     
        return df.loc[df[CATEGORY].isin([MEAN, MEASURE]),:]

    def get_data_type(self):
        """
        Returns the detrend data as a string.

        Returns:
            str: The detrend data type as a string.
        """
        if (self.param_detrend is  None) or (self.param_detrend.detrend == RAW):
            return f'{RAW}'
        if self.param_detrend.log and (self.param_detrend.detrend != BP73):
            return f'log({self.param_detrend.detrend}), ws: {self.param_detrend.window_size}. '
        
        return f'{self.param_detrend.detrend}, ws: {self.param_detrend.window_size}. '
    
    @property
    def dt_data(self):
        """
        Returns a subset of the detrend dataset based on the selected indices.

        If no indices are selected, the entire dataset is returned.

        Returns:
            pandas.DataFrame: Subset of the dataset.
        """
        if (self._dt_data is None) or len(self._dt_data) == 0:
            return None
        d = _get_selection(self.wtabulator)
        
        ids = self.wtabulator.current_view.index if len(d) <= 0 else d.index
        df = self._dt_data.loc[ids,:]     
        return df.loc[df[CATEGORY].isin([MEAN, MEASURE]),:]

    def _apply_log(self, array):
        x = np.log(array)
        x[np.isinf(x)] = np.nan
        return x

    @property
    def log_data(self):
        """
        Apply logarithm to the data values in the dataset.

        Returns:
            DataFrame: A copy of the dataset with logarithm applied to the data values.
        """
        
        if (self._data is None) or len(self._data) == 0:
            return None
        d = _get_selection(self.wtabulator)

        df = copy.deepcopy(self.data)
        df[DATA_VALUES] = df[DATA_VALUES].apply(self._apply_log)
        ids = self.wtabulator.current_view.index if len(d) <= 0 else d.index
        df = df.loc[ids,:]     
        return df.loc[df[CATEGORY].isin([MEAN, MEASURE]),:]

    def get_data_values_id(self, id):
        def get_data(df, id):
            if df is None:
                return None
            return df.loc[df[ID_CHILD] == id, DATA_VALUES].iloc[0]
        
        data = get_data(self.data, id)
        
        dt_data = get_data(self.dt_data, id)
        log_data = get_data(self.log_data, id) 
        
        return data, dt_data, log_data

    def on_edit(self, event):
        """
        Handle the event when a cell is edited.

        Args:
            event: The event object representing the edit event.
        """
        try:
            self.accept_notification = False
            self._layout.loading = True
            col = event.column
            row = self.wtabulator.value.iloc[event.row]
            new = event.value
            id_parent, id_child = row[ID_PARENT], row[ID_CHILD]
            self._data.at[row.name, col] = new
            self._dt_data.at[row.name, col] = new
            if col == TAG:
                current_package = self.get_package_name()
                self.dataset.edit_sequence(id_child, col, new, notify=True)
            else:
                self.param_package.cambium_estimation_method = 'user values'
        except Exception as inst:
            self.wtabulator.patch({event.column: [(event.row, event.old)]})
            logger.error(f'on_edit: {inst}', exc_info=True)
        finally:            
            self._layout.loading = False    
            self.param.trigger('notify_package_change')
            self.accept_notification = True
    
    def save(self):
        """
        Saves the package using the current tabulator value.

        Note: This method does not trigger the 'notify_package_change' event.

        Returns:
            None
        """
        save_package(self._data, self.get_package_name(), self.dataset)

    def statistics(self):
        """
        Calculate statistics for the dataset.

        Args:
            columns (list, optional): List of columns to include in the statistics. Defaults to [ID, KEYCODE].
            stat_columns (list, optional): List of additional statistics columns to include. Defaults to [DATA_NAN].
            data (pandas.DataFrame, optional): Data to calculate statistics on. Defaults to None.

        Returns:
            pandas.DataFrame: DataFrame containing the calculated statistics.

        """
        if self._data is not None:
            # Filtrer les lignes où DATA_LENGTH est non nul et supérieur à 0
            valid_rows = self._data[DATA_LENGTH].notna() & (self._data[DATA_LENGTH] > 0)
            if valid_rows.sum() > 0:
                values = self._data.loc[valid_rows, DATA_VALUES]                
                self._data.loc[valid_rows, STAT_MEAN] = values.apply(lambda x: np.nanmean(x))
                self._data.loc[valid_rows, STAT_MEDIAN] = values.apply(lambda x: np.nanmedian(x))
                self._data.loc[valid_rows, STAT_MODE] = values.apply(lambda x: mode(x, nan_policy='omit')[0])
                self._data.loc[valid_rows, STAT_STD] = values.apply(lambda x: np.nanstd(x))
                self._data.loc[valid_rows, STAT_VAR] = values.apply(lambda x: np.nanvar(x))
                self._data.loc[valid_rows, STAT_MIN] = values.apply(lambda x: np.nanmin(x))
                self._data.loc[valid_rows, STAT_MAX] = values.apply(lambda x: np.nanmax(x))
                self._data.loc[valid_rows, STAT_PERC25] = values.apply(lambda x: np.nanpercentile(x, 25))
                self._data.loc[valid_rows, STAT_PERC50] = values.apply(lambda x: np.nanpercentile(x, 50))
                self._data.loc[valid_rows, STAT_PERC75] = values.apply(lambda x: np.nanpercentile(x, 75))
                self._data.loc[valid_rows, STAT_SUM] = values.apply(lambda x: np.nansum(x))
                self._data.loc[valid_rows, STAT_KURTOSIS] = values.apply(lambda x: kurtosis(x, nan_policy='omit'))
                self._data.loc[valid_rows, STAT_SKEWNESS] = values.apply(lambda x: skew(x, nan_policy='omit'))
                self._data.loc[valid_rows, STAT_ENTROPY] = values.apply(lambda x: entropy(x, nan_policy='omit'))

def save_package(dataframe, package_name, dataset):
    
    def get_missing_key(df, key):
        mask = df[key].isna()
        return  mask, np.sum(mask)

    def get_missing_values(df):
        mask = (df[CATEGORY] != SET) & df[DATA_VALUES].isna()
        return mask, np.sum(mask)
    
    if package_name == '':
        logger.warning(f'Selection name is empty')
    else:
        df = dataframe
        paires = list(set(zip(df[ID_PARENT], df[ID_CHILD])))   
               
        mask, smask = get_missing_key(df, DATE_BEGIN)
        if smask > 0:       
            logger.warning(f'Some {DATE_BEGIN} is missing')
        mask, smask  = get_missing_key(df, OFFSET)
        if smask > 0:       
            logger.warning(f'Some {OFFSET} is missing')
        mask, smask = get_missing_values(df)
        if smask > 0:       
            logger.warning(f'Some {DATA_VALUES} is missing, remove them')
            df = df.loc[~mask]
        if len(df) != 0:      
            dataset.set_package(package_name, paires)
            logger.info(f'Save selection {package_name}')
        else:
            logger.warning(f'Selection is empty, delete package.')
            #dataset.delete_package(package_name)


                
            

        



