"""
Modal dialog box
"""
__author__ = "Sylvain Meignier"
__copyright__ = "Copyright 2023 Sylvain Meignier, Le Mans Université, LIUM (https://lium.univ-lemans.fr/)"
__license__ = "GPL"

import panel as pn
import param

from pyDendron.app_logger import logger, perror

class MessageBox:
    def __init__(self, template, title, message, buttons):
        self.template = template
        self.title = title
        self.message = message
        self.buttons = buttons
        self.action = False
        
        self.yes = pn.widgets.Button(name='Yes', button_type='primary', visible=False)
        self.yes.on_click(self.on_yes)
        self.no = pn.widgets.Button(name='No', button_type='primary', visible=False)
        self.no.on_click(self.on_no)
        self.cancel = pn.widgets.Button(name='Cancel', button_type='primary', visible=False)
        self.cancel.on_click(self.on_cancel)
        self.ok = pn.widgets.Button(name='Ok', button_type='primary', visible=False)
        self.ok.on_click(self.on_ok)
        
        self.buttons = pn.Row(self.yes, self.no, self.ok, self.cancel)
        
        for name in buttons:
            if name == 'yes':
                self.yes.visible = True
            elif name == 'no':
                self.no.visible = True
            elif name == 'cancel':
                self.cancel.visible = True
            elif name == 'ok':
                self.ok.visible = True
        
        self.objects =[f'## {self.title}', self.message, self.buttons]
        
    def open(self):
        self.template.modal[0].clear()      
        for obj in self.objects:
            self.template.modal[0].append(obj)  
        self.template.open_modal()
    
    def on_yes(self, event):
        self.action = True
        self.template.close_modal()
        #perror('yes')
    
    def on_no(self, event):
        self.action = False
        self.template.close_modal()
        #perror('no')
    
    def on_cancel(self, event):
        self.action = False
        self.template.close_modal()
        #perror('cancel')
    
    def on_ok(self, event):
        self.action = True
        self.template.close_modal()
        #perror('ok')
    
    # class StringInputBox(MessageBox):
    #     value = Param.String()
    #     def __init__(self, template, title, message):
    #         super().__init__(template, title, message, ['ok', 'cancel'])
    #         self._layout.insert(2, self.param.value)

    # class IntegerInputBox(MessageBox):
    #     value = Param.Integer()
    #     def __init__(self, template, title, message):
    #         super().__init__(template, title, message, ['ok', 'cancel'])
    #         self._layout.insert(2, self.param.value)
