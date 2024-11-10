"""
Treeview of dataset
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import warnings
import re
import copy
import pandas as pd

import numpy as np
import panel as pn
import param
from panel.viewable import Viewer
from pyDendron.tools.location import fullgeocode
from pyDendron.gui_panel.dataset_package import save_package
from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.dataset import Dataset, string_to_boolean
from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters, 
                                           _cell_formatters, _cell_transform,
                                           _get_selection, array2html, row_date_ce, date_ce, category_html,
                                           computed_filed)


class DatasetTreeview(Viewer):
    """
    Treeview to manage dataset.  
    """
    flat =  param.Boolean(False, doc='Show all components / sequences.')
    show_statistics =  param.Boolean(True, doc='Show data statistics.')
    table_height = param.Integer(400, bounds=(100, 1000), step=10, doc='Maximum height of the Treeview tabulator.')
    include_selection_in_package = param.Boolean(True, doc='Include the selected rows in the new package.')
    #date_BCE_CE = param.Boolean(False, doc='Date are BCE/CE.')
    path = param.List([]) # sets and means (ID_PARENT) form the root to the current set/mean
    clicked = param.List([])
    
    def __init__(self, dataset, parameters, **params):
        super(DatasetTreeview, self).__init__(**params) 
        
        self.param_mean = parameters.mean
        self.dataset = dataset
        self.param_columns = parameters.columns

        self.data = self.load() # join components & sequences from dataset        
        self.wpath, self.wstat, self.wtabulator = self.get_tabulator()
        
        bt_size = 120
    
        self.dataset.param.watch(self.on_reload,  ['notify_reload'], onlychanged=True)
        self.dataset.param.watch(self.on_synchronize,  ['notify_synchronize'], onlychanged=True)
        
        self.param.watch(self.set_wstat, ['clicked'], onlychanged=True)
        self.param.watch(self.on_table_height, ['table_height'], onlychanged=True)
        #self.param.watch(self.set_date, ['date_BCE_CE'], onlychanged=True)
        
        self.param_columns.get_widgets().param.watch(self.sync_columns, ['value'], onlychanged=True, queued=True)
        
        self.param.watch(self.sync_flat, ['flat'], onlychanged=True)
        self.param.watch(self.on_show_stats, ['show_statistics'], onlychanged=True)

        offsets_items = [('Normalize offsets', 'o'), ('Set DateEnd', 'de'), ('Set DateBegin', 'db'), ('Offset to DateBegin', 'o2y'), ('DateBegin to offset', 'y2o'), ]
        self.bt_tools = pn.widgets.MenuButton(name='Offset/date tools', items=offsets_items, icon='adjustments', button_type='primary', align=('start', 'end'))
        self.bt_tools.on_click(self.on_tools)

        #edit_items = [('Current column value to children', 'propchild'), ('Current values to selected', 'propselect'), ('Get GPS code', 'localisation')]
        edit_items = [('Current values to selected', 'propselect'), ('Get GPS code', 'localisation')]
        self.bt_edit_tools = pn.widgets.MenuButton(name='Edition tools', items=edit_items, icon='pencil', button_type='primary', align=('start', 'end'))
        self.bt_edit_tools.on_click(self.on_tools)

        self.bt_mean = pn.widgets.Button(name='Average', icon='tournament', button_type='primary', align=('start', 'end'), description='Compute mean on selected rows.')
        self.bt_mean.on_click(self.on_mean)

        package_items = [('with next level', 'a1'), ('with all descendants', 'a2'), ('n packages + next level', 'b1'), ('n packages + all descendants', 'b2')]
        self.bt_package = pn.widgets.MenuButton(name='Create package', items=package_items, icon='cube-plus', button_type='primary', align=('start', 'end'), split=True)
        self.bt_package.on_click(self.on_package)
        
        #create_items = [('Create & move selection', 'a'), ('Regexp create & move selection', 'b')]
        create_items = [('Create & move selection', 'a')]
        self.bt_create = pn.widgets.MenuButton(name='Create set', items=create_items, icon='folder-plus', button_type='primary', align=('start', 'end'), split=True)
        self.bt_create.on_click(self.on_create)
        self.w_set_name = pn.widgets.TextInput(name='', placeholder='Create parameters')
        
        self.bt_delete = pn.widgets.Button(name='Delete', icon='trash', button_type='primary', align=('start', 'end'), width=bt_size, description='Move to trash selected rows.')
        self.bt_delete.on_click(self.on_delete)
        self.bt_paste = pn.widgets.Button(name='Paste', icon='clipboard', button_type='primary', align=('start', 'end'), width=bt_size, description="Paste rows from clipboard.")
        self.bt_paste.on_click(self.on_paste)
        self.bt_copy = pn.widgets.Button(name='Copy', icon='copy', button_type='primary', align=('start', 'end'), width=bt_size, description='Copy selected rows to clipboard.')
        self.bt_copy.on_click(self.on_copy)
        self.bt_cut = pn.widgets.Button(name='Cut', icon='cut', button_type='primary', align=('start', 'end'), width=bt_size, description='Cut selected rows to clipboard')
        self.bt_cut.on_click(self.on_cut)
        
        self.bt_goto = pn.widgets.Button(name='Go to', icon='direction-sign', button_type='primary', align=('start', 'end'), width=bt_size, description='Go to selected row and quit the flat mode.')
        self.bt_goto.on_click(self.on_goto)

        self.row_cmd = pn.Row(self.bt_mean, self.bt_tools, self.bt_edit_tools, self.bt_package, self.bt_create, self.w_set_name)
        self.row_ccp = pn.Row(self.bt_copy, self.bt_cut, self.bt_paste, self.bt_delete)
        self.row_flat = pn.Row(self.bt_goto)
        self.row_flat.visible = False

        self._layout = pn.Column(
                self.wpath, 
                self.wtabulator,
                self.wstat,
                pn.layout.Divider(margin=(-10,0)),
                self.row_cmd, 
                self.row_flat,
                self.row_ccp,
                name=self.name
            )
        if self.dataset.is_empty():
            self._layout.visible = False

    def __panel__(self):
        return self._layout
    
    def on_show_stats(self, event):
        self.wstat.visible = event.new

    def on_table_height(self, event):
        self.wtabulator.max_height = event.new
        self.wtabulator.min_height = event.new
    
    def get_sidebar(self, visible=True):
        """
        Create the sidebar Card. 
        """
        
        col = pn.Column(
            self.param.flat, 
            self.param.show_statistics, 
            self.param.table_height,
            self.param.include_selection_in_package,
        )
        
        return pn.Card(col,                 
                margin=(5, 0), 
                sizing_mode='stretch_width', 
                title='TreeView',
                collapsed=True,
                visible=visible)
    
    def set_clipboard(self, selection):
        self.clipboard.value = selection.loc[:, [ICON, KEYCODE]]
    
    def get_tabulator(self):
        """
        Configure the main panel. 
        """   
        wpath = pn.Row(margin=(-10,0))
        
        stylesheet = """
        p {
        padding: 0px;
        margin: 0px;
        }"""


        wstat = pn.pane.Alert(margin=(0,-10, 0, 0), stylesheets=[stylesheet])
        dtype = self.param_columns.get_dtype()
        tab = pn.widgets.Tabulator(pd.DataFrame(columns=self.param_columns.get_columns_hiddens()),
                                    on_click=self.on_click, 
                                    on_edit=self.on_edit, 
                                    hidden_columns= self.param_columns.get_hiddens(), 
                                    text_align=_cell_text_align(dtype),
                                    editors=_cell_editors(dtype, True), 
                                    header_filters=_header_filters(dtype), 
                                    formatters=_cell_formatters(dtype),
                                    pagination='local',
                                    page_size= 1000, 
                                    frozen_columns=[ICON, KEYCODE], 
                                    selectable='checkbox',
                                    sizing_mode='stretch_width',
                                    height_policy='max',
                                    max_height=self.table_height,
                                    min_height=self.table_height,
                                    show_index=False,
                                    layout='fit_data_fill',
                                    margin=(0,0),
                                    row_content = self.get_row_content,
                                    header_tooltips=dtips_view,
                                    ) 
        return wpath, wstat, tab

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
        #perror('get_row_content')    
        try:
            if isinstance(series[DATA_VALUES], np.ndarray):
                lst = []
                lst.append((RAW, array2html(series[DATA_VALUES])))
                return pn.Tabs(*lst, height=self.table_height//2)
        except Exception as inst:
            return pn.pane.Markdown('data error')
        return pn.pane.Markdown('No data.')

    def on_synchronize(self, event):
        """ 
        Synchronize Dataset and TreeView, path is keep. 
        """
        #perror('on_synchronize', event)
        if isinstance(event.obj, Dataset) and isinstance( event.obj.notification_source, DatasetTreeview):
            #perror('on_synchronize self event')
            return
        self.load_refresh(False)

    def on_reload(self, event):
        """ 
        Synchronize Dataset and TreeView, path is reset.
        """
        self.load_refresh(True)
        
    def load_refresh(self, reset_path=False):
        """ 
        Load data from dataset and show data 
        """
        self.wtabulator.selection = []
        self.data = self.load()
        self._layout.visible = False if self.data is None else True
        if reset_path:
            self.path.clear()
        self.show_data()
    
    def load(self):
        """ 
        Load data from dataset 
        """

        data = None
        if not self.dataset.is_empty():
            try:
                self._layout.loading = True
                data1 = self.dataset.get_components().reset_index() # get data
                data2 = self.dataset.sequences.loc[self.dataset.get_roots(),:].reset_index() # add orphan sequences 
                data2.insert(0, ID_PARENT, -1)
                data2.rename(columns={ID:ID_CHILD}, inplace=True)
                with warnings.catch_warnings():
                    # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                    warnings.filterwarnings("ignore", category=FutureWarning)
                    data = pd.concat([data2, data1], ignore_index=True)
                computed_filed(data, icon=True, date=True)
                #data.insert(len(data.columns)-1, OFFSET, data.pop(OFFSET))
                #data.insert(len(data.columns)-1, DATE_BEGIN_CE, data.apply(lambda x: row_date_ce(x, DATE_BEGIN), axis=1))
                #data.insert(len(data.columns)-1, DATE_END_CE, data.apply(lambda x: row_date_ce(x, DATE_END), axis=1))
                #data.insert(0, ICON, data.apply(lambda x: category_html(x), axis=1))
                #data = data[sorted(dtype_view.keys())]  
                data = data.set_index([ID_PARENT, ID_CHILD])
            except Exception as inst:
                logger.error(f'init_data : {inst}', exc_info=True)
            finally:
                self._layout.loading = False

        return data
    
    def show_data(self):
        """ 
        Show data selection according path 
        """
        try:
            view = None
            self._layout.loading = True
            if self.flat:
                view = self.data.reset_index()
            else:
                len_path = len(self.path)
                if len_path == 0: #root nodes
                    parent = pd.DataFrame([{ID_PARENT:-2, ID_CHILD:-1, ICON:'/', KEYCODE:'/', CATEGORY:'/'}])
                    mask = self.data.index.get_level_values(ID_PARENT) == -1
                else: # a node and its children
                    id_grand_parent = self.path[-2] if len_path > 1 else -1
                    parent = self.data.loc[(id_grand_parent, self.path[-1])].to_frame().T
                    parent.index.names = [ID_PARENT, ID_CHILD]
                    parent = parent.reset_index()
                    mask = self.data.index.get_level_values(ID_PARENT) == self.path[-1]
                children = self.data.iloc[mask].reset_index()
                view = children
                
        except Exception as inst:
            logger.error(f'set_data: {inst}', exc_info=True)
            view = pd.DataFrame(columns=self.param_columns.get_columns_hiddens())
        finally:
            #perror('show_data before ', view.dtypes)
            #perror('show_data  before ', self.wtabulator.value.dtypes)
            self.param_columns.update_tabulator(self.wtabulator, view)
            #perror('show_data  after ', self.wtabulator.value.dtypes)
            #self.wtabulator.value = _cell_transform(self.wtabulator.value)
            #self.wtabulator.value = view[self.param_column.get_columns_hiddens()]
            self.wtabulator.selection = []
            self.set_wpath()
            self.set_wstat()
            self._layout.loading = False

    def on_package(self, event):
        """
        Create a new Package and add selections if menu is 'a'.
        """
        try:
            self._layout.loading = True
            selection = self.get_selection()
            if len(selection) == 0:
                logger.warning(f'No selection')
                return
            
            id_roots = selection[ID_PARENT].to_list() if self.include_selection_in_package else None
                
            if event.obj.clicked.startswith('b'): 
                max_depth = 1 if event.obj.clicked == 'b1' else None
                for id, row in selection.iterrows():
                    keycode = row[KEYCODE]
                    res = self.dataset.get_data(row[ID_CHILD], id_roots=id_roots, max_depth=max_depth).reset_index()
                    #perror(f'on_package1 {res}')
                    save_package(res, keycode, self.dataset)
            elif event.obj.clicked.startswith('a'): 
                max_depth = 1 if event.obj.clicked == 'a1' else None
                if self.w_set_name.value is None:
                    logger.warning(f'Package name is empty')
                    return
                res = self.dataset.get_data(selection[ID_CHILD].to_list(), id_roots=id_roots, max_depth=max_depth).reset_index()
                #perror(f'on_package2 {res}')
                save_package(res, self.w_set_name.value, self.dataset)
            else:
                if self.w_set_name.value is None:
                    logger.warning(f'Package name is empty')
                    return
                #perror(f'on_package3 {selection}')
                save_package(selection, self.w_set_name.value, self.dataset)

        except Exception as inst:
            logger.error(f'on_package: {inst}', exc_info=True)
        finally:
            self.wtabulator.selection = []
            self._layout.loading = False


    def on_create(self, event):
        """
        Create a new Set and add selections if menu is 'a'.
        """
        #perror('on_create', event)
        if len(self.path) == 0:
            keycode = self.w_set_name.value if self.w_set_name.value != '' else 'dataset'
            id = self.dataset.new_root(id=self.dataset.new_root_id(), append=False, keycode=keycode)
            self.dataset.notify_changes('create set')
            #logger.warning(f'cannot perform set creation in root or flat mode')
            return            
        try:
            self._layout.loading = True
            if event.obj.clicked == 'b':
                d = {}
                selection = self.get_selection()
                for i, row in selection.iterrows():
                    pattern = self.w_set_name.value if self.w_set_name.value != '' else r'(.+?\(\d+\))'
                    res = re.match(pattern, row[KEYCODE])
                    if res:
                        if res.groups():
                            folder = res.group(1)
                            if folder not in d:
                                d[folder] = [i]
                            else:
                                d[folder].append(i)
                        else:
                            pattern = '(\\w+?)'
                            logger.warning(f"Regexp don't find group. For exemple use {pattern} to select the first word as new set.")
                for keycode, ids in d.items():
                    triplets = self.get_triplets(selection.loc[ids])
                    id = self.dataset.new(keycode=keycode, category=SET, id_parent=self.path[-1])
                    self.dataset.move(triplets, self.path + [id])
                        
            elif event.obj.clicked == 'a':
                    triplets = self.get_triplets(self.get_selection())
                    keycode = self.w_set_name.value if self.w_set_name.value != '' else 'new set'
                    id = self.dataset.new(keycode=keycode, category=SET, id_parent=self.path[-1])
                    self.dataset.move(triplets, self.path + [id])
            else:
                keycode = self.w_set_name.value if self.w_set_name.value != '' else 'new set'
                id = self.dataset.new(keycode=keycode, category=SET, id_parent=self.path[-1])
                self.dataset.notify_changes('create set')
                
        except Exception as inst:
            logger.error(f'on_create: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
    
    def get_selection(self) -> pd.DataFrame:
        """
        Returns the view of selectionned series. 
        """
        return _get_selection(self.wtabulator)
            
    def get_triplets(self, selection):
        """
        Returns a list of triplets containing the parent index, child index, and offset for each selected row.

        Args:
            selection (pandas.DataFrame): The selected rows.

        Returns:
            list: A list of triplets containing the parent index, child index, and offset for each selected row.
        """
        if selection is not None:
            lst = []
            for i, row in selection.iterrows():
                id_parent = row[ID_PARENT]
                id_child = row[ID_CHILD]
                offset = row[OFFSET]
                keycode = row[KEYCODE]
                if id_child not in [TRASH, CLIPBOARD, WORKSHOP]:
                    lst.append((id_parent, id_child, offset))
                else:
                    logger.warning(f"Cannot copy/cut/paste {keycode}.")
            return lst
        else:
            return []

    def on_delete(self, event):
        """
        Handle the delete event triggered by the user.

        Args:
            event: The event object representing the delete event.

        Returns:
            None
        """
        if (len(self.path) == 0):
            #perror('on_delete', self.get_triplets(self.get_selection()))
            triplets = self.get_triplets(self.get_selection())
            self.dataset.soft_drop(triplets)
            logger.warning(f'cannot perform delete form root or in flat mode') 
            return                
        try:
            self._layout.loading = True
            triplets = self.get_triplets(self.get_selection())
            
            if (len(self.path) == 0) or (self.path[-1] == TRASH):
                self.dataset.drop(triplets)
            else:
                self.dataset.soft_drop(triplets)
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
    def on_copy(self, event):
        """
        Event handler for the copy action.

        This method is called when the user performs the copy action in the dataset treeview.
        It retrieves the selected items, converts them into triplets, and copies them to the clipboard.

        Args:
            event: The event object associated with the copy action.

        Returns:
            None
        """
        #if len(self.path) == 0:
        #    logger.warning(f'cannot perform copy in root or flat mode') 
        #    return           
        try:
            self._layout.loading = True
            selection = self.get_selection()
            triplets = self.get_triplets(selection)
            self.dataset.copy(triplets, [CLIPBOARD])
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
    def on_cut(self, event):
        """
        Perform the cut operation on the selected items in the dataset treeview.

        Args:
            event: The event object triggered by the cut operation.

        Raises:
            Exception: If an error occurs during the cut operation.

        Returns:
            None
        """
        #if len(self.path) == 0:
        #    logger.warning(f'cannot perform cut in root or flat mode') 
        #    return           
        try:
            self._layout.loading = True
            selection = self.get_selection()
            triplets = self.get_triplets(selection)
            self.dataset.move(triplets, [CLIPBOARD])
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
    
    def on_paste(self, event):
        """
        Handle the paste event.

        This method is called when the user performs a paste operation.
        It checks if the treeview is not in flat mode and if the current path is not empty.
        If these conditions are met, it retrieves the data from the clipboard and performs the paste operation.
        If an error occurs during the paste operation, an error message is logged.

        Args:
            event: The event object representing the paste event.

        Returns:
            None
        """
        #if self.flat: 
        #    logger.warning('cannot perform paste in flat mode')
        #    return
        if len(self.path) == 0:
            logger.warning('cannot perform paste in root or flat mode')       
            return     
        try:
            self._layout.loading = True
            mask = self.data.index.get_level_values(ID_PARENT) == CLIPBOARD
            selection = self.data.iloc[mask].reset_index()
            triplets = self.get_triplets(selection)
            self.dataset.move(triplets, self.path)
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading = False

    def on_goto(self, event):
        """
        Go to the selected sequence. 
        """
        try:
            self._layout.loading = True
            selection = self.get_selection()
            if len(selection) == 0:
                logger.warning('Select one serie')
                return
            self.flat = False
            self.path = self.dataset.get_path_to_root(selection[ID_PARENT].iloc[0])
            self.show_data()
        except Exception as inst:
            logger.error(f'perform: {inst}', exc_info=True)
        finally:
            self._layout.loading

    def sync_flat(self, event):
        """
        Synchronizes the visibility of the row_cmd and row_flat attributes based on the value of the event.

        Parameters:
        - event: An object representing the event that triggered the synchronization.

        Returns:
        None
        """
        self.row_cmd.visible = False if event.new else True
        self.row_flat.visible = True if event.new else False
        
        self.path.clear()
        self.show_data()

    def sync_columns(self, event):
        """
        Synchronizes the hidden columns in the tabulator widget based on the selected columns in the column selector.

        Parameters:
        - event: The event object that triggered the synchronization.

        Returns:
        None
        """
        #perror('sync_columns', self.wtabulator.value.dtypes)
        self.param_columns.update_tabulator(self.wtabulator)
    
    def on_path_click(self, event):
        """
        Event handler for when a path is clicked in the dataset treeview.

        Args:
            event: The event object containing information about the click.

        Returns:
            None
        """
        i = event.obj.tags[0]
        #logger.debug(f'on_path_click: i={i}, len={len(self.path)}, path={self.path}')
        if i < len(self.path):
            self.path = self.path[:i]
            #logger.debug(f'on_path_click: new path={self.path}')
            self.show_data()
    
    def set_wstat(self, event=None):
        """
        Update the statistics widget with information about the dataset.

        Args:
            event: Optional. The event that triggered the method.

        Returns:
            None
        """
        if self.show_statistics:
            self.wpath.visible = True
            data = self.wtabulator.value
            self.wstat.object = ''
            if data is not None:
                count = len(data)
                date_begin = data[DATE_BEGIN].min()
                if pd.notna(date_begin):
                    date_begin = int(date_begin)
                    date_begin_ce = date_ce(date_begin)
                else:
                    date_begin, date_begin_ce =  '-', '-'
                date_end = data[DATE_END].max()
                if pd.notna(date_end):
                    date_end = int(date_end)
                    date_end_ce = date_ce(date_end)
                else:
                    date_end, date_end_ce =  '-', '-'
                freq = data[CATEGORY].value_counts().to_dict()
                freq_str = ''
                
                for i, (k, v) in enumerate(freq.items()):
                    if i == 0:
                        freq_str += f'{k}: {v}'
                    else:
                        freq_str += f', {k}: {v}'
                self.wstat.object = f'**Date** [{date_begin}, {date_end}] **Date BCE/CE** [{date_begin_ce}, {date_end_ce}]. **Count** {count} ({freq_str}).'
                if len(self.clicked) > 0:
                    self.wstat.object += f' **Current** [{self.clicked[3]}, {self.clicked[1]}] = {self.clicked[2]}'
                
        else:
            self.wpath.visible = False
        
    def set_wpath(self):
        """
        Create a list of Button that represent the path (Breadcrumb navigation).
        """
        def add(i, keycode, icon=None):
            if keycode != '':
                wkeycode = f'{keycode[:15]}...' if len(keycode) > 18 else f'{keycode}'
            else:
                wkeycode = keycode
            hover = ':hover { font-weight: bold;}'

            bt = pn.widgets.Button(name=wkeycode, icon=icon, button_type='light', button_style='outline', 
                                   align=('start', 'center'), tags=[i], margin=(0, 0), width_policy='min',
                                   styles={'text-decoration': 'underline'}, stylesheets=[hover])
            bt.on_click(self.on_path_click)
            tmp_wpath.append(bt)
        
        def add_sep():    
            tmp_wpath.append(pn.pane.HTML('<span>\U000025B6</span>', align=('start', 'center'), 
                                    margin=(0, 0), width_policy='min')) 
            
        tmp_wpath = []
        tmp_wpath.append(pn.pane.Markdown('**Path:**', align=('start', 'center'), margin=(0, 0), width_policy='min'))
        tmp_wpath.append(pn.widgets.TooltipIcon(value="Current path in the treeview.", align=('start', 'center'), margin=(0, 0), width_policy='min'))
        add(0, '', icon='folder')
        for i, id in enumerate(self.path):
            add_sep()
            keycode = self.dataset.sequences.at[id, KEYCODE]
            cat = self.dataset.sequences.at[id, CATEGORY]
            icon = 'trees' if cat == MEAN else 'folder'
            add(i + 1, keycode, icon)
            
        self.wpath.objects = tmp_wpath 
    
    def localisation(self):
        """
        Perform localisation for selected rows in the dataset treeview.

        This method retrieves the selected rows from the dataset treeview and performs
        localisation using the `fullgeocode` function. It then updates the corresponding
        columns in the dataset with the latitude, longitude, and site code.

        Note: The `fullgeocode` function is assumed to be defined elsewhere.

        Returns:
            None
        """
        for id, row in self.get_selection().iterrows():
            keycode = row[KEYCODE]
            (lat, lon, alt, country, state, district, town, zip_code, site) = fullgeocode(keycode, r"^([\w/-]+(?:\s+[\w/-]+)*)")
            if lat != '':
                self.dataset.edit_sequence(row[ID_CHILD], SITE_LATITUDE, float(lat), notify=False)
                self.dataset.edit_sequence(row[ID_CHILD], SITE_LONGITUDE, float(lon), notify=False)
                self.dataset.edit_sequence(row[ID_CHILD], SITE_CODE, str(site), notify=False)
                self.dataset.notify_changes('localisation')
    
    def value2selection(self):
        """
        Updates the value of a selected item in the dataset based on the clicked column and value.

        If a column other than KEYCODE, OFFSET, CATEGORY, DATA_VALUES, DATA_INFO, DATA_LENGTH, or DATA_WEIGHTS
        is clicked, a warning message is logged and the operation is aborted.

        Args:
            None

        Returns:
            None
        """
        if self.clicked is not None:
            _, col, value, __ = self.clicked
            if col in [KEYCODE, OFFSET, CATEGORY, DATA_VALUES, DATA_INFO, DATA_LENGTH, DATA_WEIGHTS, DATA_SIGNATURES]:
                logger.warning(f'The {col} column is not suitable for this operation.')
                return
            
            ids = self.get_selection()[ID_CHILD].to_list()
            self.dataset.edit_sequence(ids, col, value, notify=False)
            self.dataset.notify_changes('value2selection')

    def value2children(self):
        """
        Updates the values of the children nodes based on the clicked node's value.

        This method retrieves the clicked node's index, column, value, and keycode. It then checks if the column is suitable for the operation.
        If the column is suitable, it iterates over the selected rows and retrieves the value, keycode, and index of each row.
        It then retrieves the descendants of the clicked node and gets the indices of the children nodes.
        Finally, it calls the `edit_sequence` method of the dataset to update the values of the children nodes with the provided value.

        Note: This method assumes that the dataset and the necessary variables (`clicked`, `KEYCODE`, `ID_CHILD`, etc.) are properly initialized.

        Returns:
            None
        """
        if self.clicked is not None:
            id, col, value, keycode = self.clicked
            if col in [ID_CHILD, ID_PARENT, KEYCODE, KEYCODE_PARENT, OFFSET, CATEGORY, DATA_VALUES, DATA_INFO, DATA_LENGTH, DATA_WEIGHTS, DATA_SIGNATURES]:
                logger.warning(f'The {col} column is not suitable for this operation.')
                return 
            
            for _, row in self.get_selection().iterrows():
                value = row[col]
                keycode = row[KEYCODE]
                id = row[ID_CHILD]
                #print('value2children id:', id)
                tree = self.dataset.get_descendants(id)
                id_children = [node.id for node in tree.filter().keys()]
                #print('value2children id_children', id_children, len(id_children))
                #print('value2children ', col, value,' keycode', keycode)
                self.dataset.edit_sequence(id_children, col, value, notify=False)
            self.dataset.notify_changes('value2children')
                                     
    def on_tools(self, event):
        """
        Set offsets or dates. 
        """
        def get_ids():
            ids = self.get_selection()[ID_CHILD].to_list()
            if len(ids) == 0:
                ids = None
            #print('get_ids', ids)
            return ids
        
        try:
            self._layout.loading = True
            if event.obj.clicked == 'o':
                self.dataset.shift_offsets(parent_id=self.path[-1], child_ids=get_ids())
            elif event.obj.clicked == 'y2o':
                self.dataset.copy_dates_to_offsets(parent_id=self.path[-1], child_ids=get_ids())
            elif event.obj.clicked == 'o2y':
                self.dataset.set_offsets_to_dates(parent_id=self.path[-1], child_ids=get_ids())
            elif event.obj.clicked == 'db':
                self.dataset.set_date_begin(parent_id=self.path[-1], child_ids=get_ids())
            elif event.obj.clicked == 'de':
                self.dataset.set_date_end(parent_id=self.path[-1], child_ids=get_ids())
            elif event.obj.clicked == 'localisation':
                self.localisation()
            elif event.obj.clicked == 'propchild':
                self.value2children()
            elif event.obj.clicked == 'propselect':
                self.value2selection()
                
        except Exception as inst:
            logger.error(f'set_data: {inst}', exc_info=True)
        finally:
            self.wtabulator.selection = []
            self._layout.loading = False
    
    def on_mean(self, event):
        """
        Compute Mean. 
        """
        try:
            self._layout.loading = True
            selection = self.get_selection()
            id_children = selection.loc[selection[CATEGORY] != MEASURE, ID_CHILD].to_list()
            date_as_offset = self.param_mean.date_as_offset
            biweight = self.param_mean.biweight_mean
            #num_threads = self.param_mean.num_threads
            check_mean_as_measure = self.param_mean.check_mean_as_measure
            #logger.debug(f'on_mean: date_as_offset={date_as_offset}, biweight={biweight}, num_threads={num_threads}, check_mean_as_measure={check_mean_as_measure}')   
            #perror('on_mean', date_as_offset, biweight, num_threads)
            self.dataset.means(id_children, date_as_offset=date_as_offset, biweight=biweight, check_mean_as_measure=check_mean_as_measure)
            self.dataset.notify_changes('on_mean')
            
        except Exception as inst:
            logger.error(f'set_data: {inst}', exc_info=True)
            self.show_data()
        finally:
            self._layout.loading = False

    def on_click(self, event):
        """
        Navigation between sets and means. 
        """
        if self.flat: 
            return
        id_row = event.row
        selected = self.wtabulator.value.iloc[id_row]
        if event.column == ICON:
            if selected[CATEGORY] != MEASURE:
                self.path.append(selected[ID_CHILD])
                self.show_data()
        else:
            self.clicked = [id_row, event.column, event.value, selected[KEYCODE]]

    def on_edit(self, event):
        """
        Handles the event when a cell in the dataset treeview is edited.

        Args:
            event: The event object containing information about the edited cell.

        Raises:
            Exception: If an error occurs while editing the cell.

        Returns:
            None
        """
        
        def set_row_date_ce(id_parent, id_child):
            date_begin = self.dataset.sequences.at[id_child, DATE_BEGIN]
            date_end = self.dataset.sequences.at[id_child, DATE_END]
            date_begin_ce = date_ce(date_begin) 
            date_end_ce = date_ce(date_end) 
            self.data.loc[(id_parent, id_child), [DATE_BEGIN, DATE_END, DATE_BEGIN_CE, DATE_END_CE]] = [date_begin, date_end, date_begin_ce, date_end_ce]
            d = {DATE_BEGIN: [(event.row, date_begin)], DATE_END: [(event.row, date_end)], 
                 DATE_BEGIN_CE: [(event.row, date_begin_ce)], DATE_END_CE: [(event.row, date_end_ce)]}
            self.wtabulator.patch(d)
            try :
                self.dataset.check_date_ring_count(id_child)
            except Exception as inst:
                pass
        
        try:
            self._layout.loading = True
            col = event.column
            row = self.wtabulator.value.iloc[event.row]
            new = event.value
            id_parent, id_child = row[ID_PARENT], row[ID_CHILD]
            if str(self.data.dtypes[col]).startswith('bool'):
                new = string_to_boolean(new)
            if col == OFFSET:
                if id_parent == -1:
                    logger.warning('Cannot edit offset in root')
                    self.wtabulator.patch({event.column: [(event.row, event.old)]})
                else:
                    self.dataset.edit_component(id_parent, id_child, new, source=self)
                    self.data.at[(id_parent, id_child), col] = new
            else:
                self.dataset.edit_sequence(id_child, col, new, source=self)
                if col in [DATE_BEGIN, DATE_END]:
                    set_row_date_ce(id_parent, id_child)
                else:
                    self.data.at[(id_parent, id_child), col] = new
        except Exception as inst:
            self.wtabulator.patch({event.column: [(event.row, event.old)]})
            logger.error(f'on_edit: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
            self.clicked = [row[ID_CHILD], col, new, row[KEYCODE]]
            

            
            




