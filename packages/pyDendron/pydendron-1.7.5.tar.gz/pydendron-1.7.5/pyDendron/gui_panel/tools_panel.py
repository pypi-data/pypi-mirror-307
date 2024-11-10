"""
Dataset tools
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

import pandas as pd
from pathlib import Path
import panel as pn
import param
import copy
import warnings
import os
from panel.viewable import Viewer
from io import BytesIO

from pyDendron.dataset import Dataset
from pyDendron.alien.io_besancon import IOBesancon
from pyDendron.alien.io_heidelberg import IOHeidelberg
from pyDendron.alien.io_rwl import IORWL
from pyDendron.alien.io_sylphe import IOSylphe
from pyDendron.alien.io_dendronIV import IODendronIV
from pyDendron.alien.io_tridas import IOTridas
from pyDendron.tools.alignment import Alignment
from pyDendron.dataname import *
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters,
                                           _cell_formatters, unique_filename,
                                           )

from pyDendron.app_logger import logger, notification_stream, perror
from pyDendron.gui_panel.my_viewer import MyViewer
from pyDendron.mean import data2col


class ToolsPanel(MyViewer):
    """ Tools to manage dataset. """
    path = param.Foldername('./', doc='Output path of the saved package.')
    filters = param.List(['*.p', '*.xlsx', '*.json'], doc='glob filter')
    encoding = param.Selector(default='utf-8', objects=['utf-8', 'latin1'], doc='file char encoding')
    tolerance = param.Integer(default=5, bounds=(1, 10), step=1, doc='Number of equal values tolerated.')
        
    def __init__(self, dataset_selector, dataset, parameters, dendron_info, cfg_path, tmp_path, **params):
        super().__init__(cfg_path, **params)
        self.dataset = dataset
        self.parameters = parameters
        self.tmp_path = tmp_path
        #self.wcolumns = parameters.columns.get_widgets()
        self.param_columns = parameters.column_package

        self.dataset_package = DatasetPackage(dataset, parameters, name='tools')
        self.dendron_info = dendron_info
        self.path = self.dendron_info.dataset_path
        self.www = self.dendron_info.www
        self.import_dataset = None
        self.outliers = []
        self.dataset_selector = dataset_selector
        
        self.bt_size = 90

        self._layout = pn.Tabs(
            ('Import', self._import()),
            ('Export', self._export()),
            ('Merge', self._merge()),
            ('Detect', self._validate()),
            ('Edit rings', self._edit_ring()),
            name=self.name,
             dynamic=True, styles={'font-size': '15px'})

    def get_sidebar(self, visible=True):   
        return pn.Card(pn.Param(self, show_name=False),                 
                margin=(5, 0), 
                sizing_mode='stretch_width', 
                title='Tools',
                collapsed=True, visible=visible)
  
    def get_options(self):
        """ Retrieve file options based on filters. """
        options = {}
        for flt in self.filters:
            for file in Path(self.dendron_info.dataset_path).glob(flt):
                options[f'\U0001F4E6 {str(file.name)}'] = file
        return options
    
    def _import(self):

        def on_import(event):               
            """ Handle importing of datasets. """  
            def get_input_io(fn):
                tmp = fn.lower()
                if tmp.endswith('.mdb'):
                    return IOSylphe(base_directory=self.tmp_path)
                elif tmp.endswith('.fh') or tmp.endswith('.fh.zip'):
                    return IOHeidelberg()
                elif tmp.endswith('.rwl') or tmp.endswith('.crn') or tmp.endswith('.crn.zip') or tmp.endswith('.rwl.zip'):
                    return IORWL()
                elif tmp.endswith('.bes') or tmp.endswith('.bes.zip'):
                    return IOBesancon()
                elif tmp.endswith('.dxml.zip'):
                    return IODendronIV(base_directory=self.tmp_path)
                elif tmp.endswith('.tridas.zip') or tmp.endswith('tridas.xml'):
                    return IOTridas(base_directory=self.tmp_path)
                elif tmp.endswith('.p') or tmp.endswith('.json') or tmp.endswith('.xlsx'):
                    return Dataset(cfg_tmp=self.tmp_path)
                raise ValueError(f'Unknown file format {fn}, must be: mdb, fh, fh.zip, rwl, rwl.zip, crn, crn.zip, bes, bes.zip, Dxml.zip, tridas.zip, p, json, xlsx.')
            
            self._layout.loading = True
            try:    
                for fn, buffer in file_input.value.items():
                    io_import = get_input_io(fn)
                    parent_keycode = Path(fn).stem
                    notifications = pn.config.notifications
                    pn.config.notifications = False
                    ds = io_import.read_buffer(parent_keycode, buffer, file_input.mime_type[fn])
                    if self.import_dataset is None:
                        self.import_dataset = ds  
                    else:
                        self.import_dataset.append(ds, notify=False)
                    pn.config.notifications = notifications
                
                if self.import_dataset is not None:
                    #perror("get_data")
                    wtabulator.value = self.import_dataset.sequences
                else:
                    #perror("empty data")
                    wtabulator.value = pd.DataFrame(columns=list(dtype.keys()))
            except Exception as inst:
                logger.error(f'on_import : {inst}', exc_info=True)
            finally:
                self._layout.loading = False
                                
        
        def on_save(event):
            """ Handle saving of the imported dataset. """
            if self.import_dataset is None:
                raise ValueError('The imported dataset is empty.')
            if dataset_name.value == '':
                raise ValueError('The dataset name is empty.')      
            self._layout.loading = True
            try:
                fn = unique_filename(Path(self.dendron_info.dataset_path) / dataset_name.value)      
                self.import_dataset.dump(fn)
                #logger.info(f'Save done in dataset {fn}')
                self.dataset_selector.on_refresh(event)
            finally:
                self._layout.loading = False

        def on_merge(event):
            """ Handle saving of the imported dataset. """
            if self.import_dataset is None:
                raise ValueError('The imported dataset is empty.')
            if self.dataset is None:
                raise ValueError('The dataset is empty.')            
            self._layout.loading = True
            try:
                self.dataset.append(self.import_dataset)
                #logger.info('Merge done in current dataset')
            finally:
                self._layout.loading = False

        
        """ Create the import tab layout. """

        def on_clear_import(event):
            self.import_dataset = None
            file_input.value = {}
            wtabulator.value = pd.DataFrame(columns=list(dtype.keys()))

        def sync_columns(event):
            self.param_columns.update_tabulator(wtabulator)
            # wtabulator.hidden_columns = _hidden_columns(self.wcolumns.value)
            # if wtabulator.value is not None:
            #     wtabulator.value = wtabulator.value[_position_columns(self.wcolumns.value, wtabulator.hidden_columns)]

        option = ['Besançon', 'Heidelberg', 'RWL']
        option += ['Sylphe', 'DendronIV', 'pyDendron']
        
        file_input = pn.widgets.FileDropper(sizing_mode='stretch_both', multiple=True, max_file_size='1000MB')
        #file_input.param.watch(on_file_input, ['value'], onlychanged=True)
        
        #file_format = pn.widgets.RadioBoxGroup(name='Format', options=option, inline=True, align=('end', 'end'))
        bt_import = pn.widgets.Button(name='Import', icon='import', button_type='primary', align=('end', 'end'), description='Import the selected file.')
        bt_import.on_click(on_import)
        bt_clear_import = pn.widgets.Button(name='Clear import', icon='trash', button_type='primary', align=('end', 'end'), description='clear imported data.')
        bt_clear_import.on_click(on_clear_import)
        
        dtype = self.param_columns.get_dtype()
        wtabulator = pn.widgets.Tabulator(
                                    pd.DataFrame(columns=self.param_columns.get_columns_hiddens()),
                                    hidden_columns=self.param_columns.get_hiddens(), 
                                    text_align=_cell_text_align(dtype),
                                    editors=_cell_editors(dtype), 
                                    header_filters=_header_filters(dtype), 
                                    formatters=_cell_formatters(dtype),
                                    sizing_mode='stretch_width',
                                    frozen_columns=[ICON, KEYCODE], 
                                    selectable='checkbox',
                                    pagination='local',
                                    page_size= 1000, 
                                    max_height=600,
                                    min_height=300,
                                    height_policy='max',
                                    layout='fit_data_fill',
                                    margin=(0,0),
                                    )
        self.param_columns.get_widgets().param.watch(sync_columns, ['value'], onlychanged=True, queued=True)
        
        dataset_name = pn.widgets.TextInput(name='Dataset name', placeholder='dataset_import.p', description='Enter the dataset name.')
        bt_save = pn.widgets.Button(name='Create', icon='file-plus', button_type='primary', align=('start', 'end'), description='Save the imported dataset in a new dataset.')
        bt_save.on_click(on_save)
        bt_merge = pn.widgets.Button(name='Merge in current dataset', icon='arrow-merge', button_type='primary', align=('start', 'end'), description='Merge the imported dataset in the current dataset.')
        bt_merge.on_click(on_merge)
        return pn.Column(file_input,
                        pn.Row(bt_clear_import, bt_import ),
                        wtabulator,
                        pn.Row(dataset_name, bt_save),
                        bt_merge
                    )

    def _export(self):
        def save_dataset_to_file():
            nonlocal fn_dataset
            if self.dataset.filename is None:
                logger.warning('Dataset is not loaded.')
                return
            fn_dataset = Path(self.tmp_path) / Path(self.dataset.filename).name
            if file_export_format.value == 'Pickle':
                fn_dataset = fn_dataset.with_suffix('.p')
            elif file_export_format.value == 'JSON':
                fn_dataset = fn_dataset.with_suffix('.json')
            else:
                fn_dataset = fn_dataset.with_suffix('.xlsx')
            fn_dataset = unique_filename(fn_dataset)
            #logger.info(f'Tools export, filename: {fn_dataset} (format {file_export_format.value})')
            self.dataset.dump(fn_dataset)
            #self.dataset_selector.on_refresh(event)
        
        def on_export_dataset():
            nonlocal fn_dataset
            try:
                save_dataset_to_file()
                bt_export_dataset.filename = fn_dataset.name
                output = BytesIO()
                with open(fn_dataset, 'rb') as file:
                    output.write(file.read())
                output.seek(0)
                fn_dataset.unlink()
                return output
            except Exception as inst:
                logger.error(f'on_excel: {inst}', exc_info=True)
            
        def on_export_package():
            nonlocal fn_package
            try:
                save_package_to_file()
                bt_export_package.filename = fn_package.name
                output = BytesIO()
                with open(fn_package, 'rb') as file:
                    output.write(file.read())
                output.seek(0)
                fn_package.unlink()
                return output
            except Exception as inst:
                logger.error(f'on_excel: {inst}', exc_info=True)
    
        def save_package_to_file():
            nonlocal fn_package
            if self.dataset.filename is None:
                logger.warning('Dataset is not loaded.')
                return
            data = dataset_package.data
            if data is None:
                logger.warning('No package to export.')
                return
            package = dataset_package.get_package_name().replace(os.sep, '_')
            if file_export_format_package.value == 'Besançon':
                bes = IOBesancon()
                fn_package = Path(self.tmp_path) / f'{package}.bes'
                bes.write_package(self.dataset, data, fn_package)
                #logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
            elif file_export_format_package.value == 'Heidelberg':
                fh = IOHeidelberg()
                fn_package = Path(self.tmp_path) / f'{package}.fh'
                fh.write_package(self.dataset, data, fn_package)
                #logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
            # elif file_export_format_package.value == 'RWL':
            #     rwl = IORWL()
            #     fn = Path(self.path) / f'{package}.rwl'
            #     rwl.write_package(self.dataset, data, fn)
            #     #logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
            elif file_export_format_package.value == 'Excel Rows':
                fn_package = Path(self.tmp_path) / f'{package}_row.xlsx'
                with pd.ExcelWriter(fn_package) as writer:
                    data.to_excel(writer, sheet_name=package, merge_cells=False, float_format="%.6f")
                #logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
            elif file_export_format_package.value == 'Excel Columns':
                fn_package = Path(self.tmp_path) / f'{package}_col.xlsx'
                if data[DATE_BEGIN].notna().any():
                    #perror('data2col date_begin')
                    data_col = data2col(data, use_offset=True, key_offset=DATE_BEGIN, add_index=True)
                    data_col_w = data2col(data, value_key=DATA_WEIGHTS , use_offset=True, key_offset=DATE_BEGIN, raise_error=False, add_index=True)
                    data_col_s = data2col(data, value_key=DATA_SIGNATURES, use_offset=True, key_offset=DATE_BEGIN, raise_error=False, add_index=True)
                elif data[OFFSET].notna().any():
                    #perror('data2col offset')
                    data_col = data2col(data, use_offset=True, key_offset=OFFSET, add_index=True)
                    data_col_w = data2col(data, value_key=DATA_WEIGHTS, use_offset=True, key_offset=OFFSET, raise_error=False, add_index=True)
                    data_col_s = data2col(data, value_key=DATA_SIGNATURES,  use_offset=True, key_offset=OFFSET, raise_error=False, add_index=True)
                else:
                    #perror('data2col ')
                    data_col = data2col(data, use_offset=False, add_index=True)
                    data_col_w = data2col(data, value_key=DATA_WEIGHTS, use_offset=False, raise_error=False, add_index=True)
                    data_col_s = data2col(data, value_key=DATA_SIGNATURES, use_offset=False, raise_error=False, add_index=True)

                with pd.ExcelWriter(fn_package) as writer:
                    data[excel_columns].T.to_excel(writer, sheet_name='Info', merge_cells=False, float_format="%.6f")
                    data_col.to_excel(writer, sheet_name=DATA_VALUES, merge_cells=False, float_format="%.6f")
                    data_col_w.to_excel(writer, sheet_name=DATA_WEIGHTS, merge_cells=False, float_format="%.6f")
                    data_col_s.to_excel(writer, sheet_name=DATA_SIGNATURES, merge_cells=False, float_format="%.6f")
                #logger.info(f'Tools export {package}, filename: {fn} (format {file_export_format_package.value})')
                    
                #self.dataset_selector.on_refresh(event)
            else:
                logger.warning(f'Unknown format {file_export_format_package.value}')
                return
             
        def on_stats(event):
            try:
                dataset_package.add_statistics = cb_stats.value
                perror(f'Add statistics {cb_stats.value}')
            except Exception as inst:
                logger.error(f'on_excel: {inst}', exc_info=True)     
             
             
                 
        file_export_format = pn.widgets.RadioBoxGroup(name='file format', options=['Pickle', 'Excel', 'JSON'], inline=True, align=('start', 'end'))

        bt_export_dataset = pn.widgets.FileDownload(callback=on_export_dataset, filename='dataset.tmp', embed=False, 
                                                label='Download', icon='file-export', button_type='primary', 
                                                width=self.bt_size, align=('start', 'end'), description='Download exported package.')
        
        #bt_save_dataset.on_click(save_dataset_to_file)
        
        file_export_format_package = pn.widgets.RadioBoxGroup(name='file format', options=['Heidelberg', 'Besançon', 'Excel Columns', 'Excel Rows'], inline=True, align=('start', 'end'))
        #bt_save_dataset_package = pn.widgets.Button(name='Export', icon='file-arrow-right', button_type='primary', align=('start', 'end'), width=self.bt_size, description='Export the selected dataset.')
        #bt_save_dataset_package.on_click(save_package_to_file)
        fn_package = ''
        fn_dataset = ''
        
        cb_stats = pn.widgets.Checkbox(name='Add statistics', align=('start', 'end'))
        cb_stats.param.watch(on_stats,  ['value'], onlychanged=True)

        
        bt_export_package = pn.widgets.FileDownload(callback=on_export_package, filename='package.tmp', embed=False, 
                                                label='Download', icon='file-export', button_type='primary', 
                                                width=self.bt_size, align=('start', 'end'), description='Download exported package.')
        
        dataset_package = self.dataset_package
        return pn.Column(
                    pn.pane.Markdown('### Export current dataset'),
                    file_export_format,
                    bt_export_dataset,
                    pn.pane.Markdown('### Export current package'),
                    dataset_package,
                    cb_stats,
                    file_export_format_package,
                    #bt_save_dataset_package,
                    bt_export_package,
        )
  
    def _merge(self):
        """ Create the dataset merge tab layout. """
        
        def load(dataset_src_name1, dataset_src_name2):
            dataset_src = Dataset()
            dataset_src.load(dataset_src_name1.value)
            
            dataset_dest = Dataset()
            dataset_dest.load(dataset_src_name2.value)
            
            return  dataset_src, dataset_dest

        def on_merge(event):
            """ Handle merging of datasets. """
            try:
                self._layout.loading = True
                fn = unique_filename(Path(self.dendron_info.dataset_path) / dataset_dest_name.value)
                #perror(f'Merge {dataset_src_name1.value} and {dataset_src_name2.value} in {fn}')
                if dataset_src_name1.value == dataset_src_name2.value:
                    logger.warning('The source datasets are the same.')
                    return
                dataset_src1, dataset_src2 = load(dataset_src_name1, dataset_src_name2)
                dest = dataset_src1.clone()
                dest.filename = fn
                dest.append(dataset_src2)
                dest.dump()
                #logger.info(f'Merge done into {fn}')
            except Exception as inst:
                logger.error(f'on_duplicate2 : {inst}', exc_info=True)
            finally:
                self._layout.loading = False

        options = self.get_options()
        
        dataset_src_name1 = pn.widgets.Select(name='1st dataset name', options=options, description='Select the first dataset to merge.')
        dataset_src_name2 = pn.widgets.Select(name='2rd dataset name', options=options, description='Select the second dataset to merge.')
        dataset_dest_name = pn.widgets.TextInput(value='dataset_import.p', name='Destination Dataset name', description='Enter the destination dataset name.')

        bt_merge = pn.widgets.Button(name='Merge', icon='arrow-merge', button_type='primary', align=('start', 'end'), width=self.bt_size, description='Merge the 2 datasets.')
        bt_merge.on_click(on_merge)

        return pn.Column(
                        pn.Row(dataset_src_name1, dataset_src_name2), 
                        pn.Row(dataset_dest_name, bt_merge)
                    )
        
    def _validate(self):

        parent_orphans = []
        child_orphans = []
        seq_orphans = []
                
        def on_duplicate(event):
            try:
                self._layout.loading = True
                counts = self.dataset.sequences[KEYCODE].value_counts()
                lst = list(counts[counts > 1].to_dict().keys())
                wduplicate.value =  '\n'.join(lst) if len(lst) > 0 else 'No duplicate'
            except Exception as inst:
                logger.error(f'on_duplicate2 : {inst}', exc_info=True)
            finally:
                self._layout.loading = False

        def on_duplicate2(event):
            try:
                self._layout.loading = True
                data = dataset_package.data
                if data is None:
                    logger.warning('No package.')
                    return
                res = alignment.ndiff_sequences(data, n=self.tolerance)
                txt = ''
                for id_i, id_j, cost , insertions, deletions, substitutions, n, err in res:
                    #id_i, id_j, cost , insertions, deletions, substitutions, n, ch]
                    txt += f'{err} (ins: {insertions}, del:{deletions}, sub:{substitutions})\n'
                wduplicate2.value = txt
                progress.value = 100
            except Exception as inst:
                logger.error(f'on_duplicate2 : {inst}', exc_info=True)
            finally:
                self._layout.loading = False
        
        def on_progress(event):
            progress.value = alignment.rate
            
        def on_outliers(event):
            data = dataset_package.dt_data
            if data is None:
                logger.warning('No package.')
                return
            txt = ''
            self.outliers.clear()
            
            for _, row in data.iterrows():
                vec = row[DATA_VALUES]
                id = row[ID_CHILD]
                med, std = np.nanmedian(vec), np.nanstd(vec)
                cut_off = std * 5 
                lower, upper = med - cut_off, med + cut_off
                keycode = row[KEYCODE]
                for i, x in enumerate(vec):
                    if (x < lower) or (x > upper) or (abs(x) <= 1e-7):
                        txt += f'Outlier {x} in "{keycode}" at index {i} (lower={round(lower, 3)}, median={round(med, 3)}, upper={round(upper, 3)})\n'
                        self.outliers.append(({ID: id, KEYCODE: keycode, 'Index':i, 'Value': x}))
            woutliers.value = txt

        def on_set_nan(event):
            for d in self.outliers:
                self.dataset.sequences.at[d[ID], DATA_VALUES][d['Index']] = np.nan
            self.dataset.notify_changes('outliers')
            
        def on_orphans(event):
            nonlocal parent_orphans, child_orphans, seq_orphans
            try:        
                self._layout.loading = True
                parent_orphans.clear()
                child_orphans.clear()
                seq_orphans.clear()
                parent_orphans += self.dataset.get_orphans_components(level=ID_PARENT)
                child_orphans += self.dataset.get_orphans_components(level=ID_CHILD)
                seq_orphans += self.dataset.get_orphans_sequences()
                worphans.value = f'Components {ID_PARENT}:\n{parent_orphans}\n Components {ID_CHILD}:\n{child_orphans}\n Sequences:\n{seq_orphans}'
            except Exception as inst:
                logger.error(f'on_orphans : {inst}', exc_info=True)
            finally:
                self._layout.loading = False
        
        def on_delete_orphans(event):
            try:
                self._layout.loading = True
                if len(parent_orphans) > 0:
                    self.dataset.drop_orphans_components(parent_orphans)
                if len(child_orphans) > 0:
                    self.dataset.drop_orphans_components(child_orphans)
                on_orphans(event)
            except Exception as inst:
                logger.error(f'on_delete_orphans : {inst}', exc_info=True)
            finally:
                self._layout.loading = False
        
        def on_check(event):
            try:
                self._layout.loading = True
                problems = []
                for id, row in self.dataset.sequences.iterrows():
                    keycode = row[KEYCODE]
                    data = row[DATA_VALUES]
                    #perror(f'Check {keycode} {data}')
                    if isinstance(data, np.ndarray):
                        ldata = len(data)
                        if ldata != row[DATA_LENGTH]:
                            problems.append(f'In {keycode}, length {len(data)} different from {row[DATA_LENGTH]}.')
                        if pd.notna(row[SAPWOOD] ):
                            if row[SAPWOOD] >= ldata :
                                problems.append(f'In {keycode}, {SAPWOOD} value {row[SAPWOOD]} is greater than data lenght.')
                            elif row[SAPWOOD] < 0 :
                                problems.append(f'In {keycode}, {SAPWOOD} value {row[SAPWOOD]} is negative.')
                    if pd.notna(row[DATE_BEGIN]) and pd.notna(row[DATE_END]):
                        if row[DATE_BEGIN] > row[DATE_END]:
                            problems.append(f'In {keycode}, {DATE_BEGIN} {row[DATE_BEGIN]} is greater than {DATE_END}')
                        if isinstance(data, np.ndarray):
                            ldata = len(data)
                            if (row[DATE_END] - row[DATE_BEGIN] + 1) != ldata:
                                problems.append(f'In {keycode}, {DATE_END} - {DATE_BEGIN} + 1 = {row[DATE_END] - row[DATE_BEGIN] + 1} different from data length {ldata}.')                       
                wcheck.value = '\n'.join(problems) if len(problems) > 0 else 'No problem detected.'
            except Exception as inst:
                logger.error(f'on_check : {inst}', exc_info=True)
            finally:
                self._layout.loading = False
        
        dataset_package = self.dataset_package
        bt_duplicate = pn.widgets.Button(name=f'Detect duplicate {KEYCODE}', icon='bolt', button_type='primary', description='Detect duplicate in the current dataset.')
        bt_duplicate.on_click(on_duplicate)
        wduplicate = pn.widgets.TextAreaInput(name=f'Duplicate {KEYCODE}', value='', sizing_mode='stretch_width', description='List of duplicate keycodes.')

        alignment = Alignment()
        bt_duplicate2 = pn.widgets.Button(name=f'Detect duplicate {DATA_VALUES}', icon='bolt', button_type='primary', description=f'Detect duplicate {DATA_VALUES} in the current package. The tolerance is set to {self.tolerance}.')
        bt_duplicate2.on_click(on_duplicate2)
        progress = pn.indicators.Progress(name='Run', value=0, sizing_mode='stretch_width', disabled=True, bar_color='primary')
        alignment.param.watch(on_progress, ['rate'], onlychanged=True)
        wduplicate2 = pn.widgets.TextAreaInput(name=f'Duplicate {DATA_VALUES}', value='', sizing_mode='stretch_width', description=f'List of {KEYCODE} with duplicate values.')

        bt_outliers = pn.widgets.Button(name=f'Detect outliers {DATA_VALUES}', icon='bolt', button_type='primary', description=f'Detect outliers in the current package. Outliers are values outside 5 standard deviations from the median.')
        bt_outliers.on_click(on_outliers)
        woutliers = pn.widgets.TextAreaInput(name=f'Outliers {DATA_VALUES}', value='', sizing_mode='stretch_width', description='List of {KEYCODE} with outlier values.')
        bt_set_nan = pn.widgets.Button(name='Set value to NaN', icon='bolt', button_type='primary', description='Set the outlier values to NaN.')
        bt_set_nan.on_click(on_set_nan)

        bt_orphans = pn.widgets.Button(name='Detect', icon='bolt', button_type='primary', description='Detect orphan indexes in database.')
        bt_orphans.on_click(on_orphans)
        worphans = pn.widgets.TextAreaInput(name=f'{KEYCODE} orphans', value='', sizing_mode='stretch_width', description='List of detected orphans.')
        bt_delete_orphans = pn.widgets.Button(name='Delete', icon='delete', button_type='primary', description='Delete detected orphans.')
        bt_delete_orphans.on_click(on_delete_orphans)

        bt_check = pn.widgets.Button(name='Check', icon='bolt', button_type='primary', description=f'Check {DATA_LENGTH}, {SAPWOOD}, date.')
        wcheck = pn.widgets.TextAreaInput(name=f'Problems', value='', sizing_mode='stretch_width', description='List of detected problems.')
        bt_check.on_click(on_check)

        return pn.Tabs(
            (f'Duplicate {KEYCODE}', pn.Column(bt_duplicate, wduplicate)),
            (f'Duplicate {DATA_VALUES}', pn.Column(dataset_package, pn.Row(bt_duplicate2,  progress), wduplicate2)),
            (f'Outliers {DATA_VALUES}', pn.Column(dataset_package, bt_outliers, woutliers, bt_set_nan)),
            ('Orphans', pn.Column(bt_orphans, worphans, bt_delete_orphans)),
            ('Check data', pn.Column(bt_check, wcheck)),
            dynamic=True
        )

    def _edit_ring(self):
        def on_insert(event):
            if len(wtabulator.selection) > 0:
                df = wtabulator.value
                i = wtabulator.selection[0]
                with warnings.catch_warnings():
                    # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                    warnings.filterwarnings("ignore", category=FutureWarning)
                    wtabulator.value = pd.concat([df.iloc[:i], pd.DataFrame({'value' : [pd.NA]}), df.iloc[i:]]).reset_index(drop=True)
        
        def on_append(event):
            with warnings.catch_warnings():
                # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                warnings.filterwarnings("ignore", category=FutureWarning)
                wtabulator.value = pd.concat([wtabulator.value, pd.DataFrame({'value' : [pd.NA]})]).reset_index(drop=True)

        def on_delete(event):
            if len(wtabulator.selection) > 0:
                wtabulator.value = wtabulator.value.drop(wtabulator.selection).reset_index(drop=True)
                wtabulator.selection = []
        
        def on_save(event):
            try:
                self._layout.loading = True
                id = select.value
                #perror(f'on_save {id}')
                array = wtabulator.value['value'].to_numpy()
                self.dataset_package.dataset.set_inconsistent_on_ascendants(id, notify=False)           
                self.dataset_package.dataset.edit_sequence(id, DATA_VALUES, array)     
                
                """
                id = select.value
                array = wtabulator.value['value'].to_numpy()
                old_len = dataset_package.dataset.sequences.at[id, DATA_LENGTH]
                length = len(array)
                if length != old_len :
                    self.dataset_package.dataset.edit_sequence(id, DATA_LENGTH, length, notify=False)                
                    self.dataset_package.dataset.edit_sequence(id, DATA_LENGTH, dataset_package.dataset.sequences.at[id, DATE_BEGIN] + length, notify=False)                
                ascendants = self.dataset_package.dataset.get_ascendants(id, recursive=True)
                if len(ascendants) > 0:
                    self.dataset_package.dataset.edit_sequence(ascendants, INCONSISTENT, True, notify=False)
                self.dataset_package.dataset.edit_sequence(id, DATA_VALUES, array)                
                wtabulator.value """
            except Exception as inst:
                logger.error(f'on_save : {inst}', exc_info=True)
            finally:
                self._layout.loading = False

        def sync_data(event):
            options = {}
            if dataset_package.dt_data is not None :
                for i, row in dataset_package.dt_data.iterrows():
                    options[row[KEYCODE]] = row[ID_CHILD]
            select.options = options
            select.value = None

        def sync_tabulator(event):
            if select.value is not None:
                category = dataset_package.dataset.sequences.at[select.value, CATEGORY]
                if category == MEASURE:
                    data = dataset_package.dataset.sequences.loc[select.value, DATA_VALUES]
                    wtabulator.value = pd.DataFrame({'value' : data})
                else:
                    wtabulator.value = None
                    logger.warning(f'The selected serie is not a tree ring serie.')

        dataset_package = self.dataset_package
        dataset_package.wselection.param.watch(sync_data, ['value'], onlychanged=True)
        #dataset_package.panel_tabulator.visible = False
        
        select = pn.widgets.Select(name=f'Select {KEYCODE}', options=[], description=f'Select the {KEYCODE} serie to edit.')
        select.param.watch(sync_tabulator, ['value'], onlychanged=True)
        
        bt_insert = pn.widgets.Button(name=f'Insert', icon='insert', button_type='primary', description='Insert a new value before the selected row.')
        bt_insert.on_click(on_insert)

        bt_append = pn.widgets.Button(name=f'Append', icon='append', button_type='primary', description='Append a new value after the last row.')
        bt_append.on_click(on_append)

        bt_delete = pn.widgets.Button(name=f'Delete', icon='delete', button_type='primary', description='Delete the selected rows.')
        bt_delete.on_click(on_delete)

        bt_save = pn.widgets.Button(name=f'Save', icon='save', button_type='primary', description='Save the modifications.')
        bt_save.on_click(on_save)

        wtabulator = pn.widgets.Tabulator(
                                    sizing_mode='stretch_width',
                                    max_height=600,
                                    min_height=300,
                                    height_policy='max',
                                    #selectable=True,
                                    selectable='checkbox',

                                    show_index = True
                                    )
        
        return pn.Column(
            dataset_package,
            select,
            wtabulator,
            pn.Row(bt_insert, bt_append, bt_delete, bt_save)
        )
     
    def __panel__(self):
        """ Return the panel layout."""
        return self._layout
    



        



