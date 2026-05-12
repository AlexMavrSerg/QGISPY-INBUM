# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:26:04 2026

@author: Intel Core I9
"""
import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import rasterio
from rasterio.plot import show
from matplotlib.figure import Figure

class tk_air_poll_visualise(ttk.Frame):
    def __init__(self,*args):
        super().__init__()
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=8)
        self.rowconfigure(index=2, weight=2)
        self.rowconfigure(index=3, weight=2)
        for c in range(20): self.columnconfigure(index=c, weight=1)
        
        self.text_hello=ttk.Label(self,textvariable=self.master.transtatedict["summ_air_end"],style="purple.TLabel", anchor="center")
        self.text_hello.grid(row=0,column=0,columnspan=20, padx=0, pady=0, sticky=tk.NSEW)
        
        self.back_button=ttk.Button(self,textvariable=self.master.transtatedict["canceled"],command=self.on_cancel)
        self.back_button.grid(row=3,column=4,columnspan=3, padx=2, pady=2, sticky=tk.NSEW)
        
        self.continue_button=ttk.Button(self,textvariable=self.master.transtatedict["continued"],command=self.on_continue)
        self.continue_button.grid(row=3,column=15,columnspan=3, padx=2, pady=2, sticky=tk.NSEW)
        
        self.save_button=ttk.Button(self,textvariable=self.master.transtatedict["save"],command=self.on_save)
        self.save_button.grid(row=2,column=2,columnspan=3, padx=1, pady=1, sticky=tk.NSEW)
        self.save_label_text=tk.StringVar(value="")
        self.save_label=ttk.Label(self,textvariable=self.save_label_text)
        self.save_label.grid(row=2,column=6,columnspan=4, padx=1, pady=1, sticky=tk.NSEW)
        self.saveas_button=ttk.Button(self,textvariable=self.master.transtatedict["saveas"],command=self.on_saveas)
        self.saveas_button.grid(row=2,column=12,columnspan=3, padx=1, pady=1, sticky=tk.NSEW)
    def show_all(self):
        fig = Figure(figsize=(8, 6), dpi=100)
        self.canvas = FigureCanvasTkAgg(fig, master=self)
        self.canvas.get_tk_widget().grid(row=1,column=0,columnspan=20,rowspan=1, sticky=tk.NSEW)
        ax = fig.add_subplot()
        show(self.master.atm_sum_rastrs[0],ax=ax,transform=self.master.atm_sum_rastrs[2], cmap='terrain')
        self.canvas.draw()
    def on_continue(self):
        self.master.change_frame(self,self.master.main_frame)
    def on_cancel(self):
        self.master.change_frame(self,self.master.tk_waitframe_air_poll_last)
    def on_save(self):
        try:
            with rasterio.open(str(self.master.ini.settings_get('pathtosave'))+"//output.tif", 'w', **self.master.atm_sum_rastrs[1]) as dst:
                dst.write(self.master.atm_sum_rastrs[0])
            self.save_label_text.set("OK")
            self.save_label.after(100,lambda: self.save_label_text.set(""))
        except:
            self.save_label_text.set("Error")
            self.save_label.after(150,lambda: self.save_label_text.set(""))    
    def on_saveas(self):
        filepath=filedialog.asksaveasfile(defaultextension=".tif", 
                                          filetypes=[("Raster", "*.tif"),])
        if filepath:
            if str(filepath).endswith(('.tif',)):
                filepath=str(filepath.name)
            else:
                filepath=str(filepath.name)+".tif"
            try:
                with rasterio.open(filepath, 'w', **self.master.atm_sum_rastrs[1]) as dst:
                    dst.write(self.master.atm_sum_rastrs[0]) 
                self.save_label_text.set("OK")
                self.save_label.after(100,lambda: self.save_label_text.set(""))
            except:
                self.save_label_text.set("Error")
                self.save_label.after(150,lambda: self.save_label_text.set(""))    