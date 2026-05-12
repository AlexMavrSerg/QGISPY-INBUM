# -*- coding: utf-8 -*-
"""
Created on Mon May 11 15:33:35 2026

@author: Intel Core I9
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets.tableview import Tableview
#from ttkbootstrap.tableview import Tableview
import pandas as pd
from tkinter import filedialog

class tk_show_mean(ttk.Frame):
    def __init__(self,*args):
        super().__init__()
        #for c in range(21): self.rowconfigure(index=c, weight=1) 
        self.name="meanview"
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=12)
        self.rowconfigure(index=2, weight=1)
        self.rowconfigure(index=3, weight=1)
        self.rowconfigure(index=4, weight=1)
        for c in range(11): self.columnconfigure(index=c, weight=1)
        self.create_tableview()
        self.create_another_widgets()
        
    def create_tableview(self):
        column_headers = [{"text": " File" , "stretch": True, "anchor": "center"},
                          {"text": " MEAN"  , "stretch": True, "anchor": "center"},
                          {"text": " type"  , "stretch": True, "anchor": "center"},]
        self.data_table  = Tableview(
                        master     = self,
                        coldata    = column_headers,
                        rowdata    = [],
                        pagesize   = 20,
                        height=20,
                        yscrollbar=True,
                        autofit    = True,
                        paginated  = True,
                        searchable = True,
                        disable_right_click=True,
                        bootstyle  = "info",
                        stripecolor = (self.master.style.colors.light, None),
                       )
        self.data_table.view.bind("<<TreeviewSelect>>", self.on_select)
        self.data_table.grid(row=1,column=0,columnspan=11,rowspan=1, sticky=tk.NSEW)
    def on_cancel(self):
        self.master.change_frame(self,self.master.worked_frames["all6startmainbutton"])
        
    def on_continue(self):
        self.master.tk_air_pollution_select_to_work_frame.show_means()
        self.master.change_frame(self,self.master.tk_air_pollution_select_to_work_frame)
    def on_save(self):
        new_list=[]
        for k in self.master.load_frames_names:
            if k!="all6mainbutton":
                for i in self.master.atm_means_rastrs[k]:
                    new_list.append([i[0],i[1],k]) 
        try:
            pd.DataFrame(new_list).to_excel(str(self.master.ini.settings_get('pathtosave'))+"//output_means.xlsx")
            self.save_label_text.set("OK")
            self.save_label.after(100,lambda: self.save_label_text.set(""))
        except:
            self.save_label_text.set("Error")
            self.save_label.after(150,lambda: self.save_label_text.set(""))
    def on_saveas(self):
        new_list=[]
        filepath=filedialog.asksaveasfile(defaultextension=".xlsx", 
                                          filetypes=[("Excel documents", "*.xlsx"), ("Excel documents", "*.xls"), ("Excel documents", "*.xlsm")])
        if filepath:
            if str(filepath.name).endswith(('.xlsx',)):
                filepath=str(filepath.name)
            else:
                filepath=str(filepath.name)+".xlsx"
            for k in self.master.load_frames_names:
                if k!="all6mainbutton":
                    for i in self.master.atm_means_rastrs[k]:
                        new_list.append([i[0],i[1],k]) 
            try:
                pd.DataFrame(new_list).to_excel(filepath)
                self.save_label_text.set("OK")
                self.save_label.after(100,lambda: self.save_label_text.set(""))
            except:
                self.save_label_text.set("Error")
                self.save_label.after(150,lambda: self.save_label_text.set(""))
    def create_another_widgets(self):
        self.namelabel = ttk.Label(self, anchor="center",textvariable=self.master.transtatedict[self.name])
        self.namelabel.grid(row=0,column=0,columnspan=11, sticky=tk.NSEW)
    
        self.back_button=ttk.Button(self,textvariable=self.master.transtatedict["canceled"],command=self.on_cancel)
        self.back_button.grid(row=4,column=1,columnspan=1, padx=1, pady=1, sticky=tk.NSEW)
        self.continue_button=ttk.Button(self,textvariable=self.master.transtatedict["continued"],command=self.on_continue,state="normal")
        self.continue_button.grid(row=4,column=8,columnspan=2, padx=1, pady=1, sticky=tk.NSEW)
        
        self.save_button=ttk.Button(self,textvariable=self.master.transtatedict["save"],command=self.on_save)
        self.save_button.grid(row=3,column=2,columnspan=2, padx=1, pady=1, sticky=tk.NSEW)
        self.save_label_text=tk.StringVar(value="")
        self.save_label=ttk.Label(self,textvariable=self.save_label_text)
        self.save_label.grid(row=3,column=4,columnspan=1, padx=1, pady=1, sticky=tk.NSEW)
        self.saveas_button=ttk.Button(self,textvariable=self.master.transtatedict["saveas"],command=self.on_saveas)
        self.saveas_button.grid(row=3,column=5,columnspan=2, padx=1, pady=1, sticky=tk.NSEW)
    def show_means(self):
        self.delete_all_rows()
        for k in self.master.load_frames_names:
            if k!="all6mainbutton":
                for i in self.master.atm_means_rastrs[k]:
                    self.data_table.insert_row(index = 'end',values = (i[0],i[1],k))
    def on_select(self,event):
        selected_rows = self.data_table.get_rows(selected=True)
    def del_selected(self):
        selected_rows = self.data_table.get_rows(selected=True)
        for k in selected_rows:
            index = self.data_table.view.index(k.iid)
            self.data_table.delete_row(index = index)
    def delete_all_rows(self):
        selected_rows = self.data_table.get_rows()
        for k in selected_rows:
            index = self.data_table.view.index(k.iid)
            self.data_table.delete_row(index = index)