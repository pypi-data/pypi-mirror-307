
"""
    Ploter module
"""
__license__ = "GPL"
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
 
import numpy as np
import pandas as pd

import param
import panel as pn
from panel.viewable import Viewer

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FixedTicker, Label, Range1d, BoxAnnotation
from bokeh.palettes import Category20, Category10
from bokeh.core.enums import LegendLocation

from pyDendron.dataname import *
from pyDendron.app_logger import logger, perror

class Ploter(Viewer):
    ANATOMY = 'Anatomy'
    ANATOMY_COLOR = {HEARTWOOD: 'black', 
                     PITH: 'blue', 
                     SAPWOOD:'red', 
                     CAMBIUM:'red',
                     BARK: 'red',
                     'signature_90': 'blue',
                     'signature_75': 'green'}


    width = param.Integer(default=1000, bounds=(50, 4000), step=10)
    height = param.Integer(default=1000, bounds=(50, 4000), step=10)
    figure_title = param.String(' ')
    figure_title_font_size = param.Integer(default=14, bounds=(1, 40), step=1)

    data_type = param.Selector(default='Raw', label='Data type *', objects=['Raw', 'Log', 'Detrend'], doc='where is the data')
    color = param.Selector(default=ANATOMY, objects=['None', KEYCODE, ANATOMY], 
            doc=f'None: all black, {KEYCODE}: one color per {KEYCODE}, {ANATOMY}: color pith, sapwood... ')
    draw_type = param.Selector(default='Line', label='Draw type *', objects=['Line', 'Step', 'Timeline'], doc='Line draw type.') 
    group_by = param.Selector(default=None, label='Group by *', objects=[None, TAG, CATEGORY, KEYCODE, DATE_END], doc='group by')
    #draw_selection = param.Boolean(False, label='Draw selection', doc='Draw only selected series in package')
    
    x_offset_mode = param.Selector(default=DATE_BEGIN, label='X offset mode *', objects=['None', DATE_BEGIN, OFFSET], doc='Delay of the rings')
    y_offset_mode = param.Selector(default='Stack', label='Y offset mode *', objects=['Zero', 'Stack'], doc='y curve position')
    y_height = param.Selector(default='[0, max]', label='Y Height *', objects=['[0, max]', '[min, max]'], doc='height of a serie')
    y_delta = param.Number(default=0, label='Y Delta *', doc='marge between two series')
    x_range_step = param.Integer(default=25, bounds=(5, 200), step=5)
    axis_marge = param.Integer(default=35, bounds=(0, 500), step=5)
    axis_font_size = param.Integer(default=10, bounds=(1, 20), step=1)

    cambium_estimation = param.Boolean(True, label= 'Cambium estimation *', doc='Draw cambium estimation')
    show_dates = param.Boolean(True, doc='Add dates at the start and end of the serie')
    show_estimated_dates = param.Boolean(True, doc='Add estimated dates at the end of the serie')
    show_cambium_season = param.Boolean(True, doc='Add cambium season at the end of the serie')

    curve_axe = param.Selector(default='1 mm', label='Curve axe *', objects=['None', '1 mm', '0 mm', 'Mean'], doc=f'position of {KEYCODE} axe')
    anatomy = param.Selector(default='Axe', label='Anatomy *', objects=['Curve', 'Axe'], doc='color of the curve')
    
    line_width_tree = param.Number(default=0.5, bounds=(0.25, 4.0), step=0.25)
    line_width_mean = param.Number(default=1, bounds=(0.25, 4.0), step=0.25)
    marker_size = param.Integer(default=1, bounds=(1, 100), step=1)

    legend = param.Selector(default=KEYCODE, label='Legend *', objects=[KEYCODE, 'Number', 'Number+' + KEYCODE, 'None'], doc=f'legend type')
    legend_location = param.Selector(default='Curve begin', label='Legend location *', objects=['None', 'Axe Y', 'Curve begin', 'Curve end']+[loc for loc in LegendLocation], doc='Legend location')
    legend_font_size = param.Integer(default=10, bounds=(1, 20), step=1)
    #grid_line_visible = param.Boolean(False, doc='Show grid line')

    signature_75 = param.Boolean(False, doc='Signature 75')
    signature_90 = param.Boolean(False, doc='Signature 90')
    
    border = param.Boolean(False, doc='Log transform')
    
    def __init__(self, ploter_name='ploter', **params):
        super(Ploter, self).__init__(**params)   
        self.ploter_name = ploter_name
        self.draw_data = None
        self.draw_group = None 
        self.data = None
        self.x_range, self.y_range = None, None
        self.figure_pane = pn.pane.Bokeh(height=self.height, width=self.width)
        self.clear()
        self._layout = self.figure_pane
        perror('Ploter init', self.width, self.height)
 
    def __panel__(self):
        return self._layout
                
    #@param.depends("width", watch=True)
    def _update_width(self):
        self.figure_pane.width = self.width

    #@param.depends("height", watch=True)
    def _update_height(self):
        self.figure_pane.height = self.height
    
    def get_pith_optimun(self, data_len):
        return int(data_len*0.1)
 
    def prepare_data(self, data):
        self.data = data

        def init_ColumnDataSource():
            return ColumnDataSource()

        def get_x_offset(row):
            if self.x_offset_mode == 'None':
                return 0
            elif self.x_offset_mode == DATE_BEGIN:
                return row[DATE_BEGIN]
            return row[OFFSET]

        def get_y_offset(row, cum_y_offset):
            data = row[DATA_VALUES]
            v = self.y_delta
            if self.draw_type == 'Timeline':
                v += 50
            else:
                v += np.nanmax(data) if self.y_offset_mode == 'Stack' else 0
            cum_y_offset += v
            return v, cum_y_offset
        
        def get_values(row, info):
            values = row[DATA_VALUES]

            sapwood_offset = row[SAPWOOD]
            info[SAPWOOD] = init_ColumnDataSource()
            info[HEARTWOOD] = init_ColumnDataSource()

            if pd.isna(sapwood_offset) or sapwood_offset < 0:
                sapwood_offset = len(values) - 1
                info['sapwood_offset'] = sapwood_offset 
            info[HEARTWOOD].data['x'] = np.arange(0, sapwood_offset + 1) + info['x_offset']
            
            info[HEARTWOOD].data['w'] = values[:sapwood_offset + 1]
            info[HEARTWOOD].data['y'] = info[HEARTWOOD].data['w'] + info['y_offset'] 
            
            info['is_sapwood'] = not(pd.isna(sapwood_offset) or sapwood_offset < 0)
            info[SAPWOOD].data['x'] = np.arange(sapwood_offset, len(values)) + info['x_offset']
            info[SAPWOOD].data['w'] = values[sapwood_offset:]
            info[SAPWOOD].data['y'] = info[SAPWOOD].data['w'] + info['y_offset']
            
        def get_missing_ring(row, info):
            values = row[DATA_VALUES]
            begin = np.where(~np.isnan(values))[0][0]
            end = np.where(~np.isnan(values))[0][-1]
            
            if begin > 0:
                info[MISSING_RING_BEGIN] = init_ColumnDataSource()
                info[MISSING_RING_BEGIN].data['x'] = np.arange(0, begin) + info['x_offset']
                info[MISSING_RING_BEGIN].data['w'] = [values[begin]] * begin
                info[MISSING_RING_BEGIN].data['y'] = [values[begin] + info['y_offset']] * begin 
            if end < len(values):
                info[MISSING_RING_END] = init_ColumnDataSource()
                info[MISSING_RING_END].data['x'] = np.arange(end, len(values)) + info['x_offset']
                info[MISSING_RING_END].data['w'] = [values[end]] * (len(values) - end)
                info[MISSING_RING_END].data['y'] = [values[end] + info['y_offset']] * (len(values) - end) 
            
        def get_pith(row, info):
            values = row[DATA_VALUES] 
            x_min = info['x_offset']
            i = np.where(~np.isnan(values))[0][0]
            w = values[i]
            info[PITH] = init_ColumnDataSource()
            if pd.notna(row[PITH]) and row[PITH]:
                info[PITH].data['x'] = [info['x_offset']]
                info[PITH].data['w'] = [w]
                info[PITH].data['y'] = [get_y(info, w)]
            return x_min
                
        def get_cambium(row, info):
            info['is_cambium_estimated'] = False
            values = row[DATA_VALUES]
            x = len(values) - 1
            x_max = x + info['x_offset']

            w = values[np.where(~np.isnan(values))[0][-1]]
            info[CAMBIUM] = init_ColumnDataSource()
            info[CAMBIUM_ESTIMATED] = init_ColumnDataSource()
            info[CAMBIUM_BOUNDARIES] = init_ColumnDataSource()
            if pd.notna(row[CAMBIUM]) and row[CAMBIUM]:
                info[CAMBIUM].data['x'] = [x + info['x_offset']]
                info[CAMBIUM].data['w'] = ['NA']
                info[CAMBIUM].data['y'] = [get_y(info, w)]
            else:
                if (CAMBIUM_ESTIMATED in row) and row[[CAMBIUM_ESTIMATED, CAMBIUM_LOWER, CAMBIUM_UPPER]].notna().all():
                    info['is_cambium_estimated'] = True

                    lower, estimated, upper = row[CAMBIUM_LOWER], row[CAMBIUM_ESTIMATED], row[CAMBIUM_UPPER]
                    wo = get_y(info, w)
                    xe = estimated + info['x_offset']
                    xl = lower + info['x_offset']
                    xu = upper + info['x_offset']
                    
                    diff_h = (np.nanmax(values) - min(np.nanmin(values), 0)) / 5
                    h = 25 if diff_h > 25 else diff_h
                    h = 0.5 if h < 0.5 else h
                    #perror(f'---> {row[KEYCODE]} {diff_h} {h} {np.nanmax(values)} {np.nanmin(values)}')
                    #h = d if d < 25 else 25
                    info[CAMBIUM_BOUNDARIES].data['x'] = np.arange(xl, xu+1) 
                    info[CAMBIUM_BOUNDARIES].data['w'] = np.array(['NA']*(xu-xl+1))
                    info[CAMBIUM_BOUNDARIES].data['y'] =  np.array([get_y(info, w)]*(xu-xl+1))
                    
                    info[CAMBIUM_ESTIMATED].data['x0'] = [xu, xe, xl]
                    info[CAMBIUM_ESTIMATED].data['x1'] = [xu, xe, xl]
                    info[CAMBIUM_ESTIMATED].data['w'] = ['NA'] * 3
                    info[CAMBIUM_ESTIMATED].data['y0'] = [wo - h] * 3
                    info[CAMBIUM_ESTIMATED].data['y1'] = [wo + h] * 3
                    x_max = xu if xu > x_max else x_max
                elif (CAMBIUM_ESTIMATED in row) and row[[CAMBIUM_ESTIMATED, CAMBIUM_LOWER, CAMBIUM_UPPER]].notna().any():
                    logger.warning(f'Incomplet cambium estimation for {row[KEYCODE]}')
                    
            return x_max

        def get_bark(row, info):
            values = row[DATA_VALUES]
            x = len(values)
            w = values[np.where(~np.isnan(values))[-1]]
            info[BARK] = init_ColumnDataSource()
            if pd.notna(row[BARK]) and row[BARK]:
                info[BARK].data['x'] = [x + info['x_offset']]
                info[BARK].data['w'] = [w]
                info[BARK].data['y'] = [get_y(info, w)]
                
        def get_border(row, info):
            info['border'] = init_ColumnDataSource()
            info['border'].data['top'] = [info['y_max']]
            info['border'].data['bottom'] = [info['y_min']]
            info['border'].data['left'] = [info['x_min']]
            info['border'].data['right'] = [info['x_max']]
            
        def get_min_max(row, info):
            info['x_min'] = get_pith(row, info)
            info['x_max'] = get_cambium(row, info)
            info['w_min'] = np.nanmin(row[DATA_VALUES])
            info['w_max'] = np.nanmax(row[DATA_VALUES])
            info['w_mean'] = np.nanmean(row[DATA_VALUES])
            info['y_min'] = info['y_offset'] #info['w_min'] + info['y_offset']
            info['y_max'] = next_cum_y_offset
            info['y_mean'] = info['w_mean'] + info['y_offset']
            info['y_label'] = round(info['y_mean'], 3)    
        
        def get_text(row, i, info):
            def add_text(value, text):
                if (value is None) or pd.isna(value):
                    return text
                if text != '':
                    text += ' \u2014 '
                return text + f'{value}'
            
            info['text_begin'] = init_ColumnDataSource()
            info['text_begin'].data['x'] = [info['x_min']]
            info['text_begin'].data['y'] = [info['y_mean']]
            info['text_end'] = init_ColumnDataSource()
            info['text_end'].data['x'] = [info['x_max']]
            info['text_end'].data['y'] = [info['y_mean']]
            text_begin = ''
            text_end = ''
            
            keycode = self.get_legend(i, info[KEYCODE])
            if self.legend_location == 'Curve begin':
                text_begin = add_text(keycode, text_begin)
            elif self.legend_location == 'Curve end':
                text_end = add_text(keycode, text_end)
            if self.show_dates :
                text_begin = add_text(row[DATE_BEGIN], text_begin)
                text_end = add_text(row[DATE_END], text_end)
            if self.show_estimated_dates and info['is_cambium_estimated']:
                b = row[DATE_BEGIN]
                lower, estimated, upper = b + row[CAMBIUM_LOWER], b + row[CAMBIUM_ESTIMATED], b + row[CAMBIUM_UPPER]
                text_end += f' [{lower}, {estimated}, {upper}]'
            if self.show_cambium_season and (pd.notna(row[CAMBIUM_SEASON]) and (row[CAMBIUM_SEASON] != '')):
                text_end = add_text(f'\U0001FA93 {row[CAMBIUM_SEASON]}', text_end)
            
            info['text_begin'].data['text'] = [text_begin]
            info['text_end'].data['text'] = [text_end]
        
        def get_curve_axe(row, info):
            info['axe'] = self.curve_axe != 'None'
            if self.curve_axe == '1 mm':
                if self.data_type == 'Raw':
                    y = info['y_offset'] + 100 - info['norm_min']
                elif self.data_type == 'Log':
                    y = info['y_offset'] + np.log(100) - info['norm_min']
                else:
                    logger.warning('Curve axe 1 mm not available in Detrend mode, set to 0 mm')
                    y = info['y_offset'] - info['norm_min']
            elif self.curve_axe == '0 mm':
                y = info['y_offset'] - info['norm_min']
            elif self.curve_axe == 'Mean':
                y = info['y_offset'] + np.nanmean(row[DATA_VALUES])
            if info['axe']:
                info[f'axe_{HEARTWOOD}'] = init_ColumnDataSource()
                info[f'axe_{HEARTWOOD}'].data['y'] = [y]
                info[f'axe_{SAPWOOD}'] = init_ColumnDataSource()
                info[f'axe_{SAPWOOD}'].data['y'] = [y]
        
        def get_curve_axe_value(row, info):
            if info['axe']:
                info[f'axe_{HEARTWOOD}'].data['x0'] = [info[HEARTWOOD].data['x'][0]]
                info[f'axe_{HEARTWOOD}'].data['x1'] = [info[HEARTWOOD].data['x'][-1]]
                info[f'axe_{SAPWOOD}'].data['x0'] = [info[SAPWOOD].data['x'][0]]
                info[f'axe_{SAPWOOD}'].data['x1'] = [info[SAPWOOD].data['x'][-1]]
            
        def get_signatures(row, info):
            if row[CATEGORY] != MEAN:
                return
            sig = row[DATA_SIGNATURES]
            values = row[DATA_VALUES]
            if sig is None:
                return
            if self.signature_75:
                mask = (sig >= 0.75) #& (sig < 0.9)
                mask = np.concatenate([(mask[:-1] | mask[1:]), mask[-1:]])
                v = copy.deepcopy(values)
                v[~mask] = np.nan
                info['signature_75'] = init_ColumnDataSource()
                info['signature_75'].data['x'] = np.arange(0, len(sig)) + info['x_offset']
                info['signature_75'].data['w'] = v
                info['signature_75'].data['y'] = info['signature_75'].data['w'] + info['y_offset']
            if self.signature_90:
                mask = (sig >= 0.9)
                mask = np.concatenate([(mask[:-1] | mask[1:]), mask[-1:]])
                v = copy.deepcopy(values)
                v[~mask] = np.nan
                info['signature_90'] = init_ColumnDataSource()
                info['signature_90'].data['x'] = np.arange(0, len(sig)) + info['x_offset']
                info['signature_90'].data['w'] = v
                info['signature_90'].data['y'] = info['signature_90'].data['w'] + info['y_offset']
        
        def get_y(info, dy):
            if self.anatomy == 'Axe' and info['axe']:
                return info[f'axe_{HEARTWOOD}'].data['y'][0]
            return dy + info['y_offset']
        
        draw = {}
        dgroup = {}
        data = data.loc[data[CATEGORY].isin([MEAN, MEASURE]),:]
        if self.x_offset_mode != 'None':
            if data[self.x_offset_mode].isna().any():
                logger.error(f"NA value(s) in {self.x_offset_mode} column, can't draw")
                self.draw_data = None
                return
                    
        cum_y_offset = 0
        group_by = self.group_by if self.group_by is not None else [0]*len(data)
        for group, df in data.groupby(group_by):
            grp = {}
            grp['name'] = group
            grp['y0'] = cum_y_offset
            for i, (_, row) in enumerate(reversed(list(df.iterrows()))):  
                #perror(f'\t row : {row[KEYCODE]}') 
                info = {}
                info['data'] = 'wood'
                info[CATEGORY] = row[CATEGORY]
                row[RAW] = row[DATA_VALUES]

                info['norm_min'] = 0
                if self.y_height == '[min, max]':
                    info['norm_min'] = np.nanmin(row[DATA_VALUES])
                    row[DATA_VALUES] -= info['norm_min']                 
                if self.draw_type == 'Timeline':
                    row[DATA_VALUES] = np.array([100] * row[DATA_LENGTH])
                info['i'] = i
                info[KEYCODE] = row[KEYCODE]
                info['x_offset'] = get_x_offset(row)
                info[DATA_LENGTH] = row[DATA_LENGTH]
                h, next_cum_y_offset = get_y_offset(row, cum_y_offset)
                #print(i, row[KEYCODE], cum_y_offset, h, next_cum_y_offset)
                info['y_offset'] = cum_y_offset
                get_curve_axe(row, info)
                get_values(row, info)
                get_bark(row, info)
                get_missing_ring(row, info)
                get_min_max(row, info)
                get_border(row, info)
                get_text(row, i, info)
                get_curve_axe_value(row, info)
                get_signatures(row, info)
                info['legend_group'] = group
                
                draw[info[KEYCODE]] = info
                cum_y_offset = next_cum_y_offset
            grp['y1'] = cum_y_offset
            dgroup[group] = grp

        self.draw_data = draw
        self.draw_group = dgroup 
        #print('prepare_data end')


    def clear(self):
        self.figure_pane.object =  figure(margin=(5), title='', toolbar_location="left", height=self.height, width=self.width,
                tools="pan,wheel_zoom,box_zoom,reset,hover,save,crosshair,tap,box_edit,freehand_draw")


    #@param.depends('y_delta', 'y_height', 'x_offset_mode', 'anatomy', 
    #               'y_offset_mode', 'draw_type', 'cambium_estimation', 'group_by', 
    #               'legend', 'legend_location', 'show_dates', 'show_estimated_dates', 
    #               'show_cambium_season', 'curve_axe', watch=True)
    def prepare_and_plot_inner(self):
        self.prepare_and_plot(data=self.data)
    
    def prepare_and_plot(self, data=None):
        try:
            #self._layout.loading = True
            if (data is None) or (len(data) == 0):
                self.clear()
                #self._layout.loading = False
                return
            self.prepare_data(data) 
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        #finally:
            #self._layout.loading = False
        
        self.plot()
        #print('end plot')
    
    def on_x_range_step(self, fig=None):
        if fig is None:
            fig = self.figure_pane.object
        if (fig is not None) and pd.notna(fig.x_range.start):
            x_min = fig.x_range.start + self.axis_marge 
            x_max = fig.x_range.end - self.axis_marge + self.x_range_step
            fig.xaxis[0].ticker = FixedTicker(ticks= np.arange(int(x_min), int(x_max), self.x_range_step))
            label = self.x_offset_mode if self.x_offset_mode != 'None' else f'{OFFSET}'
            fig.xaxis[0].axis_label = label
        
    #@param.depends('figure_title', 'figure_title_font_size', watch=True)
    def on_figure_title(self, fig=None):
        if fig is None:
            fig = self.figure_pane.object
        if fig is not None:
            fig.title.text = self.figure_title
            fig.title.text_font_size = str(self.figure_title_font_size) + 'px'
    
    #@param.depends('axis_font_size', watch=True)
    def on_axis_font_size(self, fig=None):
        if fig is None:
            fig = self.figure_pane.object
        if fig is not None:
            fig.yaxis.major_label_text_font_size = f'{self.axis_font_size}px'
            fig.xaxis.major_label_text_font_size = f'{self.axis_font_size}px'
    
    #@param.depends('legend_font_size', watch=True)
    def on_legend_font_size(self, fig=None):
        if fig is None:
            fig = self.figure_pane.object
        if fig is not None:
            fig.legend.label_text_font_size = f'{self.legend_font_size}px'
            #print(fig.legend.label_text_font_size)

    def on_legend_location(self, fig=None):
        if fig is None:
            fig = self.figure_pane.object
        if fig is not None:
            if self.legend_location not in ['None', 'Axe Y', 'Curve begin', 'Curve end']:
                #print(self.legend_location, str(self.legend_location))
                fig.legend.location = self.legend_location
                
    #@param.depends('grid_line_visible', watch=True)
    #def on_grid_line_color(self):
    #    if fig is not None:
    #        fig.ygrid.grid_line_color = fig.xgrid.grid_line_color if self.grid_line_visible else None

    def get_legend(self, i, keycode):
        if self.legend == 'Number+' + KEYCODE: 
            return f'[{i}] {keycode}'
        elif self.legend == 'Number':
            return str(i)
        elif self.legend == KEYCODE:
            return keycode
        return ''

    def on_group(self, fig=None):
        if fig is None:
            fig = self.figure_pane.object
        if self.group_by is None:
            return
        
        x0 = fig.x_range.start
        x1 = fig.x_range.end
        fs = str(self.legend_font_size)+'px'
        if len(self.draw_group) <= 10:
            colors = Category10[max(len(self.draw_group), 3)]
        else:
            colors = Category20[len(self.draw_group)] if len(self.draw_group) <= 20 else Category20[20]
        boxes = []
        for id, (grp, info) in enumerate(self.draw_group.items()):
            color = colors[id % len(colors)]
            boxes.append(BoxAnnotation(top=info['y1'], bottom=info['y0'], left=x0, right=x1,  fill_alpha=0.1, fill_color=color, 
                                       border_radius = 5, line_width=1, line_color=color, editable = True, resizable='all', movable='both'))
            
            label = Label(x=x0, y=info['y1'], anchor="top_left", text=str(grp), editable = True, 
                  text_color='black', text_font_size=fs, text_font_style='bold italic', x_offset=10, y_offset=0)
            fig.add_layout(label)
            
        fig.renderers.extend(boxes)
        
    def on_legend(self, fig=None):
        if fig is None:
            fig = self.figure_pane.object
        if fig is not None:            
            y_labels = {}
            for i, (keycode, info) in enumerate(self.draw_data.items()):                 
                y_labels[info['y_label']] = self.get_legend(i, keycode)
            #print(y_labels)
            #print('-'*10)
            #print(self.legend_location)
            if self.legend_location == 'None':
                fig.legend.visible = False
                fig.yaxis.visible = False
            elif self.legend_location == 'Axe Y':
                fig.legend.visible = False
                fig.yaxis.visible = True
                fig.yaxis.ticker = list(y_labels.keys())
                fig.yaxis.major_label_overrides = y_labels
                #print(fig.yaxis.major_label_overrides)
            elif self.legend_location.startswith('Curve'):
                fig.legend.visible = False
                fig.yaxis.visible = False
                fig.ygrid.grid_line_color = None
            else:
                fig.legend.visible = True
                fig.yaxis.visible = True
                fig.yaxis.ticker = list(y_labels.keys())
                fig.yaxis.major_label_overrides = y_labels
                #print(fig.yaxis.major_label_overrides)
                fig.legend.location = self.legend_location #"top_left"
                fig.legend.click_policy="mute"
                fig.ygrid.grid_line_color = None
       
    def get_color(self, kind, rank):
        if self.color == self.ANATOMY:
            return self.ANATOMY_COLOR[kind]
        elif self.color == KEYCODE:
            if len(self.draw_data)  <= 10:
                return Category10[10][rank]
            else:
                return Category20[20][rank % 20]
        return 'black'
    
    def get_label_legend(self, i, info):
        return f'{i} - {info[KEYCODE]}'
    
    #@param.depends( 'border', 'x_range_step', 
    #               'line_width_tree', 'line_width_mean', 'circle_radius', 'color', 'axis_marge', 'legend_font_size',
    #               watch=True)
    def plot(self, x_range = None, y_range = None):   
        #logger.debug('plot')
        #self._layout.loading = True
        try:

            # save x_range and y_range values for next plot (usefull for ligt ploter)
            if x_range is not None:
                self.x_range = x_range
            if y_range is not None:
                self.y_range = y_range
                
            #('ploter')
            if self.draw_data is None:
                return
            
            fig = figure(margin=(5), title=self.figure_title, toolbar_location="left", #height=self.height, width=self.width,
                tools="pan,wheel_zoom,box_zoom,reset,hover,save,crosshair,tap,box_edit,freehand_draw", tooltips=[('(date/offset,value)', '(@x, @w)')],
                )
            
            fig.output_backend = "svg"
            radius = self.marker_size
            line_dash = [6, 3]
            
            x = []
            for i, (keycode, info) in enumerate(self.draw_data.items()):
                line_width = self.line_width_tree if info[CATEGORY] == MEASURE else self.line_width_mean
                x.append(info['x_min'])
                x.append(info['x_max'])
                fct = fig.line
                if self.draw_type == 'Step':
                    fct = fig.step
                info['ids'] = []
                fct(x='x', y='y', source=info[HEARTWOOD], line_width=line_width,  color=self.get_color(HEARTWOOD, i), legend_label=self.get_label_legend(i, info))
                fct(x='x', y='y', source=info[SAPWOOD], line_width=line_width,  color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                if info['is_cambium_estimated'] and self.cambium_estimation:
                    fig.segment(x0='x0', y0='y0', x1='x1', y1='y1', source=info[CAMBIUM_ESTIMATED], line_width=line_width, color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                    fct(x='x', y='y', source=info[CAMBIUM_BOUNDARIES], line_dash=line_dash, line_width=line_width, color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                if self.border:
                    fig.quad(top='top', bottom='bottom', left='left', right='right', source=info['border'], line_color='red', alpha=0.05, line_width=1, color='red')
                if MISSING_RING_BEGIN in info:
                    fct(x='x', y='y', source=info[MISSING_RING_BEGIN], line_dash=line_dash, line_width=line_width, color=self.get_color(HEARTWOOD, i), legend_label=self.get_label_legend(i, info))
                if MISSING_RING_END in info:
                    c = self.get_color(SAPWOOD, i) if info['is_sapwood'] else self.get_color(HEARTWOOD, i)
                    fct(x='x', y='y', source=info[MISSING_RING_END], line_dash=line_dash, line_width=line_width, color=c, legend_label=self.get_label_legend(i, info)) 
                    
                fig.scatter(x='x', y='y', source=info[PITH], size=radius,marker="circle" ,color=self.get_color(PITH, i), legend_label=self.get_label_legend(i, info))
                fig.scatter(x='x', y='y', source=info[CAMBIUM], size=radius,marker="circle" ,color=self.get_color(SAPWOOD, i), legend_label=self.get_label_legend(i, info))
                fig.scatter(x='x', y='y', source=info[BARK], size=radius, marker="circle",color=self.get_color(BARK, i), legend_label=self.get_label_legend(i, info))
                
                if info['axe']:
                    fig.segment(x0='x0', y0='y', x1='x1', y1='y', source=info[f'axe_{HEARTWOOD}'], line_width=1, color=self.ANATOMY_COLOR[HEARTWOOD])
                    fig.segment(x0='x0', y0='y', x1='x1', y1='y', source=info[f'axe_{SAPWOOD}'], line_width=1, color=self.ANATOMY_COLOR[SAPWOOD])
                
                if self.signature_75 and 'signature_75' in info:
                    fct(x='x', y='y', source=info['signature_75'], line_width=line_width*2,  color=self.get_color('signature_75', i), legend_label=self.get_label_legend(i, info))
                    #fig.scatter(x='x', y='y', source=info['signature_75'], size=radius, marker="asterisk", color=self.get_color('signature_75', i), legend_label=self.get_label_legend(i, info))
                if self.signature_90 and 'signature_90' in info:
                    fct(x='x', y='y', source=info['signature_90'], line_width=line_width*2,  color=self.get_color('signature_90', i), legend_label=self.get_label_legend(i, info))
                    #fig.scatter(x='x', y='y', source=info['signature_90'], size=radius, marker="asterisk", color=self.get_color('signature_90', i), legend_label=self.get_label_legend(i, info))
                
                fs = str(self.legend_font_size)+'px'
                fig.text(x='x', y='y', text='text', source=info['text_begin'], x_offset=-5 , y_offset=0, anchor="center_right", text_font_size=fs)
                obj = fig.text(x='x', y='y', text='text', source=info['text_end'], x_offset=5 , y_offset=0, anchor="center_left", text_font_size=fs)
                   
            (x_min, x_max) = (np.min(x), np.max(x)) if self.x_range is None else self.x_range
            fig.x_range = Range1d(start=x_min - self.axis_marge, end=x_max + self.axis_marge)
            if self.y_range is not None:
                fig.y_range = Range1d(self.y_range[0], self.y_range[1])

            fig.legend.visible = False
            
            self.on_x_range_step(fig)
            self.on_legend(fig)
            self.on_group(fig)
            self.on_figure_title(fig)
            self.on_axis_font_size(fig)
            self.on_legend_font_size(fig)
            self.figure_pane.object = fig
            self._update_width()
            self._update_height()
            #perror('plot', self.width, self.height, self.figure_pane.object.width, self.figure_pane.object.height)
        except Exception as inst:
            logger.error(f'plot : {inst}', exc_info=True)
        #finally:
        #    self._layout.loading = False


# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from scipy.signal import hann

# def skel_plot(rw_vec, yr_vec=None, sname="", filt_weight=9, dat_out=False, master=False, plot=True):
#     # Validate and handle sname
#     if not sname:
#         sname2 = ""
#     else:
#         sname2 = str(sname)
#         if len(sname2) > 7:
#             raise ValueError("'sname' must be a character string whose width is less than 8")

#     # Remove NaN values from rw_vec and prepare series
#     na_mask = np.isnan(rw_vec)
#     rw_vec2 = rw_vec[~na_mask]
#     n_val = len(rw_vec2)

#     if n_val > 840:
#         raise ValueError("Long series (> 840) must be split into multiple plots")

#     if filt_weight < 3:
#         raise ValueError("'filt.weight' must be greater or equal to 3")

#     if n_val < filt_weight:
#         raise ValueError("'filt.weight' must not be larger than length of input series")

#     # Handle yr_vec
#     if yr_vec is None:
#         yr_vec2 = np.arange(n_val)
#     else:
#         yr_vec2 = yr_vec[~na_mask]

#     # Pad to the nearest decade if needed
#     pad0 = (min(yr_vec2) // 10) * 10
#     if pad0 != min(yr_vec2):
#         pad_length = min(yr_vec2) - pad0
#         pad_data = pd.DataFrame({'rw': [np.nan] * pad_length, 'yr': np.arange(pad0, pad0 + pad_length)})
#         rw_df = pd.concat([pad_data, pd.DataFrame({'rw': rw_vec2, 'yr': yr_vec2})], ignore_index=True)
#     else:
#         rw_df = pd.DataFrame({'rw': rw_vec2, 'yr': yr_vec2})

#     # Detrend using a Hanning window
#     rw_rw = rw_df['rw'].to_numpy()
#     window = hann(filt_weight)
#     rw_dt = np.convolve(rw_rw, window / window.sum(), mode='same')

#     skel = np.full_like(rw_rw, np.nan, dtype=float)

#     # Calculate relative growth
#     temp_diff = np.diff(rw_rw)
#     idx = np.arange(1, len(rw_rw) - 1)
#     skel[idx] = (temp_diff[:-1] + temp_diff[1:]) / (2 * rw_dt[idx])

#     skel[skel > 0] = np.nan  # Keep only negative growth
#     non_na_mask = ~np.isnan(skel)

#     if non_na_mask.any():
#         skel_range = [skel[non_na_mask].min(), skel[non_na_mask].max()]
#         new_range = [10, 1]
#         scale_factor = (new_range[1] - new_range[0]) / (skel_range[1] - skel_range[0])
#         skel = new_range[0] + (skel - skel_range[0]) * scale_factor
#         skel[skel < 3] = np.nan
#         skel = np.ceil(skel)

#     # Plotting if required
#     if plot:
#         plt.figure(figsize=(14, 9))
#         plt.plot(rw_df['yr'], skel, label='Skeleton Plot', color='black')
#         plt.xlabel('Year')
#         plt.ylabel('Skeleton Value')
#         plt.title(f'Skeleton Plot for {sname2}')
#         plt.grid(True)
#         plt.show()

#     if dat_out:
#         return pd.DataFrame({'year': rw_df['yr'], 'skeleton': skel})

# # Example usage:
# # rw_vec = np.array([...])  # Replace with your data
# # yr_vec = np.array([...])  # Replace with your year data if applicable
# # skel_plot(rw_vec, yr_vec, sname="Sample")
