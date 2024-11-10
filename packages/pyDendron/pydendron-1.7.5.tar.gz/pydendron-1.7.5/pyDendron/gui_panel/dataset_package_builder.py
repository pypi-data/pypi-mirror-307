"""
Package builder
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import pandas as pd
import param
import panel as pn
import warnings
from panel.viewable import Viewer

from pyDendron.app_logger import logger, perror

from pyDendron.dataname import *
from pyDendron.gui_panel.dataset_package import save_package

from pyDendron.gui_panel.tabulator import (_cell_text_align, _cell_editors, _header_filters, _cell_formatters, 
                                           _get_selection)

class DatasetPackageBuilder(Viewer):
    selection = param.List(default=[], doc='path')

    def __init__(self, dataset, parameters, treeview, **params):
        bt_size = 80
        super(DatasetPackageBuilder, self).__init__(**params)   

        self.dataset = dataset
        self.parameters = parameters
        self.param_columns = self.parameters.columns
        self.treeview = treeview

        self.param_columns.get_widgets().param.watch(self.sync_columns, ['value'], onlychanged=True)

        self.wpath_local = pn.Row()
        self.wpath_treeview = self.treeview.wpath
        
        self.wpath_treeview.param.watch(self.sync_path, ['objects'], onlychanged=True)
        
        self.sql_field = pn.widgets.AutocompleteInput(name='Column', min_characters=0, options=self.param_columns.get_columns_hiddens(), placeholder='Select a column', width=bt_size*2, description='Select a column to filter.')
        self.sql_field.param.watch(self.sync_column_value, ['value'], onlychanged=True)
        self.sql_operator = pn.widgets.Select(name='operator', options=['==', '>', '<', '!=', 'contains' ], width=bt_size*2, description='Select an operator for filter.')
        self.sql_value = pn.widgets.AutocompleteInput(name='value', min_characters=0, restrict=False, options=[], placeholder='Enter a value', width=bt_size*2, description='Enter a value for filter.')
        self.bt_and_add = pn.widgets.Button(name='And ...', icon='logic-and', button_type='primary', width=int(1.5*bt_size), align=('start', 'end'), description='Add the filter with an AND condition.')
        self.bt_and_add.on_click(self.on_add_and)
        self.bt_or_add = pn.widgets.Button(name='Or ...', icon='logic-or', button_type='primary', width=int(1.5*bt_size), align=('start', 'end'), description='Add the filter with an OR condition.')
        self.bt_or_add.on_click(self.on_add_or)

        self.wfilter = pn.widgets.TextAreaInput(name='Filter', value=f'(`{CATEGORY}` != "{SET}")', height=60, sizing_mode='stretch_width', description='SQL like expression to apply to the rows selection.')

        self.bt_select = pn.widgets.Button(name='Append', icon='table-plus', button_type='primary', width=int(1.75*bt_size), align=('start', 'center'))
        self.bt_select.on_click(self.on_select)
        self.rb_append_mode = pn.widgets.RadioBoxGroup(name='Append mode', options=['empty table', 'current table'], inline=True, align=('start', 'center'))
        self.tg_level = pn.widgets.RadioBoxGroup(name='Level', value='current level', options=['current level', 'all descendants'], inline=True, align=('start', 'center'))
        
        self.add_parent = pn.widgets.Checkbox(name='Add parent', value=False, align=('start', 'center'))
        
        dtype = self.param_columns.get_dtype()
        self.wtabulator = pn.widgets.Tabulator(pd.DataFrame(columns=self.param_columns.get_columns_hiddens()), name='Result',                 
                hidden_columns=self.param_columns.get_hiddens(), 
                pagination='local',
                selectable='checkbox', 
                sizing_mode='stretch_width',
                text_align=_cell_text_align(dtype),
                editors=_cell_editors(dtype), 
                frozen_columns=[ICON, KEYCODE], 
                header_filters=_header_filters(dtype), 
                formatters=_cell_formatters(dtype),
                min_height=300,
                page_size=1000,
                max_height=300,
                height_policy='max',
                )
        self.bt_erase = pn.widgets.Button(name='Remove row', icon='eraser', button_type='primary', width=int(1.75*bt_size), align=('start', 'end'), description='Remove the selected rows.')
        self.bt_erase.on_click(self.on_erase)
        
        self.bt_save = pn.widgets.Button(name='Save package', icon='file', button_type='primary', width=int(1.75*bt_size), align=('start', 'end'), description='Save the package into the dataset.')
        self.bt_save.on_click(self.on_save)
        self.wselection_name = pn.widgets.TextInput(name='Name', sizing_mode='stretch_width', description='Package name.')
        
        
        self._layout = pn.Column(
                        self.wpath_local,
                        pn.Row(self.sql_field, self.sql_operator, self.sql_value, self.bt_and_add, self.bt_or_add), 
                                self.wfilter, #title='Select', collapsed=True, sizing_mode='stretch_width'),
                        pn.Row(self.bt_select, 
                               pn.pane.HTML('<b>In:</b>', align=('start', 'center')), pn.widgets.TooltipIcon(value="Clear table before append or keep current rows.", align=('start', 'center')), self.rb_append_mode, 
                               pn.pane.HTML('<b>From:</b>', align=('start', 'center')), pn.widgets.TooltipIcon(value="Select rows form the current path or from the root (all dataset).", align=('start', 'center')),self.tg_level,
                               pn.pane.HTML('<b>Option:</b>', align=('start', 'center')), pn.widgets.TooltipIcon(value="Include parent.", align=('start', 'center')), self.add_parent),
                                
                        self.wtabulator, 
                        self.bt_erase,
                        pn.Row(self.bt_save, self.wselection_name),
                        )

    def __panel__(self):
        return self._layout
    
    def sync_path(self, event):
        """
        Synchronizes the path in the GUI with the current dataset path.

        Parameters:
            event (Event): The event that triggered the synchronization.

        Returns:
            None
        """
        self.wpath_local.objects = [pn.pane.Markdown('**From current Dataset path:**', align=('start', 'center'), margin=(0, 0))] + self.wpath_treeview.objects[1:]
        
    def sync_columns(self, event):
        """
        Synchronizes the hidden columns in the tabulator widget based on the selected columns in the columns widget.

        Parameters:
        - event: The event object triggered by the user action.

        Returns:
        None
        """
        self.param_columns.update_tabulator(self.wtabulator)

    def build(self):
        """
        Builds the dataset package.

        Returns:
            tuple: A tuple containing the wtabulator and _layout objects.
        """
        return self.wtabulator, self._layout

    def sync_column_value(self, event):
        """
        Synchronizes the value of the 'wvalue' attribute based on the selected event.

        Args:
            event: The event object containing the new value.

        Returns:
            None
        """
        if event.new != '':
            try:
                self._layout.loading = True
                if event.new not in [DATA_INFO, DATA_VALUES, DATA_WEIGHTS, DATA_SIGNATURES]:
                    if self.param_columns.get_dtype()[event.new] != 'string':
                        self.sql_value.options = []
                    else:
                        self.sql_value.options = self.dataset.sequences[event.new].dropna().unique().tolist()
            except Exception as inst:
                logger.error(f'sync_column_value: {inst}', exc_info=True)
                self.sql_value.options = []
            finally:
                self._layout.loading = False

    def on_save(self, event):
        """
        Event handler for the save button.

        Saves the package using the values from the `wtabulator` and `wselection_name` widgets.

        Parameters:
        - event: The event object triggered by the save button.

        Returns:
        None
        """
        save_package(self.wtabulator.value, self.wselection_name.value, self.dataset)
            
    def on_add_filter(self):
        """
        Adds a filter to the dataset package builder.

        Returns:
            None
        """
        if self.param_columns.get_dtype()[self.sql_field.value] == 'string':
            if self.sql_operator.value == 'contains':
                self.wfilter.value += f'(`{self.sql_field.value}`.str.contains("{self.sql_value.value}"))'
            else:
                self.wfilter.value += f'(`{self.sql_field.value}` {self.sql_operator.value} "{self.sql_value.value}")'
        else:
            if self.sql_operator.value != 'contains':
                self.wfilter.value += f'(`{self.sql_field.value}` {self.sql_operator.value} {self.sql_value.value})'
        
    def on_add_and(self, event):
        """
        Appends ' and ' to select string.
        """
        self.wfilter.value += ' and '
        self.on_add_filter()
        
    def on_add_or(self, event):
        """
        Appends ' or ' to select string.

        Args:
            event: The event object triggered by the user action.
        """
        self.wfilter.value += ' or '
        self.on_add_filter()
    
    def on_erase(self, event):
        """
        Event handler for the erase button.

         It removes the selected rows from the wtabulator widget.

        Args:
            event: The event object triggered by the erase button click.

        Returns:
            None
        """
        try:
            self._layout.loading = True
            df_selection = _get_selection(self.wtabulator)
            self.wtabulator.value = self.wtabulator.value.drop(df_selection.index.to_list())
        except Exception as inst:
            logger.error(f'on_erase: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(self.param_columns.get_dtype().keys()))
        finally:
            self.wtabulator.selection = []
            self._layout.loading = False

    # def get_descendants(self, groups, groups_all, id_parent):
    #     """
    #     Recursively retrieves the descendants of a given parent index.

    #     Parameters:
    #         groups (pandas.core.groupby.DataFrameGroupBy): The groups object containing the hierarchical data.
    #         groups_all (pandas.core.groupby.DataFrameGroupBy): The groups_all object containing all the groups.
    #         id_parent (int): The index of the parent node.

    #     Returns:
    #         list: A list of indices representing the descendants of the parent node.
    #     """
    #     lst = []
    #     if id_parent in groups.groups:
    #         for id_parent, id_child in groups.get_group(id_parent).index:
    #             lst += self.get_descendants(groups, groups_all, id_child)
        
    #     if id_parent in groups_all.groups:
    #         lst += groups_all.get_group(id_parent).index.to_list()

    #     return lst

    def on_select(self, event):
        """
        Handle the event when an item is selected in the GUI treeview.

        Args:
            event: The event object representing the selection event.

        Returns:
            None

        Raises:
            None
        """
        try:
            self._layout.loading = True
            res = None
            
            if len(self.treeview.path) < 1:
                logger.warning('Creation of package not available if the path is empty (root).')
            else:
                id_parent = self.treeview.path[-1]
                id_roots= self.treeview.path[-2] if len(self.treeview.path) > 1 else None
                if self.tg_level.value == 'current level':
                    if self.add_parent.value:
                        if id_roots is None:
                            logger.warning('Add parent not possible with empty root')
                        res = self.dataset.get_data(id_parent, id_roots=id_roots, max_depth=1)
                    else:
                        res = self.treeview.wtabulator.value.set_index([ID_PARENT, ID_CHILD])
                    if self.wfilter.value != '':
                        res = res.query(self.wfilter.value)
                    self.wselection_name.value = self.wpath_local.objects[-1].name
                else:
                    if self.add_parent.value:
                        if id_roots is None:
                            logger.warning('Add parent not possible with empty root')
                        res = self.dataset.get_data(id_parent, id_roots=id_roots)
                    else:
                        res = self.dataset.get_data(id_parent)

                    if self.wfilter.value != '':
                        res = res.query(self.wfilter.value)
                    if self.rb_append_mode.value ==  'empty table':
                        self.wselection_name.value = self.wpath_local.objects[-1].name
                    else:
                        self.wselection_name.value = f'{self.wselection_name.value} + {self.wpath_local.objects[-1].name}'
                if res is not None:
                    if self.rb_append_mode.value ==  'empty table':
                        self.wtabulator.value = self.treeview.data.loc[res.index.to_list(), :].reset_index()
                    else:
                        with warnings.catch_warnings():
                            # TODO: pandas 2.1.0 has a FutureWarning for concatenating DataFrames with Null entries
                            warnings.filterwarnings("ignore", category=FutureWarning)
                            self.wtabulator.value = pd.concat([self.wtabulator.value, self.treeview.data.loc[res.index.to_list(), :].reset_index()])
                else:
                    logger.warning('on_select: empty result')
        except Exception as inst:
            logger.error(f'on_select: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=self.param_columns.get_columns_hiddens())
            
        finally:
            self._layout.loading = False
