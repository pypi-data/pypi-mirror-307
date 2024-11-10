
"""
    This module is used to run a function in a thread.
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
 
try:
    import threading
except ImportError:
    threading = None
import time
from pyDendron.app_logger import logger, perror

class RunThread:
    def __init__(self, run_action, end_action=None, args=(), kwargs={}):
        self._stop_event = threading.Event()
        self.run_action = run_action
        self.end_action = end_action
        self.kwargs = kwargs 
        self.args = args
        self.kwargs['stop_event'] = self._stop_event
        self.kwargs['end_action'] = self.end_action

    def start(self):
        #perror("Starting thread")
        if threading is None:
            self.run_action(*self.args, **self.kwargs)
            self.end_action()
        else:
            self.thread = threading.Thread(target=self.run_action, args=self.args, kwargs=self.kwargs)
            self.thread.start()
        #perror("Thread started")

    def stop(self):
        #perror("Stopping thread")
        self._stop_event.set()
        self.thread.join()
        #perror("Thread stopped")
        
