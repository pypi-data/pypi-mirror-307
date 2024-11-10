"""
Ploter panel
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"

from pathlib import Path
import json

import panel as pn
from panel.viewable import Viewer
from bokeh.models import ColumnDataSource

from pyDendron.app_logger import logger, perror, __version__, check_version
from pyDendron.dataname import *
from pyDendron.dataset import Dataset
from pyDendron.gui_panel.dataset_package import DatasetPackage

from pyDendron.ploter import Ploter


class PloterPanel(Viewer):

    def __init__(self, dataset, parameters, cfg_path, **params):
        super(PloterPanel, self).__init__(**params)   
        bt_size = 75
        self.dataset = dataset
        self.parameters = parameters
        self.cfg_path = cfg_path
            
        self.dataset_package = DatasetPackage(dataset, parameters, name='ploter', editable=True, orderable=True)
        self.dataset_package.param.watch(self._sync_data, ['notify_package_change'], onlychanged=True)

        self.ploter = self.load_cfg()
        
        self.sliding_select = pn.widgets.Select(name='Sliding serie', options=[], description='Select the serie to slide.')
        self.sliding_select.param.watch(self.on_sliding_select, ['value'], onlychanged=True)
        #self.ploter.param.watch(self.on_sliding_select, ['y_delta', 'y_height', 'x_offset_mode', 'anatomy', 
        #                                                'y_offset_mode', 'draw_type', 'cambium_estimation', 
        #                                                'legend', 'legend_location', 'show_dates', 'curve_axe',
        #                                                'show_estimated_dates', 'show_cambium_season',
        #                                                              ], onlychanged=True)
        
        self.ploter.param.watch(self._sync_data, ['data_type'], onlychanged=True)

        self.x_slider = pn.widgets.IntSlider(name='X Slider', start=0, end=8, step=1, value=0,
                                             sizing_mode='stretch_width', max_width=250)
        self.y_slider = pn.widgets.FloatSlider(name='Y Slider', start=0, end=8, step=1, value=0, 
                                             sizing_mode='stretch_width', max_width=250)
        
        self.x_slider.param.watch(self.on_slider_x, ['value'], onlychanged=True)
        self.y_slider.param.watch(self.on_slider_y, ['value'], onlychanged=True)
        self.bt_save = pn.widgets.Button(name='Save offset', icon='Save', button_type='primary', align=('start', 'center'), width=2*bt_size, description='Save the offset.' )
        self.bt_save.on_click(self.on_save_offset)
        
        self.bt_plot = pn.widgets.Button(name='Plot', icon='pencil', button_type='primary', align=('start', 'center'), width=2*bt_size, description='Replot the package.' )
        self.bt_plot.on_click(self.on_plot)
        
        layout_light = pn.Row(
            self.bt_plot,
            pn.Row('### Sliding',
                self.sliding_select,
                self.x_slider,
                self.y_slider,
                self.bt_save, styles=dict(background='WhiteSmoke')
            ))
        self._layout = pn.Column(self.dataset_package, layout_light, self.ploter, name=self.name,
                                  margin=(5, 0), sizing_mode='stretch_width')
    
    def on_save_offset(self, event):
        pass
    
    def get_sidebar(self, visible=True):
        pploter = pn.Param(self.ploter, name='Dynamic')
        #reploter = pn.Param(self.ploter.param_replot, name='Reset')
        return pn.Card(pploter, title='Plot', sizing_mode='stretch_width', margin=(5, 0), collapsed=True, visible=visible)  

    def dump_cfg(self):
            """
            Dump the configuration of the ploter panel to a JSON file.

            This method serializes the parameters of the ploter panel and saves them
            to a JSON file specified by `self.cfg_file`.

            Returns:
                None
            """
            cfg_file = self.cfg_path / Path(f'{self.__class__.__name__}.cfg.json')
            with open(cfg_file, 'w') as fd:
                data = {
                    'version': __version__,
                    'ploter' : self.ploter.param.serialize_parameters(),
                }
                json.dump(data, fd)

    def reset(self):
        self.ploter.clear()

    def load_cfg(self):
        """
        Load the configuration for the ploter.

        Returns:
            Ploter: The ploter object with the loaded configuration.
        """
        try:
            cfg_file = self.cfg_path / Path(f'{self.__class__.__name__}.cfg.json')

            if check_version(cfg_file):
                with open(cfg_file, 'r') as fd:
                    data = json.load(fd)
                    ploter = Ploter(**Ploter.param.deserialize_parameters(data['ploter']))
            else:
                ploter = Ploter()
        except Exception as inst:
            logger.warning(f'ignore {cfg_file } ploter panel. {inst}')
        return ploter

    def __panel__(self):
        return self._layout

    def _sync_data(self, event):
        try:
            data = self.dataset_package.data
            if data is not None:
                #logger.debug(f'ploter panel: sync data --> data not None')
                lst = self.dataset_package.data[KEYCODE].to_list() 
                self.sliding_select.options = ['None'] + lst
                #self.on_replot(None)
            else:
                #logger.debug(f'ploter panel: sync data --> data None')
                self.sliding_select.options = ['None']
            self.reset()
            self.sliding_select.value = 'None'
        except Exception as inst:
            logger.error(f'ploter panel: {inst}', exc_info=True)

    def on_plot(self, event):
        self._layout.loading = True
        #self.ploter.visible = False
        try:
            #perror('on_plot before', self.ploter.width, self.ploter.height, self.ploter.figure_pane.object.width, self.ploter.figure_pane.object.height)
            #self.ploter.clear()
            #logger.debug(f'ploter panel: on_replot')
            if self.ploter.data_type == 'Raw':
                self.ploter.prepare_and_plot(data=self.dataset_package.data)
            elif self.ploter.data_type == 'Detrend':
                self.ploter.prepare_and_plot(data=self.dataset_package.dt_data)
            elif self.ploter.data_type == 'Log':
                self.ploter.prepare_and_plot(data=self.dataset_package.log_data)
        except Exception as inst:
            logger.error(f'ploter panel: {inst}', exc_info=True)
        finally:
            #self.ploter.visible = True
            self._layout.loading = False
            #perror('on_plot after', self.ploter.width, self.ploter.height, self.ploter.figure_pane.object.width, self.ploter.figure_pane.object.height)


    def on_sliding_select(self, event):
        """
        Event handler for the sliding select widget.

        Parameters:
        - event: The event object triggered by the sliding select widget.

        Description:
        - This method is called when the value of the sliding select widget changes.
        - It updates the x and y sliders based on the selected value and the draw data.
        """
        if (self.sliding_select.value != 'None') and (self.ploter.draw_data is not None):
            keycode = self.sliding_select.value
            data = self.ploter.draw_data[keycode]
            fig = self.ploter.figure_pane.object
            self.x_slider.start =  int(fig.x_range.start - data[DATA_LENGTH])
            self.x_slider.end = int(data[DATA_LENGTH] + fig.x_range.end)
            self.x_slider.step = 1
            self.x_slider.value = data['x_offset']
            
            self.y_slider.start = fig.y_range.start - data['w_min'] 
            self.y_slider.end = fig.y_range.end + data['w_max']
            self.y_slider.value = data['y_offset']
            self.y_slider.step = (self.y_slider.end - self.y_slider.start) // 100
            
    def on_slider_x(self, event):
        """
        Event handler for the x-slider.

        Adjusts the x-offset of the plotted data based on the slider value.
        Updates the 'x' value kinds of the ColumnDataSource objects accordingly.

        Args:
            event: The event object triggered by the slider.

        Returns:
            None
        """
        if (self.ploter.draw_data is not None) and (self.sliding_select.value in self.ploter.draw_data):
            data_slide = self.ploter.draw_data[self.sliding_select.value]
            delta_x = data_slide['x_offset'] - self.x_slider.value
            data_slide['x_offset'] = self.x_slider.value
            for key, info in data_slide.items():
                if isinstance(info, ColumnDataSource):
                    for key in ['x', 'left', 'right', 'x0', 'x1']:
                        if key in info.data:
                            info.data[key] = [x - delta_x for x in info.data[key]]
    
    def on_slider_y(self, event):
        """
        Event handler for the y-slider.
    
        Adjusts the y-offset of the plotted data based on the slider value.
        Updates the 'y' value kinds of the ColumnDataSource objects accordingly.
    
        Args:
            event: The event object triggered by the slider.
    
        Returns:
            None
        """
        if (self.ploter.draw_data is not None) and (self.sliding_select.value in self.ploter.draw_data):
            fig = self.ploter.figure_pane.object
            info = self.ploter.draw_data[self.sliding_select.value]
            delta_y = info['y_offset'] - self.y_slider.value
            info['y_offset'] = self.y_slider.value

            for key, value in info.items():
                if isinstance(value, ColumnDataSource):
                    for key in ['y', 'top', 'bottom', 'y0', 'y1']:
                        if key in value.data:
                            value.data[key] = [y - delta_y for y in value.data[key]]
            
            old_y_mean = info['y_label']
            info['y_label'] = round(info['w_mean'] + info['y_offset'], 3)
            self.ploter.on_legend()

