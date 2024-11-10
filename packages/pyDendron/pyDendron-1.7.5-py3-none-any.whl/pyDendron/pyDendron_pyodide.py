
"""
    pyodide version of pyDendron
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
 
import os
#import getpass
#import argparse
#import sys

import panel as pn
from pathlib import Path
#import json
#from bokeh.server.contexts import BokehSessionContext
import bokeh
#from datetime import datetime
#import platform
#import shutil

from pyDendron.dataset import Dataset
from pyDendron.gui_panel.sidebar import ParamColumns, ParamDetrend, ParamMean, ParamPackage, ParamColumnPackage
from pyDendron.gui_panel.dataset_selector import DatasetSelector
from pyDendron.gui_panel.dataset_treeview import DatasetTreeview
from pyDendron.gui_panel.dataset_package import DatasetPackage
from pyDendron.gui_panel.dataset_package_builder import DatasetPackageBuilder
from pyDendron.gui_panel.dataset_package_editor import DatasetPackageEditor
from pyDendron.gui_panel.tools_panel import ToolsPanel
from pyDendron.gui_panel.ploter_panel import PloterPanel
from pyDendron.gui_panel.debug_panel import DebugPanel
from pyDendron.gui_panel.crossdating_panel import CrossDatingPanel
from pyDendron.app_logger import logger, perror, catch_bokeh_log, open_mail_client, LOG_FILENAME, __version__


def bt_notification():
    """
    Create a button to clear notifications.
    
    Returns:
        pn.widgets.Button: The button to clear notifications.
    """
    def on_rm_notification(event):
        pn.state.notifications.clear()
        
    rm_notification = pn.widgets.Button(name='Clear notifications', icon="trash", button_type='default', align=('end', 'center'))
    rm_notification.on_click(on_rm_notification)
    return rm_notification

def bt_gps():
    """
    Create a button to open the GPS site.
    
    Returns:
        pn.pane.Markdown: The button to open the GPS site.
    """
    # GPS 
    return pn.pane.Markdown("""<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round" class="icon icon-tabler icons-tabler-outline icon-tabler-map">
    <path stroke="none" d="M0 0h24v24H0z" fill="none" />
    <path d="M3 7l6 -3l6 3l6 -3v13l-6 3l-6 -3l-6 3v-13" />
    <path d="M9 4v13" />
    <path d="M15 7v13" />
    </svg>
    <a href="https://nominatim.openstreetmap.org" target="_blank">Open GPS site</a>""")

def get_logout():
    return pn.pane.Markdown("""<svg  xmlns="http://www.w3.org/2000/svg"  width="18"  height="18"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="1"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-logout">
        <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
        <path d="M9 12h12l-3 -3" /><path d="M18 15l3 -3" /></svg>
        <a href="/logout" >Logout</a>""")    


def bt_send_log():
    def on_send_log(event):
        
        panel_version = pn.__version__
        bokeh_version = bokeh.__version__
        date_today = datetime.now()
        os_info = platform.system() + ' ' + platform.release()
        user_name = pn.state.user #getpass.getuser()
        #perror(f'User: {user_name}')
        
        agent = pn.state.headers["User-Agent"] if "User-Agent" in pn.state.headers else "Unknown"
        
        info_string = f"""
        pyDendron: {__version__}
        Date: {date_today}
        OS: {os_info}
        User: {user_name}
        Agent: {agent}
        Panel: {panel_version}
        Bokeh: {bokeh_version}"""

        info_string += '\n'+'-'*80 + '\n'
        with open(LOG_FILENAME, 'r') as file:
            info_string += file.read()
            
        open_mail_client(
            to='pyDendron@univ-lemans.fr',
            subject=f'pyDendron error {user_name}',
            body=info_string
        )
    
    bt_log = pn.widgets.Button(name='Send log', icon="send", button_type='default', align=('end', 'center'))
    bt_log.on_click(on_send_log)
    return bt_log

def get_version():
    return pn.pane.Markdown(f"version: {__version__} ")


pn.extension('tabulator', 'filedropper', throttled=True, notifications=True, loading_spinner='dots')
pn.param.ParamMethod.loading_indicator = True
#pn.extension(
#    disconnect_notification="""Server Connected Closed <br /> <button class="btn btn-outline-light" onclick="location.reload();">Click To Reconnect</button> """
#)

#logo = os.path.join(os.path.dirname(__file__), 'data', 'trees.svg')
template = pn.template.FastListTemplate(title='pyDendron', 
                                        #logo=logo,
                                        meta_author='LIUM, Le Mans Université',
                                        meta_keywords='Dendromean',
                                        main_layout=None,
                                        )
template.header.objects = [get_version(), bt_notification(), #bt_send_log(), 
                           bt_gps()]

dataset = Dataset()
filters = ['*.p', '*.json', '*.xlsx']
#perror('dataset_selector', )
dataset_selector = DatasetSelector(dataset, template=template, path='file::/Users/meignier/pyDendron/dataset/meignier', filters=filters, cfg_path='')    
#dataset_selector.wselect.options = ['test', 'toto', 'tata'] 
template.main.append(dataset_selector)

template.servable()

