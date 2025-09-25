# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 11:54:32 2025

@author: Intel Core I9
"""

import tkinter as tk
from tkinter import Tk, ttk, font, filedialog
from inimodule import *

class TabB(ttk.Frame):
    def __init__(self, parent,path):
        super().__init__(parent)
        self.parent = parent
        self.path=path
        self.ini = read_ini( self.path,'QGISPYITPS')
        self.fullscreen_enabled = tk.IntVar(value=int(self.ini['DEFAULT']['fullscreen']))  
        self.init_ui()

    def init_ui(self):
        """self.text = tk.Text(self, width=20, height=10)
        self.text.pack()
        self.text.insert(1.0, 'Hello World!\nFoo\nBar\n\n123\n')
        self.button = ttk.Button(self, text='Append', command=self.on_append)
        self.button.pack()"""
        self.main_directory_select = tk.StringVar(value=str(self.ini['DEFAULT']['pathtoprogram']))
        self.btnBrowse=ttk.Button(self, text="Выбрать место сохранения результата",style='danger.TButton',command=self.set_program_path)
        self.btnBrowse.place(relheight=0.1, relwidth=0.6, relx=0, rely=0)
        
        self.btn1=ttk.Label(self, textvariable=self.main_directory_select,style='secondary.TButton')
        self.btn1.place(relheight=0.1, relwidth=1, relx=0, rely=0.1)
        
        self.checkbutton_fullscreen = ttk.Checkbutton(self, text='Полный экран', variable=self.fullscreen_enabled, command=self.checkbutton_changed)
        self.checkbutton_fullscreen.place(relheight=0.1, relwidth=0.2, relx=0, rely=0.32)
        
        self.select_theme()
        
        self.pack(expand=True, fill=tk.BOTH)
    
    def checkbutton_changed(self):
        self.ini = change_ini(self.path,'QGISPYITPS', 'fullscreen', self.fullscreen_enabled.get())
        
    def set_program_path(self):
        self.main_directory=filedialog.askdirectory(parent = self, initialdir = self.main_directory_select.get())
        if len(self.main_directory) > 0:
            self.main_directory_select.set(self.main_directory)
            self.ini = change_ini(self.path,'QGISPYITPS', 'pathtoprogram', self.main_directory)

    def select_theme(self):
        theme1='winnative'
        theme2='clam'
        theme3='alt'
        theme4='default'
        theme5='classic'
        theme6='vista'
        theme7='xpnative'
        self.selected_theme = tk.StringVar(value=self.ini['DEFAULT']['theme'])
        self.theme1_btn = ttk.Radiobutton(self,text=theme1, value=theme1, variable=self.selected_theme, command=lambda: self.select_theme_ini(theme1))
        self.theme1_btn.place(relheight=0.1, relwidth=0.1, relx=0, rely=0.25)
  
        self.theme2_btn = ttk.Radiobutton(self,text=theme2, value=theme2, variable=self.selected_theme, command=lambda: self.select_theme_ini(theme2))
        self.theme2_btn.place(relheight=0.1, relwidth=1, relx=0.11, rely=0.25)
 
        self.theme3_btn = ttk.Radiobutton(self,text=theme3, value=theme3, variable=self.selected_theme, command=lambda: self.select_theme_ini(theme3))
        self.theme3_btn.place(relheight=0.1, relwidth=1, relx=0.22, rely=0.25)
        
        self.theme4_btn = ttk.Radiobutton(self,text=theme4, value=theme4, variable=self.selected_theme, command=lambda: self.select_theme_ini(theme4))
        self.theme4_btn.place(relheight=0.1, relwidth=1, relx=0.33, rely=0.25)
  
        self.theme5_btn = ttk.Radiobutton(self,text=theme5, value=theme5, variable=self.selected_theme, command=lambda: self.select_theme_ini(theme5))
        self.theme5_btn.place(relheight=0.1, relwidth=1, relx=0.44, rely=0.25)
 
        self.theme6_btn = ttk.Radiobutton(self,text=theme6, value=theme6, variable=self.selected_theme, command=lambda: self.select_theme_ini(theme6))
        self.theme6_btn.place(relheight=0.1, relwidth=1, relx=0.55, rely=0.25)
        
        self.theme7_btn = ttk.Radiobutton(self,text=theme7, value=theme7, variable=self.selected_theme, command=lambda: self.select_theme_ini(theme7))
        self.theme7_btn.place(relheight=0.1, relwidth=1, relx=0.66, rely=0.25)
    def select_theme_ini(self, theme): 
        change_ini(self.path,'QGISPYITPS', 'theme', theme)
    
    