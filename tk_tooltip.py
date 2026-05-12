# -*- coding: utf-8 -*-
"""
Created on Mon May  4 17:50:19 2026

@author: Intel Core I9
"""
#from ttkbootstrap.tooltip import ToolTip as TT
from ttkbootstrap.widgets import ToolTip as TT
class ToolTip(TT):       
    def change_text(self,text):
        # Меняем текст
        self.text = text