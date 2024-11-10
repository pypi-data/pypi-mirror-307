
"""
    Adaptation of Viewer class
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
 
import json
import param
import panel as pn
from panel.viewable import Viewer
from pathlib import Path
from pyDendron.app_logger import logger, perror, check_version, __version__

class MyViewer(Viewer):
    def __init__(self, cfg_path, **params):
        super().__init__(**params)
        self.cfg_path = cfg_path
        self.cfg_file = cfg_path / Path(f'{self.__class__.__name__}.cfg.json')
        self.load_cfg()
    
    def dump_cfg(self):
        with open(self.cfg_file, 'w') as fd:
            data = {
                'version': __version__,
                'param' : self.param.serialize_parameters(),
            }
            json.dump(data, fd)

    def load_cfg(self):
        try:
            #print(f'{self.__class__.__name__} load_cfg')
            if check_version(self.cfg_file):
                with open(self.cfg_file, 'r') as fd:
                    data = json.load(fd)
                    for key, value in json.loads(data['param']).items():
                        if key in self.param.params().keys():
                            if key != 'name':
                                self.param.set_param(key, value)
        except Exception as inst:
            logger.warning(f'ignore cfg {self.__class__.__name__}.')
            logger.error(f'load_cfg: {inst}')    
