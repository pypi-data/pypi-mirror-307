"""
Package Editor
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"


import pandas as pd
import param
import panel as pn
from panel.viewable import Viewer
from pathlib import Path
from io import BytesIO

from pyDendron.app_logger import logger, perror
from pyDendron.gui_panel.dataset_package import DatasetPackage, save_package
from pyDendron.dataname import ICON
from pyDendron.gui_panel.tabulator import (_get_selection, get_download_folder, unique_filename)

class DatasetPackageEditor(Viewer):
    selection = param.List(default=[], doc='path')

    def __init__(self, dataset, parameters, **params):
        bt_size = 150
        super(DatasetPackageEditor, self).__init__(**params) 
        
        self.dataset = dataset
        self.param_column_package = parameters.column_package
        self.package = DatasetPackage(dataset, parameters, name='Editor')
        self.panel_tabulator = self.package.panel_tabulator
        self.wselection = self.package.wselection
        #self.wselection.param.watch(self.on_package_selected,  ['value'], onlychanged=True)

        self.wtabulator = self.package.wtabulator
        
        delete_items = [('Delete all packages', 'a')]
        self.bt_delete = pn.widgets.MenuButton(name='Delete package', items=delete_items, icon='file-off', button_type='primary', align=('start', 'end'), split=True)
        #self.bt_delete = pn.widgets.Button(name='Delete package', icon='file-off', button_type='primary', width=bt_size, align=('start', 'end'), description='Delete the selected package.')
        self.bt_delete.on_click(self.on_delete)
        
        self.bt_erase = pn.widgets.Button(name='Remove row', icon='eraser', button_type='primary', width=bt_size, align=('start', 'end'), description='Remove the selected rows.')
        self.bt_erase.on_click(self.on_erase)
        
        self.bt_save = pn.widgets.Button(name='Save package', icon='file', button_type='primary', width=bt_size, align=('start', 'end'), description='Save the package into the dataset.')
        self.bt_save.on_click(self.on_save)

        #self.bt_stats = pn.widgets.Button(name='Add', icon='column-insert-left', button_type='primary', align=('start', 'end'), description='Add the statistics into the table.')
        #self.bt_stats.on_click(self.on_stats)

        #self.bt_excel = pn.widgets.FileDownload(callback=self.on_excel, filename='package.xlsx', embed=False, 
        #                                        label='Download Excel', icon='file-export', button_type='primary', 
        #                                        width=bt_size, align=('start', 'end'), description='Download the table as an Excel file.')
        
        self.bt_add = pn.widgets.Button(name='Merge into', icon='cube-plus', button_type='primary', align=('start', 'end'), description='Merge the selected package into the current package.')
        self.bt_add.on_click(self.on_add)
        
        self.bt_remame = pn.widgets.Button(name='Rename package', icon='edit', button_type='primary', align=('start', 'end'), description='Rename the selected package.')
        self.bt_remame.on_click(self.on_rename)
        self.wnew_name = pn.widgets.TextInput(name='New name:', value='', placeholder='Enter the new name for the package.', align=('start', 'end'), width=bt_size)

        self.package_merge =  pn.widgets.Select(name='Package to merge:', options=[], description='Select the package to merge into the current package.')
        self.wselection.param.watch(self.sync_data,  ['value'], onlychanged=True)


        self._layout = pn.Column(self.package, 
                                 pn.Row(self.bt_erase, self.bt_save, self.bt_delete),
                                 pn.Row(self.bt_remame, self.wnew_name),
                                 pn.Row(self.bt_add, self.package_merge)
                                )
        self.panel_tabulator.collapsed = False
    
    def on_rename(self, event):
        """
        Renames the selected package.

        This method is triggered when the 'Rename package' button is clicked in the GUI.
        It checks if the dataset package is valid, and if so, it renames the package using the specified new name.

        Parameters:
            event (wx.Event): The event object that triggered the method.

        Returns:
            None
        """
        try:
            if not self.check_package(data=False):
                return
            new_name = self.wnew_name.value
            old_name = self.wselection.value    
            if new_name == '':
                logger.warning('New name is empty.')
                return
            save_package(self.wtabulator.value, new_name, self.dataset)
            self.dataset.delete_package(old_name)
            self.wselection.value = new_name
        except Exception as inst:
            logger.error(f'on_rename: {inst}', exc_info=True)
    
    def sync_data(self, event):
        """
        Synchronizes the data in the dataset package editor.

        This method updates the options in the `package_merge` attribute based on the current selection in the `wselection_name` attribute.

        Parameters:
        - event: The event object that triggered the synchronization.

        Returns:
        - None
        """
        self.package_merge.options = list(set(self.wselection.options) - set('None'))
        self.package_merge.value = ''
    
    # def on_package_selected(self, event):
    #     """
    #     Event handler for when a package is selected.

    #     Parameters:
    #     - event: The event object representing the package selection event.
    #     """
    #     self.bt_excel.filename = 'pkg_' + self.wselection.value + '.xlsx'
    
    def __panel__(self):
        return self._layout

    def on_add(self, event):
        if not self.check_package(data=False):
            return

        if self.package_merge.value != '':
            p1 = self.dataset.get_package(self.package_merge.value)
            p2 = self.dataset.get_package(self.wselection.value)
            name = self.wselection.value
            self.dataset.set_package(self.wselection.value, list(set(p1 + p2)))
            self.package.param.trigger('notify_package_change')
            
    # def on_excel(self):
    #     """
    #     Export the data in the tabulator widget to an Excel file.

    #     Returns:
    #         BytesIO: The Excel file as a BytesIO object.

    #     Raises:
    #         Exception: If an error occurs during the export process.
    #     """
    #     try:
    #         if not self.check_package():
    #             return
    #         output = BytesIO()
    #         with pd.ExcelWriter(output) as writer:
    #             cols = [x for x in self.wtabulator.value.columns.to_list() if x != ICON] 
    #             data = self.wtabulator.value[cols]
    #             data.to_excel(writer, sheet_name=self.wselection.value, merge_cells=False, float_format="%.6f")
    #         output.seek(0)
    #         return output
    #     except Exception as inst:
    #         logger.error(f'on_excel: {inst}', exc_info=True)

    def check_package(self, package_name=True, data=True):
        """
        Check if the package is valid.

        Args:
            package_name (bool): Flag indicating whether to check the package name. Defaults to True.
            data (bool): Flag indicating whether to check the data. Defaults to True.

        Returns:
            bool: True if the package is valid, False otherwise.
        """
        if (self.wselection.value == '') and package_name:
            logger.warning('Package name is empty.')
            return False
        if ((self.wtabulator.value is None) or (len(self.wtabulator.value) <=0 )) and data:
            logger.warning('Data is empty.')
            return False
        return True

    # def on_stats(self, event):
    #     """
    #     Perform statistical calculations on the dataset.

    #     This method is triggered when the 'Stats' button is clicked in the GUI.
    #     It checks if the dataset package is valid, and if so, it performs statistical
    #     calculations on the dataset using the specified columns and stat columns.

    #     Parameters:
    #         event (wx.Event): The event object that triggered the method.

    #     Returns:
    #         None

    #     Raises:
    #         Exception: If an error occurs during the statistical calculations.

    #     """
    #     try:
    #         if not self.check_package():
    #             return
    #         cols = list(set(self.wtabulator.value.columns.to_list()) - set(self.param_column_package.get_columns()))
    #         self.wtabulator.value = self.dataset.statistics(data=self.wtabulator.value[cols], 
    #                                         columns=cols, 
    #                                         stat_columns=self.param_column_package.get_columns())
    #     except Exception as inst:
    #         logger.error(f'on_excel: {inst}', exc_info=True)
        
    def on_delete(self, event):
        """
        Deletes the selected package from the dataset.

        Parameters:
        - event: The event object triggered by the delete action.

        Returns:
        - None
        """
        if event.obj.clicked == 'a':
            self.dataset.delete_all_packages()
        else:
            if not self.check_package(data=False):
                return
            self.dataset.delete_package(self.wselection.value)
            self.wselection.value = self.wselection.options[0]
    
    def on_save(self, event):
        """
        Event handler for the save button.

        This method is called when the user clicks the save button in the GUI panel.
        It performs the necessary checks and saves the package if the checks pass.

        Args:
            event: The event object triggered by the save button.

        Returns:
            None
        """
        try:
            #print('on_save')
            self._layout.loading = True
            if not self.check_package():
                return
            save_package(self.wtabulator.value, self.wselection.value, self.dataset)
            #print('on_save')
        except Exception as inst:
            logger.error(f'on_save: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
            self.wselection.value =  self.wselection.options[0]
        finally:
            self._layout.loading = False

    def on_erase(self, event):
        """
        Event handler for the erase button.

        This method is called when the erase button is clicked. It removes the selected rows from the tabulator widget.

        Args:
            event: The event object associated with the button click.

        Returns:
            None
        """
        try:
            self._layout.loading = True
            df_selection = _get_selection(self.wtabulator)
            if df_selection is not None:
                self.wtabulator.value = self.wtabulator.value.drop(df_selection.index.to_list())
                save_package(self.wtabulator.value, self.wselection.value, self.dataset)
            else:
                logger.warning('No row selected.')
        except Exception as inst:
            logger.error(f'on_erase: {inst}', exc_info=True)
            self.wtabulator.value = pd.DataFrame(columns=list(dtype_view.keys()))
        finally:
            self.wtabulator.selection = []
            self._layout.loading = False
