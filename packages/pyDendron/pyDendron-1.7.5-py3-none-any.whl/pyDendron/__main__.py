

"""
    pyDendron Main
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
 
import sys
import signal
import subprocess
import argparse

from pyDendron import pyDendron_panel


try:
    parser = argparse.ArgumentParser(description="pydenron: A dendromean tool for tree-ring data analysis.")
    parser.add_argument('--www', action='store_true', help='pyDendron server and client navigator are on different computer.')
    parser.add_argument('--debug', action='store_true', help='Active debug mode')
    parser.add_argument('--autoreload', action='store_true', help='Panel server flag: whether to autoreload source when script changes.')


    args = parser.parse_args()
    #page = pyDendron_import.__file__ if args.importdata else pyDendron_panel.__file__
    page = pyDendron_panel.__file__
    
    cmd = f'-m panel serve --global-loading-spinner --keep-alive 1000 --check-unused-sessions 1000 --unused-session-lifetime 1000 ' 
    cmd_page = f'--show {page} '
    MAX_SIZE_MB=128*1024*2 
    
    if args.www:
        cmd += f'--websocket-max-message-size {MAX_SIZE_MB} '
        cmd_page += '--args --www '
    elif args.debug:
        cmd += '--admin-log-level debug --admin --profiler pyinstrument '
    elif args.autoreload:
        cmd += '--autoreload '
        #print('autoreload sources')    
    
    print('cmd: sys.executable '+ cmd + cmd_page)
    
    subprocess.run([sys.executable] + cmd.split() + cmd_page.split())
except KeyboardInterrupt:
    pass
except Exception as e:
    print(f"Error: {e}")
    exit()

