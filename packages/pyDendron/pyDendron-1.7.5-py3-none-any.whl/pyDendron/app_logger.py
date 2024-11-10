
"""
Application Logger
"""

__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"


import logging
import sys
import os
import panel as pn
import numpy as np
import webbrowser
import urllib.parse
from pathlib import Path
import json

GENERAL_LEVEL = logging.ERROR
APP_LEVEL = logging.DEBUG
NOTIFICATION_LEVEL = logging.INFO
LOG_PATH = Path(os.path.expanduser("~")) / 'pyDendron'
LOG_FILENAME = str(LOG_PATH / 'pydendron.log')
FORMAT = '%(asctime)s | %(levelname)s | %(name)s | %(message)s'

def get_git_version():
    import subprocess
    
    try:
        import importlib.metadata

        version = importlib.metadata.version('pyDendron')
        return version
    except ImportError:
        # Get the directory of the __init__.py file
        current_directory = Path(__file__).resolve().parent
        file_path = current_directory / 'version.txt'
        # Exécute la commande git pour obtenir la version (tag) la plus récente
        version = subprocess.check_output(['git', 'describe', '--tags']).strip().decode('utf-8')

        return version
    except subprocess.CalledProcessError:
            return "Number unable."
    
__version__ = get_git_version()


class NotificationStream():
    """
    A class that represents a notification stream.

    This class is responsible for writing log messages to the notification system.
    It provides methods to send different types of notifications based on the log message level.

    Args:
        duration (int, optional): The duration of the notifications in milliseconds. Defaults to 5000.
    """

    def __init__(self, duration=5000):
        self.duration = duration
        self.previous_message = None

    def _extracte_message(self, msg):
        """
        Extracts the relevant part of the log message.

        Args:
            msg (str): The log message.

        Returns:
            str: The extracted log message.
        """
        
        #if msg.find('[STDERR]') >= 0:
        #    return None
        #index = np.max(np.array([msg.find("DEBUG"), msg.find("WARNING"), msg.find("INFO"),
        #    msg.find("ERROR"), msg.find("CRITICAL")]))
        #if index > -1:
        #    msg = msg[index:]
        msg = msg.split('|')[-1]
        if len(msg) > 103:
            msg = msg[:50]+ '...'+msg[-50:]
        return msg
 
    def write(self, msg):
        """
        Writes a log message to the notification system.

        This method processes the log message and sends the appropriate notification based on the log message level.

        Args:
            msg (str): The log message to be sent as a notification.
        """
        if pn.config.notifications and (pn.state.notifications is not None):
            if msg is None:
                return
            text = self._extracte_message(msg)
            if text == self.previous_message:
                return
            if msg.find('DEBUG') >= 0:
                pn.state.notifications.send(text, background='hotpink', icon='<i class="fas fa-bug"></i>')
            elif msg.find('WARNING') >= 0:
                if msg.find('Dropping a patch') >= 0: #can't remove Bokeh message !!!
                    return
                pn.state.notifications.warning(text, self.duration*2)
            elif msg.find('INFO') >= 0:
                pn.state.notifications.info(text, self.duration)
            elif msg.find('ERROR') >= 0:
                pn.state.notifications.error(text, 0)
            elif msg.find('CRITICAL') >= 0:
                pn.state.notifications.send(text, duration=0, background='black', icon='<i class="fas fa-burn"></i>')
            else:
                #print('Unknown log message level:|||', msg, '|||')
                pn.state.notifications.send(text, duration=0, background='gray', icon='<i class="fas fa-bolt"></i>')
            self.previous_message = text

def add_stream(logger, handler, level=logging.INFO, format=FORMAT):
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(format)) # add formatter to ch
    logger.addHandler(handler) # add ch to logger
    return handler

class StderrToLogger(object):
    def __init__(self, logger, level=logging.DEBUG):
        self.logger = logger
        self.level = level

    def write(self, message):
        if (message.strip() != "") and (message.strip() != "^"):
            self.logger.log(self.level, '[STDERR] ' + message.rstrip())

    def flush(self):
        pass

def print_logger_info():
    print('*'*80)
    for name, logger in logging.Logger.manager.loggerDict.items():
        if isinstance(logger, logging.Logger):
            print('---->', name, 'cst general:', GENERAL_LEVEL, 'cst app:', APP_LEVEL, 'cur level:', logger.level, 'parent:',logger.parent, 'propagate:', logger.propagate)
            for handler in logger.handlers:
                print('\t---->', handler)
    print('*'*80)

def general_logger(level=GENERAL_LEVEL, format=FORMAT):
    logging.basicConfig(format=FORMAT, level=GENERAL_LEVEL, force=True)
    logging.captureWarnings(True)
    
    for name, logger in logging.Logger.manager.loggerDict.items():
        if isinstance(logger, logging.Logger):
            logger.setLevel(level)
            for handler in logger.handlers:
                handler.setLevel(level)
                handler.setFormatter(logging.Formatter(format))

    # create general logger
    logger_root = logging.getLogger()

    # create file handler
    LOG_PATH.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(LOG_FILENAME, mode='w')
    add_stream(logger_root, file_handler, level=level, format=format)

    return logger_root

def app_logger(level=APP_LEVEL, format=FORMAT):
    logger = logging.getLogger('pyDendron')
    logger.setLevel(level)

    # redirect stderr to logger
    sys.stderr = StderrToLogger(logger)

    # create notification stream to redirect log messages to the panel notification system
    notification_stream = NotificationStream()
    notification_handler = add_stream(logger_root, logging.StreamHandler(notification_stream), level=level, format=format)

    return logger, notification_stream

logger_root = general_logger()
logger, notification_stream = app_logger()

"""
-------------------------------------------------------------------------------
Logger addones functions
-------------------------------------------------------------------------------
"""
def catch_bokeh_log(cb_connection, cb_disconnection, app):
    """
    Catch the disconnection of a WebSocket connection and save the data.

    Args:
    
        cb_auto_save : callback to save data.
    """
    
    class BohehFilter(logging.Filter):
        def __init__(self, cb_connection, cb_disconnection, app):
            super(BohehFilter, self).__init__()
            self.cb_connection = cb_connection
            self.cb_disconnection = cb_disconnection
            self.app = app
            
        def filter(self, record):
            if record.getMessage().startswith('WebSocket connection closed'):
                self.cb_disconnection(self.app)
            elif record.getMessage().startswith('ServerConnection created'):
                self.cb_connection(self.app)
            return True

    logger_bokeh = logging.getLogger('bokeh.server.views.ws')
    logger_bokeh.setLevel(APP_LEVEL)
    logger_bokeh.addFilter(BohehFilter(cb_connection, cb_disconnection, app))

def catch_tornado_log(app):
    class TornadoFilter(logging.Filter):
        def __init__(self, app):
            super(TornadoFilter, self).__init__()
            self.app = app
            
        def filter(self, record):
            if record.getMessage().startswith('Exception in callback functools.partial(<bound method IOLoop._discard_future_result'):
                return False
            return True
    
    logger_tornado = logging.getLogger('tornado.application')
    logger_tornado.addFilter(TornadoFilter(app))

def open_mail_client(to, subject, body):
    mailto_link = f"mailto:{to}?subject={urllib.parse.quote(subject)}&body={urllib.parse.quote(body)}"
    webbrowser.open(mailto_link)

def perror(*args, **kwargs):
    """
    Print the message to sys.stderr with the same arguments as the print function.

    Parameters:
    *args : Variable length argument list to print.
    **kwargs : Arbitrary keyword arguments for print.
    """
    logger.debug(' '.join([repr(arg) for arg in args])+' '.join([f"{key}={repr(value)}" for key, value in kwargs.items()]))

    #print(*args, file=sys.stderr, **kwargs)
    
    
def check_version(cfg_filename):
    if Path(cfg_filename).is_file():
        with open(cfg_filename, 'r') as f:
            data = json.load(f)
            if 'version' in data:
                v = data["version"]
                if v == __version__:
                    return True
                else:
                    logger.info(f'ignore {cfg_filename}, versions differ: {v} != {__version__}')
    else:
        logger.info(f'CFG file not found: {cfg_filename}')
    
    return False
