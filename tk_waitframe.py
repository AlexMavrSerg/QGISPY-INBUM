# -*- coding: utf-8 -*-
"""
Created on Wed May  6 12:57:42 2026

@author: User
"""

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets.scrolled import ScrolledText
#from ttkbootstrap.scrolled import ScrolledText

from air_class import air_calc

class tk_waitframe(ttk.Frame):
    def __init__(self,*args):
        super().__init__()
        self.create_widgets()
    
    def start_calc(self):
        self.text_errors.text.delete("1.0", "end")
        self.back_button.config(state="disabled")
        self.progbar.start(10)
        all_values={}
        for i in self.master.load_frames_names:
            all_values[i]=self.master.load_frames[i].get_all_files()
        self.thread =  air_calc(self,self.master.load_frames_names,all_values)
        self.thread.start()
        
    def on_calc(self):
        try:
            self.back_button.config(state="normal")
            del self.thread
        except:
            pass
   
    def forget_grid(self,par):
        if par=="start":
            self.start_button.grid_forget()
            self.stop_button.grid(row=3,column=1,columnspan=1, padx=2, pady=2, sticky=tk.NSEW)
        elif "stop":
            self.stop_button.grid_forget()
            self.start_button.grid(row=3,column=1,columnspan=1, padx=2, pady=2, sticky=tk.NSEW)
    def on_stop(self):
        self.thread.Stop()
    def on_cancel(self):
        
        self.master.change_frame(self,self.master.main_frame)
        
    def on_continue(self):
        self.master.show_mean_frame.show_means()
        self.master.change_frame(self,self.master.show_mean_frame)
    def create_widgets(self):
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=1)
        self.rowconfigure(index=2, weight=10)
        self.rowconfigure(index=3, weight=2)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=1)
        
        self.text_hello=ttk.Label(self,textvariable=self.master.transtatedict["air_wait_hello"],style="purple.TLabel", anchor="center")
        self.text_hello.grid(row=0,column=0,columnspan=3, padx=0, pady=0, sticky=tk.NSEW)
        
        self.progbar_var = tk.IntVar(value=0)
        self.progbar=ttk.Progressbar(self,orient="horizontal", mode="indeterminate", variable=self.progbar_var)
        self.progbar.grid(row=1,column=0,columnspan=3, padx=0, pady=1, sticky=tk.NSEW)
        
        self.text_errors=ScrolledText(self,state="disabled")
        self.text_errors.grid(row=2,column=0,columnspan=3, padx=0, pady=0, sticky=tk.NSEW)
        
        self.back_button=ttk.Button(self,textvariable=self.master.transtatedict["canceled"],command=self.on_cancel)
        self.back_button.grid(row=3,column=0,columnspan=1, padx=2, pady=2, sticky=tk.NSEW)
        
        self.start_button=ttk.Button(self,textvariable=self.master.transtatedict["start"],command=self.start_calc)
        self.start_button.grid(row=3,column=1,columnspan=1, padx=2, pady=2, sticky=tk.NSEW)
        self.stop_button=ttk.Button(self,textvariable=self.master.transtatedict["stop"],command=self.on_stop)
        #self.stop_button.grid(row=3,column=1,columnspan=1, padx=2, pady=2, sticky=tk.NSEW)
        
        self.continue_button=ttk.Button(self,textvariable=self.master.transtatedict["continued"],command=self.on_continue,state="disabled")
        self.continue_button.grid(row=3,column=2,columnspan=1, padx=2, pady=2, sticky=tk.NSEW)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        