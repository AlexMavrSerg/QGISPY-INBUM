# -*- coding: utf-8 -*-
"""
Created on Mon May 11 19:08:37 2026

@author: Intel Core I9
"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.widgets.tableview import Tableview
#from ttkbootstrap.tableview import Tableview

class tk_air_pollution_select_to_work(ttk.Frame):
    def __init__(self,*args):
        super().__init__()
        self.name="meanselectedframe"
        self.rowconfigure(index=0, weight=1)
        self.rowconfigure(index=1, weight=6)
        self.rowconfigure(index=2, weight=2)
        self.rowconfigure(index=3, weight=2)
        self.rowconfigure(index=4, weight=6)
        self.rowconfigure(index=5, weight=1)
        for c in range(15): self.columnconfigure(index=c, weight=1)
        self.create_tableview_on()
        self.create_tableview_off()
        self.create_another_widgets()
    def delete_all_rows(self):
        selected_rows = self.data_table_on.get_rows()
        for k in selected_rows:
            index = self.data_table_on.view.index(k.iid)
            self.data_table_on.delete_row(index = index)
        selected_rows = self.data_table_off.get_rows()
        for k in selected_rows:
            index = self.data_table_off.view.index(k.iid)
            self.data_table_off.delete_row(index = index)
    def show_means(self):
        self.delete_all_rows()
        for k in self.master.load_frames_names:
            if k!="all6mainbutton":
                for i in self.master.atm_means_rastrs[k]:
                    if i[3]==1:
                        self.data_table_on.insert_row(index = 'end',values = (i[0],i[1],k,i[2],i[5]))
                    elif i[3]==0:
                        self.data_table_off.insert_row(index = 'end',values = (i[0],i[1],k,i[2],i[5]))
    def create_tableview_on(self):
        column_headers = [{"text": " File" , "stretch": True, "anchor": "center"},
                          {"text": " MEAN"  , "stretch": True, "anchor": "center"},
                          {"text": " type"  , "stretch": True, "anchor": "center"},
                          {"text": " x"  , "stretch": True, "anchor": "center"},
                          {"text": " y"  , "stretch": True, "anchor": "center"},]
        self.data_table_on  = Tableview(
                        master     = self,
                        coldata    = column_headers,
                        rowdata    = [],
                        pagesize   = 8,
                        height=8,
                        yscrollbar=True,
                        autofit    = True,
                        paginated  = True,
                        searchable = True,
                        disable_right_click=True,
                        bootstyle  = "info",
                        stripecolor = (self.master.style.colors.light, None),
                       )
        self.data_table_on.grid(row=1,column=0,columnspan=15,rowspan=1, sticky=tk.NSEW)
    def create_tableview_off(self):
        column_headers = [{"text": " File" , "stretch": True, "anchor": "center"},
                          {"text": " MEAN"  , "stretch": True, "anchor": "center"},
                          {"text": " type"  , "stretch": True, "anchor": "center"},
                          {"text": " x"  , "stretch": True, "anchor": "center"},
                          {"text": " y"  , "stretch": True, "anchor": "center"},]
        self.data_table_off  = Tableview(
                        master     = self,
                        coldata    = column_headers,
                        rowdata    = [],
                        pagesize   = 8,
                        height=8,
                        yscrollbar=True,
                        autofit    = True,
                        paginated  = True,
                        searchable = True,
                        disable_right_click=True,
                        bootstyle  = "info",
                        stripecolor = (self.master.style.colors.light, None),
                       )
        self.data_table_off.grid(row=4,column=0,columnspan=15,rowspan=1, sticky=tk.NSEW)
    def on_cancel(self):
        self.master.change_frame(self,self.master.show_mean_frame)
        
    def on_continue(self):
        self.master.change_frame(self,self.master.tk_waitframe_air_poll_last)
        
    def on_oned(self):
        selected_rows = self.data_table_off.get_rows(selected=True)
        for j in selected_rows:
            k=j.values
            for i in range(len(self.master.atm_means_rastrs[k[2]])):
                if self.master.atm_means_rastrs[k[2]][i][0]==k[0]:
                    self.master.atm_means_rastrs[k[2]][i][3]=1
                    self.data_table_on.insert_row(index = 'end',values = (self.master.atm_means_rastrs[k[2]][i][0],
                                                                          self.master.atm_means_rastrs[k[2]][i][1],
                                                                          self.master.atm_means_rastrs[k[2]][i][4],
                                                                          self.master.atm_means_rastrs[k[2]][i][2],
                                                                          self.master.atm_means_rastrs[k[2]][i][5]))
                    index = self.data_table_off.view.index(j.iid)
                    self.data_table_off.delete_row(index = index)
                    break
    def on_offed(self):
        selected_rows = self.data_table_on.get_rows(selected=True)
        for j in selected_rows:
            k=j.values
            for i in range(len(self.master.atm_means_rastrs[k[2]])):
                if self.master.atm_means_rastrs[k[2]][i][0]==k[0]:
                    self.master.atm_means_rastrs[k[2]][i][3]=0
                    self.data_table_off.insert_row(index = 'end',values = (self.master.atm_means_rastrs[k[2]][i][0],
                                                                          self.master.atm_means_rastrs[k[2]][i][1],
                                                                          self.master.atm_means_rastrs[k[2]][i][4],
                                                                          self.master.atm_means_rastrs[k[2]][i][2],
                                                                          self.master.atm_means_rastrs[k[2]][i][5]))
                    index = self.data_table_on.view.index(j.iid)
                    self.data_table_on.delete_row(index = index)
                    break
    def create_another_widgets(self):
        self.namelabel = ttk.Label(self, anchor="center",textvariable=self.master.transtatedict[self.name])
        self.namelabel.grid(row=0,column=0,columnspan=11, sticky=tk.NSEW)
        
        self.back_button=ttk.Button(self,textvariable=self.master.transtatedict["canceled"],command=self.on_cancel)
        self.back_button.grid(row=5,column=1,columnspan=2, padx=1, pady=1, sticky=tk.NSEW)
        self.continue_button=ttk.Button(self,textvariable=self.master.transtatedict["continued"],command=self.on_continue, state="normal")
        self.continue_button.grid(row=5,column=7,columnspan=2, padx=1, pady=1, sticky=tk.NSEW)
        
        self.on_button=ttk.Button(self,textvariable=self.master.transtatedict["onened"],command=self.on_oned)
        self.on_button.grid(row=3,column=2,columnspan=2, padx=1, pady=1, sticky=tk.NSEW)
        self.off_button=ttk.Button(self,textvariable=self.master.transtatedict["offed"],command=self.on_offed)
        self.off_button.grid(row=3,column=7,columnspan=2, padx=1, pady=1, sticky=tk.NSEW)