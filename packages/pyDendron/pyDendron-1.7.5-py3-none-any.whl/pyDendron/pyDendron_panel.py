
"""
    pyDendron panel
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
 
import os
import getpass
import argparse
import sys

import panel as pn
from pathlib import Path
import json
from bokeh.server.contexts import BokehSessionContext
import bokeh
from datetime import datetime
import platform
import shutil

from pyDendron.dataname import ADD_STATISTICS
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
from pyDendron.app_logger import logger, perror, catch_bokeh_log, open_mail_client, LOG_FILENAME, check_version, __version__, catch_tornado_log


def set_extension():
    """
    Set the required extensions for the pyDendron panel.

    This function enables the necessary extensions for the pyDendron panel to function properly.
    It enables the 'throttled', 'notifications', 'tabulator', and 'loading_spinner' extensions.
    It also sets the loading indicator to True and disables the console output.

    Parameters:
        None

    Returns:
        None
    """
    def version(request):
        return __version__
    
    pn.extension(session_key_func=version) # set a session key, use for --reuse-sessions
    pn.extension('tabulator', 'filedropper', throttled=True, notifications=True, loading_spinner='dots')
    pn.param.ParamMethod.loading_indicator = True
    pn.extension(
        disconnect_notification="""Server Connected Closed <br /> <button class="btn btn-outline-light" onclick="location.reload();">Click To Reconnect</button> """,
        ready_notification="""connected."""
    )

class Parameters:
    """
    Class representing the parameters for pyDendron.
    """

    def __init__(self, app, cfg_path):
        self.app = app
        self.detrend = None
        self.mean = None 
        self.columns = None 
        self.column_package = None
        self.package = None
        self.cfg_path = cfg_path
        os.makedirs(os.path.dirname(cfg_path), exist_ok=True)
        self.cfg_filename = cfg_path / Path('pyDendron.cfg.json')
        self.bt_save_parameters = pn.widgets.Button(name='Save parameters', icon="settings", button_type='default', align=('end', 'center'))
        self.bt_save_parameters.on_click(self.on_save_param)
        self.load()

    def get_widgets(self):
            """
            Returns the widget for saving parameters.

            Returns:
                bt_save_parameters (Widget): The widget for saving parameters.
            """
            return self.bt_save_parameters
    
    def save(self):
        """
        Save the parameters to a file.

        This method serializes the parameters of various components and saves them to a JSON file.

        Returns:
            None
        """
        with open(self.cfg_filename, 'w') as f:
            data = {
                'version': __version__,
                'detrend' : self.detrend.param.serialize_parameters(),
                'mean' : self.mean.param.serialize_parameters(),
                'columns' : self.columns.get_columns(),
                'column_package': self.column_package.get_columns(),
                'package' : self.package.param.serialize_parameters(),
            }
            json.dump(data, f)
        self.app.ploter.dump_cfg()
        self.app.crossdating.dump_cfg()
        self.app.dataset_selector.dump_cfg()
        self.app.tools.dump_cfg()
    
    def on_save_param(self, event):
        """
        Event handler for saving parameters.

        This method saves the current parameters and displays a notification
        indicating that the parameters have been saved.

        Args:
            event: The event object associated with the save action.

        Returns:
            None
        """
        self.save()
        logger.info('Parameters saved')
    
    def load(self):
        """
        Load the parameters from a file.

        Args:
            cfg_filename (str): The path to the file.

        Raises:
            Exception: If there is an error loading the file.
        """
        def default_parameters():
            self.detrend = ParamDetrend()
            self.mean = ParamMean()
            self.columns = ParamColumns()
            self.column_package = ParamColumnPackage()
            self.package = ParamPackage()
        
        import json
        try:
            if check_version(self.cfg_filename):
                with open(self.cfg_filename, 'r') as f:
                    data = json.load(f)
                    self.detrend = ParamDetrend(**ParamDetrend.param.deserialize_parameters(data['detrend']))
                    self.mean = ParamMean(**ParamMean.param.deserialize_parameters(data['mean']))
                    self.columns = ParamColumns(selections=data['columns'])
                    self.column_package = ParamColumnPackage(selections=data['column_package'])
                    self.package = ParamPackage(**ParamPackage.param.deserialize_parameters(data['package']))
            else:
                default_parameters()
        except Exception as inst:
            logger.warning(f'1 - Error in {self.cfg_filename}, ignore cfg files. {inst}')
            default_parameters()


class SidebarWidget:
    """
    A class representing a sidebar widget.

    Attributes:
        sidebar (object): The sidebar object.
        objects (dict): A dictionary to store the sidebar objects.
        hiddens (dict): A dictionary to store the paramters to hide depending of ative tab in main panel.
    """

    def __init__(self, app):
        # Add to sidebar
        self.sidebar = app.template.sidebar
        self.objects = {}
        self.hiddens = {}
        self.append_title('## Datasets')
        self.append(app.dataset_selector, 'dataset')
        self.append_title('## Parameters')
        self.append(app.parameters.columns, 'param_columns')
        self.append(app.parameters.column_package, 'param_column_package')
        self.append(app.parameters.package, 'param_package')
        self.append(app.parameters.detrend, 'param_detrend') 
        self.append(app.parameters.mean, 'param_mean')
        self.append(app.treeview, 'treeview')
        self.append(app.ploter, 'ploter')
        self.append(app.crossdating, 'crossdating')
        self.append(app.tools, 'tools')
        
        self.init_hiddens()
        self.active_parameters(app.treeview.name)
        
    def append(self, pane, name):
        """
        Append an parameter object to the sidebar.

        Args:
            pane (Viewer): The pane to be appended.
            name (str): The name of the object.
        """
        card = pane.get_sidebar()
        self.objects[name] = card
        self.sidebar.append(card)

    def append_title(self, title):
        """
        Append a title to the sidebar.

        Args:
            title (str): The title to be appended.
            name (str): The name of the title.
        """
        self.sidebar.append(title)

    def init_hiddens(self):
        """
        Initialize the parameter objects to hide for a given the title of the tab.
        """
        self.hiddens['Treeview'] = ['ploter', 'crossdating', 'tools', 'param_detrend', 'param_package','param_column_package']
        self.hiddens['Package'] = ['treeview', 'ploter', 'crossdating', 'tools', 'param_detrend', 'param_mean', 'param_columns']
        self.hiddens['Ploter'] = ['treeview', 'crossdating', 'tools', 'param_columns']
        self.hiddens['Crossdating'] = ['treeview', 'ploter', 'tools', 'param_columns']
        self.hiddens['Tools'] = ['treeview', 'ploter', 'crossdating', 'tools', 'param_package', 
                                 'param_detrend', 'param_mean', 'param_columns']
        self.hiddens['Debug'] = ['treeview', 'ploter', 'crossdating', 'tools', 'param_colums', 'param_package', 
                                 'param_detrend', 'param_mean', 'param_columns', 'param_column_package']

    def active_parameters(self, name):
        """
        Activate the parameters based on the given name of the active tab.

        Args:
            name (str): The name to determine which parameters to activate.
        """
        lst = self.hiddens[name]
        for param_name, param in self.objects.items():
            param.visible = False if param_name in lst else True

class DendronApp:
    """
    The main application class for pyDendron.
    
    Args:
        dendron_info (object): An object containing information about pyDendron.
    """
    def __init__(self, www, session_context):
        filters = ['*.p', '*.json', '*.xlsx']

        self.www = www
        self.session_context = session_context
        self.username = getpass.getuser() if pn.state.user is None else pn.state.user
        
        if f'context {self.username}' not in pn.state.cache:        
            self.dendron_path = None
            self.dataset_path = None
            self.cfg_path = None
            self.tmp_path = None
            
            self.set_directories()
            self.parameters = Parameters(self, self.cfg_path)
            self.template = self.get_template()       
            self.dataset = Dataset(username=self.username)
            self.dataset_selector = DatasetSelector(self.dataset, template=self.template, path=self.dataset_path, filters=filters, cfg_path=self.cfg_path )        
            
            self.treeview = DatasetTreeview(self.dataset, self.parameters, name='Treeview')
            self.tab_package = self.get_tab_package()
            self.ploter = PloterPanel(self.dataset, self.parameters, cfg_path=self.cfg_path, name='Ploter')
            self.crossdating = CrossDatingPanel(self.dataset, self.parameters, self.cfg_path, name='Crossdating')
            self.tools = ToolsPanel(self.dataset_selector, self.dataset, self.parameters, self, tmp_path=self.tmp_path, cfg_path=self.cfg_path, filters=filters, name='Tools')
            self.debug = DebugPanel(self.dataset, self.parameters, self, name='Debug')
            self.tabs = pn.Tabs(self.treeview, self.tab_package, self.ploter, self.crossdating, self.tools, ('Debug', self.debug),
                    dynamic=False, margin=0, styles={'padding' : '0px', 'font-size': '18px'}, sizing_mode='stretch_both',)

            self.tabs.param.watch(self.on_activate, ['active'], onlychanged=True)
            self.template.main.append(self.tabs)
            self.sidebar_widget = SidebarWidget(self)
            

        else:
            self.get_cache()

    def set_cache(self):
        #self.ploter.reset()

        d = {}
        print('--> Set cache')
        print('--> session_context (set_cache)', self.session_context)
        pn.state.cache[f'context {self.username}'] = d
        #d['session_context'] = self.session_context
        d['dendron_path'] = self.dendron_path 
        d['dataset_path'] = self.dataset_path
        d['cfg_path'] = self.cfg_path 
        d['tmp_path'] = self.tmp_path
        d['parameters'] = self.parameters
        d['dataset_selector'] = self.dataset_selector
        d['dataset'] = self.dataset
        #d['tabs'] = self.tabs
        d['treeview'] = self.treeview
        d['tab_package'] = self.tab_package
        #d['ploter'] = self.ploter
        #d['crossdating'] = self.crossdating
        d['tools'] = self.tools
        d['debug'] = self.debug
        #d['template'] = self.template
        #d['sidebar_widget'] = self.sidebar_widget
        d['ploter.dataset_package'] = self.ploter.dataset_package
        d['crossdating.dataset_package'] = self.crossdating.dataset_package
        d['crossdating.master_dataset_package'] = self.crossdating.master_dataset_package
        d['tabs.active'] = self.tabs.active
        d['crossdating.cross_dating.results'] = self.crossdating.cross_dating.results

    def get_cache(self):
        def set_package(package, data):
            package.set_package_name(data.get_package_name())
            package.sync_dataset(None)
        
        print('--> Get cache')
        if f'context {self.username}' in pn.state.cache:
            d = pn.state.cache[f'context {self.username}']

            self.dendron_path = d['dendron_path']
            self.dataset_path = d['dataset_path']
            self.cfg_path = d['cfg_path']
            self.tmp_path = d['tmp_path']
            self.parameters = d['parameters']
            
            self.template = self.get_template()       

            #self.sidebar_widget = d['sidebar_widget']
            self.dataset_selector = d['dataset_selector']
            self.dataset = d['dataset']
            self.treeview = d['treeview']
            self.tab_package = d['tab_package']
            self.ploter = PloterPanel(self.dataset, self.parameters, cfg_path=self.cfg_path, name='Ploter')
            self.crossdating = CrossDatingPanel(self.dataset, self.parameters, self.cfg_path, name='Crossdating')
            self.tools = d['tools']
            self.debug = d['debug']
            self.tabs = pn.Tabs(self.treeview, self.tab_package, self.ploter, self.crossdating, self.tools, ('Debug', self.debug),
                    dynamic=False, margin=0, styles={'padding' : '0px', 'font-size': '18px'}, sizing_mode='stretch_both',)

            self.tabs.param.watch(self.on_activate, ['active'], onlychanged=True)
            self.template.main.append(self.tabs)
            self.sidebar_widget = SidebarWidget(self)
            
            set_package(self.ploter.dataset_package, d['ploter.dataset_package'])
            set_package(self.crossdating.dataset_package, d['crossdating.dataset_package'])
            set_package(self.crossdating.master_dataset_package, d['crossdating.master_dataset_package'])
            self.crossdating.cross_dating.results = d['crossdating.cross_dating.results']
            self.crossdating.on_tabs(None)
            self.tabs.active = d['tabs.active']
            
        
    def set_directories(self):
        self.dendron_path = Path(os.path.expanduser("~")) / 'pyDendron'
        self.dataset_path = self.dendron_path / 'dataset' / Path(self.username)
        self.cfg_path = self.dendron_path / 'cfg' / Path(self.username)
        self.tmp_path = self.dendron_path / 'tmp' / Path(self.username)

        os.makedirs(self.dataset_path, exist_ok=True)
        os.makedirs(self.cfg_path, exist_ok=True) 
        os.makedirs(self.tmp_path, exist_ok=True) 
        
        dataset_test = self.dataset_path / 'dataset_test.p'
        dataset_test_src = os.path.join(os.path.dirname(__file__), 'data', 'dataset_test.p')
        if (not dataset_test.is_file()) and (Path(dataset_test_src).is_file()):
            shutil.copy(dataset_test_src, self.dataset_path)
        self.print_info()

    def print_info(self):
            logger.info(f'Mode: {self.www}')
            logger.info(f'username: {self.username}')
            logger.info(f'dendron_path: {self.dendron_path}')
            logger.info(f'dataset_path: {self.dataset_path}')
            logger.info(f'cfg_path: {self.cfg_path}')
            logger.info(f'tmp_path: {self.tmp_path}')

    def get_tab_package(self):
        """
        Get the tab package.
        
        Returns:
            pn.Tabs: The tab panel containing the package builder and package editor.
        """
        package_editor = DatasetPackageEditor(self.dataset, self.parameters, name='Editor')
        package_builder = DatasetPackageBuilder(self.dataset, self.parameters, self.treeview, name='Builder')
        tab_package = pn.Tabs(package_builder, package_editor, name='Package',
                                styles={'font-size': '16px'})
        return tab_package

    def bt_notification(self):
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
    
    def bt_gps(self):
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

    def get_logout(self):
        return pn.pane.Markdown("""<svg  xmlns="http://www.w3.org/2000/svg"  width="18"  height="18"  viewBox="0 0 24 24"  fill="none"  stroke="currentColor"  stroke-width="1"  stroke-linecap="round"  stroke-linejoin="round"  class="icon icon-tabler icons-tabler-outline icon-tabler-logout">
            <path stroke="none" d="M0 0h24v24H0z" fill="none"/><path d="M14 8v-2a2 2 0 0 0 -2 -2h-7a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h7a2 2 0 0 0 2 -2v-2" />
            <path d="M9 12h12l-3 -3" /><path d="M18 15l3 -3" /></svg>
            <a href="/logout" >Logout</a>""")    


    def bt_send_log(self):
        def on_send_log(event):
            
            panel_version = pn.__version__
            bokeh_version = bokeh.__version__
            date_today = datetime.now()
            os_info = platform.system() + ' ' + platform.release()
            user_name = pn.state.user #getpass.getuser()
            
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

    def get_version(self):
        return pn.pane.Markdown(f"version: {__version__} user: {self.username}")

    def get_template(self):
        """
        Get the template for the application.
                
        Returns:
            pn.template.FastListTemplate: The template for the application.
        """
        logo = os.path.join(os.path.dirname(__file__), 'data', 'trees.svg')
        logo_blue = os.path.join(os.path.dirname(__file__), 'data', 'trees_blue.svg')
        # site_url='https://git-lium.univ-lemans.fr/Meignier/pyDendron/wikis',
        template = pn.template.FastListTemplate(title='pyDendron', logo=logo, favicon=logo_blue, meta_author='LIUM, Le Mans Université', 
                                                meta_keywords='Dendrochronology', main_layout=None)
        template.header.objects = [self.get_version(), self.bt_notification(), self.parameters.get_widgets(), 
                                    self.bt_send_log(), self.bt_gps()]
        if self.www:
            template.header.objects.append( self.get_logout())
        template.modal.append(pn.Column())
        return template
            
    def on_activate(self, event):
        """
        Event handler for tab activation.
        
        Args:
            event (object): The event object.
        """
        self.sidebar_widget.active_parameters(self.tabs.objects[event.obj.active].name)
        
app = None
          
def cb_auto_save():
    """
    Automatically save the dataset.
    """
    msg = 'save'
    if (app is not None) and app.dataset_selector.save_auto:
        msg += ' dataset'
        app.dataset.dump()
    if (app is not None) and app.dataset_selector.save_cfg:
        msg += ' parameters'
        app.parameters.on_save_param(None)
    if msg != 'save':
        logger.info(msg)

def cb_disconnection(app):
    
    #if pn in globals() and (logger is not None):
    try:
        logger.info(f'On disconnection {pn.state.user} {app.username}.')
        if (app is not None):
            logger.info(f' Save context: start')
            app.set_cache()
            app.dataset.dump()
            app.parameters.on_save_param(None)
    except Exception as e:
        print('*** Warning: Context not save***')
        print('*** error', e)

def cb_ready_notification():
    """
    Display a notification when the application is ready.
    """
    pn.state.notifications.append('pyDendron is ready.')

def cb_connection(app):
    pass

#def session_created(session_context: BokehSessionContext):
#    print('--> session created', session_context)
    
def session_destroyed(session_context: BokehSessionContext):
    print('--> session destroyed', session_context)

app = None
if __name__.startswith('bokeh_app'):
    #pn.state.on_session_created(session_created)
    print('--> session_context (main)', pn.state.curdoc.session_context)
    pn.state.on_session_destroyed(session_destroyed)
    
    parser = argparse.ArgumentParser(description="pydenron: A dendromean tool for tree-ring data analysis.")
    parser.add_argument('--www', action='store_true', help='A flag to enable www mode')
    args = parser.parse_args()
    www = args.www

    logger.info('Get paths')
    set_extension()
    logger.info('Create application ')
    app = DendronApp(www, pn.state.curdoc.session_context)
    logger.info('End of initialisation')
    app.template.servable()
    # Callback: autosave 
    logger.info('add_periodic_callback ')
    pn.state.add_periodic_callback(cb_auto_save, 1000*60*5) 
    catch_bokeh_log(cb_connection, cb_disconnection, app)
    #catch_tornado_log(app)
    


    
