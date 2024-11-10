"""
Dataset selector
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

import param
import panel as pn
from panel.viewable import Viewer
import json

from pathlib import Path

from pyDendron.app_logger import logger, perror
from pyDendron.dataname import *
from pyDendron.dataset import Dataset
from pyDendron.gui_panel.my_viewer import MyViewer
from pyDendron.gui_panel.dialog import MessageBox

class DatasetSelector(MyViewer):
    """
    Show dataset tree as list of panel 
    """
    path = param.Foldername('./', doc='path of the data')
    filters = param.List(['*.p', '*.xlsx', '*.json'], doc='glob filter')
    options = param.Dict({}, doc='options')
    save_auto =  param.Boolean(True, doc='Automatically save the dataset on every major change or every 5 minutes.')
    save_cfg =  param.Boolean(True, doc='Save dataset and configuration when disconnected.')
    backup =  param.Boolean(True, doc='Create a backup of the dataset when loading a new dataset.')
    
    def __init__(self, dataset, template, cfg_path, **param):
        super(DatasetSelector, self).__init__(cfg_path, **param)
        #self.cfg_file = cfg_path / Path('pyDendron.selector.cfg.json')
        self.template = template
        self.dataset = dataset

        self.wselect = pn.widgets.Select(name='Selection', options=self.get_options(), description='Dataset to load.')
        
        self.bt_load = pn.widgets.Button(name='Load', icon='loader', button_type='primary', description='Load the selected dataset.')
        self.bt_load.on_click(self.on_load)
        self.bt_refresh = pn.widgets.Button(name='Refresh', icon='refresh', button_type='primary', description='Refresh the dataset list.')
        self.bt_refresh.on_click(self.on_refresh)
        self.bt_save = pn.widgets.Button(name='Save', icon='file-download', button_type='primary', description='Save the loaded dataset.')        
        self.bt_save.on_click(self.on_save)
        
        self._layout = pn.Column(self.wselect, 
                                 pn.Row(self.bt_load, self.bt_refresh, self.bt_save), 
                                 pn.Row(self.param.save_auto, self.param.backup, self.param.save_cfg)
                                 )

        self.param.watch(self.on_save_auto,  ['save_auto'], onlychanged=True)
        
    def __panel__(self):
        return self._layout

    def get_sidebar(self):
            """
            Returns a Card widget that contains the sidebar parameters.

            Returns:
                pn.Card: The Card widget representing the sidebar.
            """
            box = pn.Card(
                self._layout, 
                margin=(5, 0), 
                sizing_mode='stretch_width',
                hide_header=True, 
                title='Dataset')
            return box

    def get_options(self):
        """
        Retrieve the available options for the dataset selector.

        Returns:
            dict: A dictionary containing the options for the dataset selector.
                    The keys are formatted as emoji + file name, and the values are the corresponding file paths.
        """
        options = {}
        #perror(f'Filters: {self.filters}')
        for flt in self.filters:
            for file in Path(self.path).glob(flt):
                options[f'\U0001F4E6 {str(file.name)}'] = file
        return options

    def on_load(self, event):
        """
        Event handler for the load button.

        Args:
            event: The event object representing the button click event.

        Raises:
            Exception: If an error occurs during the loading process.

        """
        try:
            self._layout.loading = True
            file = self.wselect.value
            self.dataset.load(file)
            if self.backup:
                self.dataset.backup(file)
        except Exception as inst:
            logger.error(f'DatasetSelector, on_load: {inst}', exc_info=True)
        finally:
            self._layout.loading = False
        
    def on_refresh(self, event):
        """
        Event handler for the refresh button.

        Parameters:
            event : The event object.

        Returns:
            None
        """
        self.wselect.options = self.get_options()

    def on_save_auto(self, event):
        """
        Callback method triggered when the 'save_auto' event is fired.

        Args:
            event: The event object containing information about the event.

        Returns:
            None
        """
        self.dataset.save_auto = event.new
        
    def on_save(self, event):
        """
        Saves the dataset.

        This method is called when the user clicks the save button. 

        Parameters:
        - event: The event object representing the save button click.

        Returns:
        None
        """
        try:
            self._layout.loading = True
            self.dataset.dump()
        except Exception as inst:
            logger.error(f'on_save: {inst}')
        finally:
            self._layout.loading = False

    @property  
    def _values(self):
        return self.wselect.value        


