# -*- coding: utf-8 -*-
"""
Created on Tue May  5 17:06:24 2026

@author: Intel Core I9
"""

import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showerror,askyesno
from functools import partial
import ttkbootstrap as ttk
from ttkbootstrap.widgets.tableview import Tableview
#from ttkbootstrap.tableview import Tableview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import rasterio
from rasterio.plot import show
from matplotlib.figure import Figure
import os

class tk_loadframe(ttk.Frame):
    def __init__(self,passed=0,name="",*args):
        super().__init__()
        self.name=name
        for c in range(21): self.rowconfigure(index=c, weight=1)   
        for c in range(21): self.columnconfigure(index=c, weight=1)
        #self.colors = self.master.style.colors
        self.create_tableview()
        self.create_another_widgets()
        
    def create_tableview(self):
        column_headers = [{"text": " File" , "stretch": True, "anchor": "center"},
                          {"text": " Path"  , "stretch": True, "anchor": "center"},
                          {"text": " Type"  , "stretch": True, "anchor": "center"},]
        self.data_table  = Tableview(
                        master     = self,
                        coldata    = column_headers,
                        rowdata    = [],
                        pagesize   = 10,
                        height=10,
                        yscrollbar=True,
                        autofit    = True,
                        paginated  = True,
                        searchable = True,
                        bootstyle  = "info",
                        stripecolor = (self.master.style.colors.light, None),
                       )
        self.data_table.view.bind("<<TreeviewSelect>>", self.on_select)
        self.data_table.grid(row=1,column=0,columnspan=17,rowspan=10, sticky=tk.NSEW)
    def get_all_files(self):
        files=[]
        selected_rows = self.data_table.get_rows()
        for i in selected_rows:
            files.append('/'.join(reversed(i.values[0:2])))
        return files
            
    def on_select(self,event):
        selected_rows = self.data_table.get_rows(selected=True)
        if len(selected_rows)==1:
           self.visualise_plot(selected_rows[0].values[0:2])
    def del_selected(self):
        selected_rows = self.data_table.get_rows(selected=True)
        for k in selected_rows:
            index = self.data_table.view.index(k.iid)
            self.data_table.delete_row(index = index)

    def create_another_widgets(self):
        self.namelabel = ttk.Label(self, anchor="center",textvariable=self.master.transtatedict[self.name])
        self.namelabel.grid(row=0,column=0,columnspan=21, sticky=tk.NSEW)
        
        self.loadone_button=ttk.Button(self,textvariable=self.master.transtatedict["loadone"],command=self.load_rastr)
        self.loadone_button.grid(row=12,column=4,columnspan=3, padx=2, pady=2, sticky=tk.NSEW)
        self.loaddir_button=ttk.Button(self,textvariable=self.master.transtatedict["loaddir"],command=self.func_load_rastr_dir)
        self.loaddir_button.grid(row=14,column=4,columnspan=3, padx=2, pady=2, sticky=tk.NSEW)
        self.deletesel_button=ttk.Button(self,textvariable=self.master.transtatedict["deletesel"],command=self.del_selected)
        self.deletesel_button.grid(row=12,column=0,columnspan=3, padx=2, pady=2, sticky=tk.NSEW)
        
        self.cancel_button=ttk.Button(self,textvariable=self.master.transtatedict["canceled"],command=partial(self.master.change_frame,self,self.master.main_frame))
        self.cancel_button.grid(row=15,column=1,columnspan=4, padx=2, pady=2, sticky=tk.NSEW)
        
        self.change_frames_buttons={}
        r,c=0,0
        for i in self.master.load_frames_names:
            self.change_frames_buttons[i]=ttk.Button(self,textvariable=self.master.transtatedict[i])
            self.change_frames_buttons[i].grid(row=0+r,column=20+c,columnspan=2, padx=2, pady=2, sticky=tk.NSEW)
            if i==self.name: self.change_frames_buttons[i].config(state="disable")
            if r+1<10: r+=1
            else: r=0; c-=2
        
        self.fig = Figure(figsize=(5, 3.5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=12,column=11,columnspan=10,rowspan=10, sticky=tk.NSEW)
    def shape_rastr_load_check(self):
        rastr_c=0
        for row in self.data_table.get_rows():
            if "rastr" in row.values:
               rastr_c=1   
            if rastr_c==1: return True
        return False
    def load_shape(self):
        find=0
        for row in self.data_table.get_rows():
            if "shape" in row.values:
                result = askyesno(title="Подтвержение операции", message="""Может быть загружен только 1 шейп.
                                                                            Перезаписать?""")
                if result: 
                    find=1 
                    row_iid=row.iid
                    break
                else: 
                    find=2
                    break
        if find==0:
            file=self.func_load_shape()
            if file:
                self.data_table.insert_row(index = 0, values = file+("shape",))
        elif find==1:
            file=self.func_load_shape()
            if file:
                self.data_table.delete_row(index = self.data_table.view.index(row_iid))
                self.data_table.insert_row(index = 0, values = file+("shape",))
                self.data_table.load_table_data()
            
    def add_rows(self,files,mark,pos):
        for i in range(len(files)):
            self.data_table.insert_row(index = pos[i],values = files[i]+(mark,))
        self.data_table.load_table_data()
            
    def func_load_shape(self):   
        filetypes_for = (("Все типы", "*.shp"),
                   #("Все типы", "*.shx"),
                   #("Все типы", "*.prj"),
                   #("Все типы", "*.dbf"),
                   #("Все типы", "*.cpg"),
                   ("Шейп файл 1", "*.shp"))
                   #("Шейп файл 2", "*.shx"),
                   #("Шейп файл 3", "*.prj"),
                   #("Шейп файл 4", "*.dbf"),
                   #("Шейп файл 5", "*.cpg"))
        file = filedialog.askopenfilename(title="Выбор файлов",
                                              filetypes=filetypes_for)
        if file:
            [name,path] = os.path.split(str(file))
            return (path,name)
    def load_rastr(self):
        files=self.func_load_rastr()
        if files:
            self.check_rastrs(files)
    def check_rastrs(self,files):
        all_rows=[]
        for row in self.data_table.get_rows():
            all_rows.append(row.values[0:2])     
        errors_list=[]
        for i in files:
            if list(i) in all_rows:
                #showerror("Ошибка", f"{i.join('\\')} уже есть в данном наборе")
                a='/'.join(reversed(i))
                errors_list.append(a)
            else: self.add_rows([i],"rastr",["end"])
        if len(errors_list)>0:
            error_string='\n'.join(errors_list)
            showerror("Ошибка", f"Файлы\n{error_string}\nуже есть в данном наборе")
        self.data_table.load_table_data()
    def func_load_rastr(self):
        filetypes_for = (("Все типы", "*.tiff"),
                   ("Все типы", "*.tif"),
                   ("Растр с геопривязкой", "*.tiff"),
                   ("Растр с геопривязкой 2", "*.tif"))
        files = list(filedialog.askopenfilenames(title="Выбор файлов",
                                              filetypes=filetypes_for))
        new_files=[]
        for i in files:
            [name,path] = os.path.split(str(i))
            new_files.append((path,name))
            
        if files:
            return new_files
    def func_load_rastr_dir(self):
        filetypes_for = ('.tiff' , '.tif')
        directory=filedialog.askdirectory()
        files=[]
        try:
            for file in os.listdir(directory):
                if file.endswith(filetypes_for):
                    files.append((file,directory))
        except:
            pass
        if len(files)>0:
            self.check_rastrs(files)
    def visualise_plot(self,im):
        im='/'.join(reversed(im))
        
        ax = self.fig.add_subplot(111)
        with rasterio.open(im) as raster:
            # Чтение данных в массив NumPy
            #elevation = src.read(1)  # Первый канал
            #fig, ax = plt.subplots(figsize=(8, 8))
            show((raster, 1),ax=ax)
        
        self.canvas.draw()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        