# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 12:04:42 2025

@author: Intel Core I9
"""
import os
import sys
import threading
import tkinter as tk    
from tkinter import Tk, ttk, font, filedialog
from tkinter.messagebox import askyesno
import PIL
from PIL import Image, ImageTk
import time
import pandas as pd
import processing
from processing.core.Processing import Processing
import configparser
import rasterio
from osgeo import gdal
import openpyxl

def create_ini(path,name, pathto='C:\\'):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'pathtoprogram': str(pathto),
                         'theme': 'winnative',
                         'fullscreen': '0'}
    with open(path+'\\'+name+'.ini', 'w') as configfile:
      config.write(configfile)

def read_ini(path, name, pathto='C:\\'):
    config = configparser.ConfigParser()
    config.sections()
    if os.path.isfile(path+'\\'+name+'.ini'):
        config.read(path+'\\'+name+'.ini')
    else:
        create_ini(path, name, pathto)
        config.read(path+'\\'+name+'.ini')
    config.sections()
    return config

def change_ini(path, name, section, value):
    config = configparser.ConfigParser()
    config = read_ini(path, name)
    config['DEFAULT'][section] = str(value)
    with open(path+'\\'+name+'.ini', 'w') as configfile:
      config.write(configfile)
    return config

def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True).start()
    return execute

path=os.path.dirname(os.path.abspath(__file__))

class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.dir_path=path
        self.ini = read_ini(path,'QGISPYINBUM', self.dir_path)
        self.fullscreen_enabled = tk.IntVar(value=int(self.ini['DEFAULT']['fullscreen']))
        self.__on_update()
        self.First_Settings()
        self.window.update_idletasks()
        self.filepath_NO2=[]; self.filename_NO2=[]; self.mean_NO2=[]; self.xy_NO2=[]
        self.filepath_SO2=[]; self.filename_SO2=[]; self.mean_SO2=[]; self.xy_SO2=[]
        self.filepath_O3=[]; self.filename_O3=[]; self.mean_O3=[]; self.xy_O3=[]
        self.filepath_HCHO=[]; self.filename_HCHO=[]; self.mean_HCHO=[]; self.xy_HCHO=[]
        self.filepath_CO=[]; self.filename_CO=[]; self.mean_CO=[]; self.xy_CO=[]
        self.filepath_CH4=[]; self.filename_CH4=[]; self.mean_CH4=[]; self.xy_CH4=[]
        self.filename_Rstr=[]; self.filepath_Rstr=[]
        self.danger_const=[1.3, 1, 1.7, 1.3, 0.9, 0.9]
        self.create_widgets()
        self.window.mainloop()
    
    def __on_update(self):
        if self.fullscreen_enabled.get() == 1:
            self.window.attributes("-fullscreen", True)
        else:
            self.window.attributes("-fullscreen", False)
            
    def First_Settings(self):
        self.window.title('QGISPY-INBUM')
        self.window.geometry("1400x720+400+200")
        self.window.resizable(True, True)
        self.window.minsize(1400,720)
        self.window.maxsize(2560,1440)
        self.Default_Font()
    
    def Default_Font(self):
        default_font = font.Font(family="Segoe UI", size=round(self.window.winfo_height()/50), weight="bold")
        self.window.option_add('*Font', default_font)
    
    @thread
    def change_font_recursive(self, widget, new_font):
        """
        Рекурсивно изменяет шрифт всех дочерних виджетов.
        """
        try:
            widget.config(font=new_font)
        except:
            pass
        for child in widget.winfo_children():
            self.change_font_recursive(child, new_font)
        
    def create_widgets(self):
        self.notebook = ttk.Notebook(self.window)
        self.notebook.style = ttk.Style()
        self.notebook.style.theme_use(self.ini['DEFAULT']['theme'])
        self.a_tab = ttk.Frame(self.notebook)
        self.tab_a_init_ui()
        self.notebook.add(self.a_tab, text="Главная Страница")
        self.b_tab = ttk.Frame(self.notebook)
        self.tab_b_init_ui()
        self.notebook.add(self.b_tab, text="Параметры")
        self.c_tab = ttk.Frame(self.notebook)
        self.tab_c_create()
        self.notebook.add(self.c_tab, text="Справка")
        self.d_tab = ttk.Frame(self.notebook)
        self.tab_d_init_ui()
        self.notebook.add(self.d_tab, text="Расчет")
        self.e_tab = ttk.Frame(self.notebook)
        self.tab_e_init_ui()
        self.notebook.add(self.e_tab, text="Калькулятор растров")
        self.f_tab = ttk.Frame(self.notebook)
        self.tab_f_init_ui()
        self.notebook.add(self.f_tab, text="Результат")
        self.Exfr = ttk.Frame(self.notebook)
        self.notebook.add(self.Exfr, text="Выйти")
        
        self.notebook.pack(expand=True, fill=tk.BOTH)
        self.notebook.bind("<Button-1>", self.event_exit)
        self.hide_w(3)
        self.hide_w(4)
        self.hide_w(5)
    
    def tab_a_init_ui(self):
        """Данные о файлах для подгрузки"""
        self.a_tab.selected=-1
        self.a_tab.Image=Image.open(self.dir_path+"\\pngegg.png").resize((20,20),Image.LANCZOS)
        self.a_tab.photo = ImageTk.PhotoImage(self.a_tab.Image)
        """Сохдание виджетов""" 
        self.a_tab.filepath_select = tk.StringVar(value="")
        self.create_Listbox()
        self.Frame_Rastr()
        self.Frame_NO2()
        self.Frame_SO2()
        self.Frame_O3()
        self.Frame_HCHO()
        self.Frame_CO()
        self.Frame_CH4()
        self.btndel=ttk.Button(self.a_tab, text="Удалить",style='danger.TButton',command=self.delete)
        self.btndel.place(relheight=0.04, relwidth=0.2, relx=0, rely=0.61)
        self.lblpath=ttk.Label(self.a_tab, textvariable=self.a_tab.filepath_select,style='secondary.TButton')
        self.lblpath.place(relheight=0.04, relwidth=0.4, relx=0.2, rely=0.61)
        self.a_tab.btnstart=ttk.Button(self.a_tab, text="Начать",style='success.TButton',command=self.startbutton)
        self.a_tab.btnstart.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.65)
        self.a_tab.pack(expand=True, fill=tk.BOTH)
        
    def startbutton(self):
        if len(self.filename_Rstr)==0:
            tk.messagebox.showerror("Ошибка", f"Не выбран векторный файл")
        elif len(self.filename_NO2)==0 and len(self.filename_SO2)==0 and len(self.filename_O3)==0 and len(self.filename_HCHO)==0 and len(self.filename_CO)==0 and len(self.filename_CH4)==0:
            tk.messagebox.showerror("Ошибка", f"Не выбран ни одюин растровый файл")
        else:
            self.ch_w(3)
            self.hide_w(5)
            self.hide_w(4)
            self.hide_w(2)
            self.hide_w(1)
            self.hide_w(0)
            self.global_calc_mean()
        
    def create_Listbox(self):
        self.a_tab.languages_var = tk.StringVar(value=[])
        self.a_tab.lb = tk.Listbox(self.a_tab, listvariable=self.a_tab.languages_var, selectmode=tk.SINGLE)
        self.a_tab.scrollbar = ttk.Scrollbar(self.a_tab, orient="vertical", command=self.a_tab.lb.yview)
        self.a_tab.scrollbar.place(relheight=0.6, relwidth=0.01, relx=0.6, rely=0)
        self.a_tab.lb["yscrollcommand"]=self.a_tab.scrollbar.set
        self.a_tab.lb.place(relheight=0.6, relwidth=0.6, relx=0, rely=0)
        self.a_tab.lb.bind("<<ListboxSelect>>", self.listbox_selected)
    
    def listbox_selected(self, event):
        self.a_tab.filepath_select
        selection = self.a_tab.lb.curselection()
        selected_language = self.a_tab.lb.get(selection[0])
        match self.a_tab.selected:
            case 0:
                index = self.filename_Rstr.index(selected_language)
                self.a_tab.filepath_select.set(self.filepath_Rstr[index])
            case 1:
                index = self.filename_NO2.index(selected_language)
                self.a_tab.filepath_select.set(self.filepath_NO2[index])
            case 2:
                index = self.filename_SO2.index(selected_language)
                self.a_tab.filepath_select.set(self.filepath_SO2[index])
            case 3:
                index = self.filename_O3.index(selected_language)
                self.a_tab.filepath_select.set(self.filepath_O3[index])
            case 4:
                index = self.filename_HCHO.index(selected_language)
                self.a_tab.filepath_select.set(self.filepath_HCHO[index])
            case 5:
                index = self.filename_CO.index(selected_language)
                self.a_tab.filepath_select.set(self.filepath_CO[index])
            case 6:
                index = self.filename_CH4.index(selected_language)
                self.a_tab.filepath_select.set(self.filepath_CH4[index])
                
    def Frame_Rastr(self):
        self.a_tab.Rstr_files = tk.StringVar(value=str(len(self.filename_Rstr)))
        self.a_tab.RstrLb=ttk.Label(self.a_tab,text="Shape. Файлов выбрано ",style='secondary.TButton')
        self.a_tab.RstrLb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0, bordermode=tk.OUTSIDE)
        self.a_tab.RstrLbNum=ttk.Label(self.a_tab,textvariable=self.a_tab.Rstr_files,style='secondary.TButton')
        self.a_tab.RstrLbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0, bordermode=tk.OUTSIDE)
        self.a_tab.Rstrbtnf=ttk.Button(self.a_tab, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(0,1))
        self.a_tab.Rstrbtnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0, bordermode=tk.OUTSIDE)
        self.a_tab.btnRstr=ttk.Button(self.a_tab, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(0,1))
        self.a_tab.btnRstr.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0, bordermode=tk.OUTSIDE)
        self.a_tab.btnRstrfind=tk.Button(self.a_tab, image=self.a_tab.photo,command=lambda: self.add(0))
        self.a_tab.btnRstrfind.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0, bordermode=tk.OUTSIDE)

    def Frame_NO2(self):
        self.a_tab.NO2_files = tk.StringVar(value=str(len(self.filename_NO2)))
        self.a_tab.NO2Lb=ttk.Label(self.a_tab,text="NO2. Файлов выбрано ",style='secondary.TButton')
        self.a_tab.NO2Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.09, bordermode=tk.OUTSIDE)
        self.a_tab.NO2LbNum=ttk.Label(self.a_tab,textvariable=self.a_tab.NO2_files,style='secondary.TButton')
        self.a_tab.NO2LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.09, bordermode=tk.OUTSIDE)
        self.a_tab.NO2btnf=ttk.Button(self.a_tab, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(1,2))
        self.a_tab.NO2btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.09, bordermode=tk.OUTSIDE)
        self.a_tab.btnNO2=ttk.Button(self.a_tab, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(1,2))
        self.a_tab.btnNO2.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.09, bordermode=tk.OUTSIDE)
        self.a_tab.btnNO2find=tk.Button(self.a_tab, image=self.a_tab.photo,command=lambda: self.add(1))
        self.a_tab.btnNO2find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.09, bordermode=tk.OUTSIDE)
   
    def Frame_SO2(self):
        self.a_tab.SO2_files = tk.StringVar(value=str(len(self.filename_SO2)))
        self.a_tab.SO2Lb=ttk.Label(self.a_tab,text="SO2. Файлов выбрано ",style='secondary.TButton')
        self.a_tab.SO2Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.18, bordermode=tk.OUTSIDE)
        self.a_tab.SO2LbNum=ttk.Label(self.a_tab,textvariable=self.a_tab.SO2_files,style='secondary.TButton')
        self.a_tab.SO2LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.18, bordermode=tk.OUTSIDE)
        self.a_tab.SO2btnf=ttk.Button(self.a_tab, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(2,2))
        self.a_tab.SO2btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.18, bordermode=tk.OUTSIDE)
        self.a_tab.btnSO2=ttk.Button(self.a_tab, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(2,2))
        self.a_tab.btnSO2.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.18, bordermode=tk.OUTSIDE)
        self.a_tab.btnSO2find=tk.Button(self.a_tab, image=self.a_tab.photo,command=lambda: self.add(2))
        self.a_tab.btnSO2find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.18, bordermode=tk.OUTSIDE)
           
    def Frame_O3(self):
        self.a_tab.O3_files = tk.StringVar(value=str(len(self.filename_O3)))
        self.a_tab.O3Lb=ttk.Label(self.a_tab,text="O3. Файлов выбрано ",style='secondary.TButton')
        self.a_tab.O3Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.27, bordermode=tk.OUTSIDE)
        self.a_tab.O3LbNum=ttk.Label(self.a_tab,textvariable=self.a_tab.O3_files,style='secondary.TButton')
        self.a_tab.O3LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.27, bordermode=tk.OUTSIDE)
        self.a_tab.O3btnf=ttk.Button(self.a_tab, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(3,2))
        self.a_tab.O3btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.27, bordermode=tk.OUTSIDE)
        self.a_tab.btnO3=ttk.Button(self.a_tab, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(3,2))
        self.a_tab.btnO3.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.27, bordermode=tk.OUTSIDE)
        self.a_tab.btnO3find=tk.Button(self.a_tab, image=self.a_tab.photo,command=lambda: self.add(3))
        self.a_tab.btnO3find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.27, bordermode=tk.OUTSIDE)
   
    def Frame_HCHO(self):
        self.a_tab.HCHO_files = tk.StringVar(value=str(len(self.filename_HCHO)))
        self.a_tab.HCHOLb=ttk.Label(self.a_tab,style='secondary.TButton',text="HCHO. Файлов выбрано ")
        self.a_tab.HCHOLb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.36, bordermode=tk.OUTSIDE)
        self.a_tab.HCHOLbNum=ttk.Label(self.a_tab,textvariable=self.a_tab.HCHO_files,style='secondary.TButton')
        self.a_tab.HCHOLbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.36, bordermode=tk.OUTSIDE)
        self.a_tab.HCHObtnf=ttk.Button(self.a_tab,style='secondary.TButton', text="Выбрать файлы",command=lambda: self.openFile(4,2))
        self.a_tab.HCHObtnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.36, bordermode=tk.OUTSIDE)
        self.a_tab.btnHCHO=ttk.Button(self.a_tab,style='secondary.TButton', text="Выбрать папку",command=lambda: self.openDir(4,2))
        self.a_tab.btnHCHO.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.36, bordermode=tk.OUTSIDE)
        self.a_tab.btnHCHOfind=tk.Button(self.a_tab, image=self.a_tab.photo,command=lambda: self.add(4))
        self.a_tab.btnHCHOfind.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.36, bordermode=tk.OUTSIDE)
   
    def Frame_CO(self):
        self.a_tab.CO_files = tk.StringVar(value=str(len(self.filename_CO)))
        self.a_tab.COLb=ttk.Label(self.a_tab,style='secondary.TButton',text="CO. Файлов выбрано ")
        self.a_tab.COLb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.45, bordermode=tk.OUTSIDE)
        self.a_tab.COLbNum=ttk.Label(self.a_tab,textvariable=self.a_tab.CO_files,style='secondary.TButton')
        self.a_tab.COLbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.45, bordermode=tk.OUTSIDE)
        self.a_tab.CObtnf=ttk.Button(self.a_tab,style='secondary.TButton', text="Выбрать файлы",command=lambda: self.openFile(5,2))
        self.a_tab.CObtnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.45, bordermode=tk.OUTSIDE)
        self.a_tab.btnCO=ttk.Button(self.a_tab,style='secondary.TButton', text="Выбрать папку",command=lambda: self.openDir(5,2))
        self.a_tab.btnCO.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.45, bordermode=tk.OUTSIDE)
        self.a_tab.btnCOfind=tk.Button(self.a_tab, image=self.a_tab.photo,command=lambda: self.add(5))
        self.a_tab.btnCOfind.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.45, bordermode=tk.OUTSIDE)
  
    def Frame_CH4(self):
        self.a_tab.CH4_files = tk.StringVar(value=str(len(self.filename_CH4)))
        self.a_tab.CH4Lb=ttk.Label(self.a_tab,style='secondary.TButton',text="CH4. Файлов выбрано ")
        self.a_tab.CH4Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.54, bordermode=tk.OUTSIDE)
        self.a_tab.CH4LbNum=ttk.Label(self.a_tab,textvariable=self.a_tab.CH4_files,style='secondary.TButton')
        self.a_tab.CH4LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.54, bordermode=tk.OUTSIDE)
        self.a_tab.CH4btnf=ttk.Button(self.a_tab,style='secondary.TButton', text="Выбрать файлы",command=lambda: self.openFile(6,2))
        self.a_tab.CH4btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.54, bordermode=tk.OUTSIDE)
        self.a_tab.btnCH4=ttk.Button(self.a_tab,style='secondary.TButton', text="Выбрать папку",command=lambda: self.openDir(6,2))
        self.a_tab.btnCH4.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.54, bordermode=tk.OUTSIDE)
        self.a_tab.btnCH4find=tk.Button(self.a_tab, image=self.a_tab.photo,command=lambda: self.add(6))
        self.a_tab.btnCH4find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.54, bordermode=tk.OUTSIDE)
    
    def update_files(self):
        self.a_tab.Rstr_files.set(str(len(self.filename_Rstr)))
        self.a_tab.NO2_files.set(str(len(self.filename_NO2)))
        self.a_tab.SO2_files.set(str(len(self.filename_SO2)))
        self.a_tab.O3_files.set(str(len(self.filename_O3)))
        self.a_tab.HCHO_files.set(str(len(self.filename_HCHO)))
        self.a_tab.CO_files.set(str(len(self.filename_CO)))
        self.a_tab.CH4_files.set(str(len(self.filename_CH4)))
    
    def delete(self):
        try:
            selection = self.a_tab.lb.curselection()
            selected_language = self.a_tab.lb.get(selection[0])
        except:
            return
        self.a_tab.lb.delete(selection[0])
        match self.a_tab.selected:
            case 0:
                index = self.filename_Rstr.index(selected_language)
                self.filename_Rstr.pop(index)
                self.filepath_Rstr.pop(index)
            case 1:
                index = self.filename_NO2.index(selected_language)
                self.filename_NO2.pop(index)
                self.filepath_NO2.pop(index)
            case 2:
                index = self.filename_SO2.index(selected_language)
                self.filename_SO2.pop(index)
                self.filepath_SO2.pop(index)
            case 3:
                index = self.filename_O3.index(selected_language)
                self.filename_O3.pop(index)
                self.filepath_O3.pop(index)
            case 4:
                index = self.filename_HCHO.index(selected_language)
                self.filename_HCHO.pop(index)
                self.filepath_HCHO.pop(index)
            case 5:
                index = self.filename_CO.index(selected_language)
                self.filename_CO.pop(index)
                self.filepath_CO.pop(index)
            case 6:
                index = self.filename_CH4.index(selected_language)
                self.filename_CH4.pop(index)
                self.filepath_CH4.pop(index)
        self.update_files()
        
    def add(self,n):
        self.a_tab.lb.delete(0,tk.END)
        match n:
            case 0:
                self.a_tab.selected=0
                if len(self.filename_Rstr)>0:
                    for i in self.filename_Rstr:
                        self.a_tab.lb.insert(tk.END, i)
            case 1:
                self.a_tab.selected=1
                if len(self.filename_NO2)>0:
                    for i in self.filename_NO2:
                        self.a_tab.lb.insert(tk.END, i)
            case 2:
                self.a_tab.selected=2
                if len(self.filename_SO2)>0:
                    for i in self.filename_SO2:
                        self.a_tab.lb.insert(tk.END, i)
            case 3:
                self.a_tab.selected=3
                if len(self.filename_O3)>0:
                    for i in self.filename_O3:
                        self.a_tab.lb.insert(tk.END, i)
            case 4:
                self.a_tab.selected=4
                if len(self.filename_HCHO)>0:
                    for i in self.filename_HCHO:
                        self.a_tab.lb.insert(tk.END, i)
            case 5:
                self.a_tab.selected=5
                if len(self.filename_CO)>0:
                    for i in self.filename_CO:
                        self.a_tab.lb.insert(tk.END, i)
            case 6:
                self.a_tab.selected=6
                if len(self.filename_CH4)>0:
                    for i in self.filename_CH4:
                        self.a_tab.lb.insert(tk.END, i)
    
    def openFile(self,n,types):
        if types == 1:
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
        elif types == 2:
            filetypes_for = (("Все типы", "*.tiff"),
                       ("Все типы", "*.tif"),
                       ("Растр с геопривязкой", "*.tiff"),
                       ("Растр с геопривязкой 2", "*.tif"))
        files = list(filedialog.askopenfilenames(title="Выбор файлов",
                                              filetypes=filetypes_for))
        for i in files:
            (path, name) = os.path.split(str(i))
            self.create_filelist(n,name,path)
        self.update_files()
        self.add(n)
        
    def openDir(self,n,types):
        if types == 1:
            #filetypes_for = ('.shp', '.shx', '.prj', '.dbf', '.cpg')
            filetypes_for = ('.shp')
        elif types == 2:
            filetypes_for = ('.tiff' , '.tif')
        directory=filedialog.askdirectory()
        files=[]
        try:
            for file in os.listdir(directory):
                if file.endswith(filetypes_for):
                    files.append(file)
            for name in files:
                self.create_filelist(n,name,directory)
            self.update_files()
            self.add(n)
        except:
            pass
                
    def create_filelist(self,n,name,path):
        match n:
            case 0:
                if name in self.filename_Rstr:
                    tk.messagebox.showerror("Ошибка", f"{name} уже есть в данном наборе")  
                else: 
                    self.filepath_Rstr.append(path)
                    self.filename_Rstr.append(name)
            case 1:
                 if name in self.filename_NO2:
                     tk.messagebox.showerror("Ошибка", f"{name} уже есть в данном наборе")  
                 else: 
                     self.filepath_NO2.append(path)
                     self.filename_NO2.append(name)
            case 2:
                if name in self.filename_SO2:
                    tk.messagebox.showerror("Ошибка", f"{name} уже есть в данном наборе")  
                else: 
                    self.filepath_SO2.append(path)
                    self.filename_SO2.append(name)
            case 3:
                if name in self.filename_O3:
                    tk.messagebox.showerror("Ошибка", f"{name} уже есть в данном наборе")  
                else: 
                    self.filepath_O3.append(path)
                    self.filename_O3.append(name)
            case 4:
                if name in self.filename_HCHO:
                    tk.messagebox.showerror("Ошибка", f"{name} уже есть в данном наборе")  
                else: 
                    self.filepath_HCHO.append(path)
                    self.filename_HCHO.append(name)
            case 5:
                if name in self.filename_CO:
                    tk.messagebox.showerror("Ошибка", f"{name} уже есть в данном наборе")  
                else: 
                    self.filepath_CO.append(path)
                    self.filename_CO.append(name)
            case 6:
                if name in self.filename_CH4:
                    tk.messagebox.showerror("Ошибка", f"{name} уже есть в данном наборе")  
                else: 
                    self.filepath_CH4.append(path)
                    self.filename_CH4.append(name)         
        
    def tab_b_init_ui(self):
        self.b_tab.main_directory_select = tk.StringVar(value=str(self.ini['DEFAULT']['pathtoprogram']))
        self.b_tab.btnBrowse=ttk.Button(self.b_tab, text="Выбрать место сохранения результата",style='danger.TButton',command=self.set_program_path)
        self.b_tab.btnBrowse.place(relheight=0.1, relwidth=0.6, relx=0, rely=0)
        
        self.b_tab.btn1=ttk.Label(self.b_tab, textvariable=self.b_tab.main_directory_select,style='secondary.TButton')
        self.b_tab.btn1.place(relheight=0.1, relwidth=1, relx=0, rely=0.1)
        
        self.b_tab.checkbutton_fullscreen = ttk.Checkbutton(self.b_tab, text='Полный экран', variable=self.fullscreen_enabled, command=self.checkbutton_changed_btab)
        self.b_tab.checkbutton_fullscreen.place(relheight=0.1, relwidth=0.2, relx=0, rely=0.32)
        
        self.select_theme()
        
        self.b_tab.pack(expand=True, fill=tk.BOTH)
    
    def checkbutton_changed_btab(self):
        self.ini = change_ini(self.dir_path,'QGISPYITPS', 'fullscreen', self.fullscreen_enabled.get())
        self.__on_update()    
        
    def set_program_path(self):
        self.b_tab.main_directory=filedialog.askdirectory(parent = self.b_tab, initialdir = self.b_tab.main_directory_select.get())
        if len(self.b_tab.main_directory) > 0:
            self.b_tab.main_directory_select.set(self.b_tab.main_directory)
            self.ini = change_ini(self.dir_path,'QGISPYITPS', 'pathtoprogram', self.b_tab.main_directory)

    def select_theme(self):
        theme1='winnative'; theme2='clam'; theme3='alt'; theme4='default'; theme5='classic'; theme6='vista'; theme7='xpnative'
        self.b_tab.selected_theme = tk.StringVar(value=self.ini['DEFAULT']['theme'])
        self.b_tab.theme1_btn = ttk.Radiobutton(self.b_tab,text=theme1, value=theme1, variable=self.b_tab.selected_theme, command=lambda: self.select_theme_ini(theme1))
        self.b_tab.theme1_btn.place(relheight=0.1, relwidth=0.1, relx=0, rely=0.25)
        self.b_tab.theme2_btn = ttk.Radiobutton(self.b_tab,text=theme2, value=theme2, variable=self.b_tab.selected_theme, command=lambda: self.select_theme_ini(theme2))
        self.b_tab.theme2_btn.place(relheight=0.1, relwidth=1, relx=0.11, rely=0.25)
        self.theme3_btn = ttk.Radiobutton(self.b_tab,text=theme3, value=theme3, variable=self.b_tab.selected_theme, command=lambda: self.select_theme_ini(theme3))
        self.theme3_btn.place(relheight=0.1, relwidth=1, relx=0.22, rely=0.25)
        self.theme4_btn = ttk.Radiobutton(self.b_tab,text=theme4, value=theme4, variable=self.b_tab.selected_theme, command=lambda: self.select_theme_ini(theme4))
        self.theme4_btn.place(relheight=0.1, relwidth=1, relx=0.33, rely=0.25)
        self.theme5_btn = ttk.Radiobutton(self.b_tab,text=theme5, value=theme5, variable=self.b_tab.selected_theme, command=lambda: self.select_theme_ini(theme5))
        self.theme5_btn.place(relheight=0.1, relwidth=1, relx=0.44, rely=0.25)
        self.theme6_btn = ttk.Radiobutton(self.b_tab,text=theme6, value=theme6, variable=self.b_tab.selected_theme, command=lambda: self.select_theme_ini(theme6))
        self.theme6_btn.place(relheight=0.1, relwidth=1, relx=0.55, rely=0.25)
        self.theme7_btn = ttk.Radiobutton(self.b_tab,text=theme7, value=theme7, variable=self.b_tab.selected_theme, command=lambda: self.select_theme_ini(theme7))
        self.theme7_btn.place(relheight=0.1, relwidth=1, relx=0.66, rely=0.25)

    def select_theme_ini(self, theme): 
        change_ini(self.dir_path,'QGISPYITPS', 'theme', theme)  
        self.notebook.style.theme_use(theme)
        
    def tab_c_create(self):
        self.credits = tk.Text(self.c_tab)
        self.credits.place(relheight=0.95, relwidth=0.95, relx=0, rely=0)
        self.credits.ys = ttk.Scrollbar(self.c_tab,orient = "vertical", command = self.credits.yview)
        self.credits.ys.place(relheight=0.95, relwidth=0.05, relx=0.95, rely=0)
        self.credits.xs = ttk.Scrollbar(self.c_tab,orient = "horizontal", command = self.credits.xview)
        self.credits.xs.place(relheight=0.05, relwidth=0.95, relx=0, rely=0.95)
        self.credits["yscrollcommand"] = self.credits.ys.set
        self.credits["xscrollcommand"] = self.credits.xs.set
        self.credits.insert("1.0", """Команда проекта:
                                    Греков Александр Николаевич
                                    Маврин Александр Сергеевич
                                    Табунщик Владимир""")
        self.credits.configure(state=tk.DISABLED)
        self.c_tab.pack(expand=True, fill=tk.BOTH)       
        
    def tab_d_init_ui(self):
        self.d_tab.text=[]
        self.d_tab.workreader = tk.Text(self.d_tab)
        self.d_tab.workreader.place(relheight=0.25, relwidth=0.95, relx=0, rely=0)
        self.d_tab.workreader.ys = ttk.Scrollbar(self.d_tab,orient = "vertical", command = self.d_tab.workreader.yview)
        self.d_tab.workreader.ys.place(relheight=0.25, relwidth=0.05, relx=0.95, rely=0)
        self.d_tab.workreader.xs = ttk.Scrollbar(self.d_tab,orient = "horizontal", command = self.d_tab.workreader.xview)
        self.d_tab.workreader.xs.place(relheight=0.05, relwidth=0.95, relx=0, rely=0.95)
        self.d_tab.workreader["yscrollcommand"] = self.d_tab.workreader.ys.set
        self.d_tab.workreader["xscrollcommand"] = self.d_tab.workreader.xs.set
        self.d_tab.workreader.insert("1.0", str(self.d_tab.text))
        self.d_tab.workreader.configure(state=tk.DISABLED)
        self.d_tab.pack(expand=True, fill=tk.BOTH)
        self.cred_ins("""\n\n\n          ПОДОЖДИТЕ\n          ИДЕТ ОБРАБОТКА\n\n\n""")
        self.d_tab.btnret=ttk.Button(self.d_tab, text="Назад",style='secondary.TButton', command = self.def_return)
        self.d_tab.btnret.place(relheight=0.2, relwidth=0.5, relx=0.3, rely=0.27)   
        self.d_tab.btncont=ttk.Button(self.d_tab, text="Продолжить\nКалькулятор растров",style='secondary.TButton', command = self.def_continue)
        self.d_tab.btncont.place(relheight=0.2, relwidth=0.5, relx=0.3, rely=0.57) 
        self.d_tab.btncont["state"] = tk.DISABLED
        
    def def_return(self):
        self.d_tab.btncont["state"] = tk.DISABLED
        self.ch_w(2)
        self.ch_w(1)
        self.ch_w(0)
        self.hide_w(3)   
        self.hide_w(4)
        self.hide_w(5)
    
    def def_continue(self):    
        self.d_tab.btncont["state"] = tk.DISABLED
        self.create_view_change_widgets()
        self.ch_w(4)
        self.hide_w(5)
        self.hide_w(3)
        self.hide_w(2)
        self.hide_w(1)
        self.hide_w(0)
        
    def cred_ins(self,text):
        self.d_tab.workreader.configure(state=tk.NORMAL)
        self.d_tab.workreader.delete("0.0", tk.END)
        self.d_tab.workreader.insert(tk.END,text)
        self.d_tab.workreader.configure(state=tk.DISABLED)
        
    def global_calc_mean(self):
        self.d_tab.btnret["text"]="Назад"
        self.cred_ins("""\n\n\n          ПОДОЖДИТЕ\n          ИДЕТ ОБРАБОТКА\n\n\n""")
        if len(self.filename_NO2)>0:
            self.mean_NO2=self.calc_mean(self.filepath_NO2, self.filename_NO2)
            self.xy_NO2=self.calc_height_width(self.filepath_NO2, self.filename_NO2)
        if len(self.filename_SO2)>0:
            self.mean_SO2=self.calc_mean(self.filepath_SO2, self.filename_SO2)
            self.xy_SO2=self.calc_height_width(self.filepath_SO2, self.filename_SO2)
        if len(self.filename_HCHO)>0:
            self.mean_HCHO=self.calc_mean(self.filepath_HCHO, self.filename_HCHO)
            self.xy_HCHO=self.calc_height_width(self.filepath_HCHO, self.filename_HCHO)
        if len(self.filename_CO)>0:
            self.mean_CO=self.calc_mean(self.filepath_CO, self.filename_CO)
            self.xy_CO=self.calc_height_width(self.filepath_CO, self.filename_CO)
        if len(self.filename_CH4)>0:
            self.mean_CH4=self.calc_mean(self.filepath_CH4, self.filename_CH4)
            self.xy_CH4=self.calc_height_width(self.filepath_CH4, self.filename_CH4)
        if len(self.filename_O3)>0:
            self.mean_O3=self.calc_mean(self.filepath_O3, self.filename_O3)
            self.xy_O3=self.calc_height_width(self.filepath_O3, self.filename_O3)
        self.save_excel()
        self.d_tab.btnret["text"]="Готово. Назад"
        self.d_tab.btncont["state"] = tk.NORMAL
        
    def save_excel(self):
        new_list=[]
        if len(self.filename_NO2)>0:
            for i in range(len(self.filename_NO2)):
                new_list.append([self.filename_NO2[i],float(self.mean_NO2[i])])
                self.mean_NO2[i]=[self.filename_NO2[i],float(self.mean_NO2[i]),0, self.xy_NO2[i][0], self.xy_NO2[i][1]]
        if len(self.filename_SO2)>0:
            for i in range(len(self.filename_SO2)):
                new_list.append([self.filename_SO2[i],float(self.mean_SO2[i])])
                self.mean_SO2[i]=[self.filename_SO2[i],float(self.mean_SO2[i]),0, self.xy_SO2[i][0], self.xy_SO2[i][1]]
        if len(self.filename_HCHO)>0:
            for i in range(len(self.filename_HCHO)):
                new_list.append([self.filename_HCHO[i],float(self.mean_HCHO[i])])
                self.mean_HCHO[i]=[self.filename_HCHO[i],float(self.mean_HCHO[i]),0, self.xy_HCHO[i][0], self.xy_HCHO[i][1]]
        if len(self.filename_CO)>0:
            for i in range(len(self.filename_CO)):
                new_list.append([self.filename_CO[i],float(self.mean_CO[i])])
                self.mean_CO[i]=[self.filename_CO[i],float(self.mean_CO[i]),0, self.xy_CO[i][0], self.xy_CO[i][1]]
        if len(self.filename_CH4)>0:   
            for i in range(len(self.filename_CH4)):
                new_list.append([self.filename_CH4[i],float(self.mean_CH4[i])])
                self.mean_CH4[i]=[self.filename_CH4[i],float(self.mean_CH4[i]),0, self.xy_CH4[i][0], self.xy_CH4[i][1]]
        if len(self.filename_O3)>0:
            for i in range(len(self.filename_O3)):
                new_list.append([self.filename_O3[i],float(self.mean_O3[i])])
                self.mean_O3[i]=[self.filename_O3[i],float(self.mean_O3[i]),0, self.xy_O3[i][0], self.xy_O3[i][1]]
        self.cred_ins(str(new_list).replace("]","\n").replace("[","").replace(",",""))
        pd.DataFrame(new_list).to_excel(str(self.ini['DEFAULT']['pathtoprogram'])+"//output.xlsx")
        return True

    def calc_height_width(self,full_file_paths,full_file_names):
        df_orders=[]
        for i in range(len(full_file_names)):
            try:
                Processing.initialize()
                a=processing.run("native:rasterlayerproperties", 
                               {'INPUT': full_file_paths[i]+"\\"+full_file_names[i],
                                'BAND':1})
                df_orders.append([a["WIDTH_IN_PIXELS"], a["HEIGHT_IN_PIXELS"]])
            except Exception as e:
                print(e)
                with open(str(self.ini['DEFAULT']['pathtoprogram'])+"//log.txt", 'a') as file:
                    file.writelines(str(e)) 
        return df_orders  

    def calc_mean(self,full_file_paths,full_file_names):
        df_orders=[]
        for i in range(len(full_file_names)):
            try:
                Processing.initialize()
                processing.run("native:zonalstatisticsfb", 
                               {'INPUT': self.filepath_Rstr[0]+"\\"+self.filename_Rstr[0],
                                'INPUT_RASTER': full_file_paths[i]+"\\"+full_file_names[i],
                                'RASTER_BAND':1,
                                'COLUMN_PREFIX':'_',
                                'STATISTICS':[2],
                                'OUTPUT':self.dir_path+"\\calc_"+full_file_names[i].replace(".tif",".xlsx")},
                               is_child_algorithm=False)
                df_orders.append(pd.read_excel(self.dir_path+"\\calc_"+full_file_names[i].replace(".tif",".xlsx"), index_col=0)["_mean"].iloc[0])
                os.remove(self.dir_path+"\\calc_"+full_file_names[i].replace(".tif",".xlsx"))
            except Exception as e:
                print(e)
                with open(self.dir_path+"//log.txt", 'a') as file:
                    file.writelines(str(e))            
        return df_orders    
        
    
    def tab_e_init_ui(self):
        self.e_tab.h = ttk.Scrollbar(self.e_tab,orient=tk.HORIZONTAL)
        self.e_tab.v = ttk.Scrollbar(self.e_tab,orient=tk.VERTICAL)
        self.e_tab.h.place(relheight=0.1, relwidth=0.98, relx=0, rely=0.765)
        self.e_tab.v.place(relheight=0.8, relwidth=0.1, relx=0.94, rely=0)
        self.e_tab.btncont=ttk.Button(self.e_tab, text="Продолжить",style='secondary.TButton', command = self.def_continue_rastr)
        self.e_tab.btncont.place(relheight=0.11, relwidth=0.2, relx=0.5, rely=0.87)
        self.e_tab.btnret=ttk.Button(self.e_tab, text="Вернуться в меню",style='secondary.TButton', command = self.def_return_rastr)
        self.e_tab.btnret.place(relheight=0.11, relwidth=0.2, relx=0.3, rely=0.87)  
        self.e_tab.btnall=ttk.Button(self.e_tab, text="Включить все",style='secondary.TButton', command = lambda: self.def_all_rastr(1))
        self.e_tab.btnall.place(relheight=0.11, relwidth=0.1, relx=0.8, rely=0.87)
        self.e_tab.btnnothing=ttk.Button(self.e_tab, text="Выключить все",style='secondary.TButton', command = lambda: self.def_all_rastr(0))
        self.e_tab.btnnothing.place(relheight=0.11, relwidth=0.1, relx=0.9, rely=0.87)
        
    def def_all_rastr(self,bu):
        for l in range(len(self.change_var_NO2)):
            self.change_var_NO2[l].set(bu)
        for l in range(len(self.change_var_SO2)):
            self.change_var_SO2[l].set(bu)
        for l in range(len(self.change_var_HCHO)):
            self.change_var_HCHO[l].set(bu)
        for l in range(len(self.change_var_CO)):
            self.change_var_CO[l].set(bu)
        for l in range(len(self.change_var_CH4)):
            self.change_var_CH4[l].set(bu)
        for l in range(len(self.change_var_O3)):
            self.change_var_O3[l].set(bu)    
    
    def def_return_rastr(self):
        self.e_tab.canv_frame.destroy()
        self.ch_w(2)
        self.ch_w(1)
        self.ch_w(0)
        self.hide_w(3)   
        self.hide_w(4)
        self.hide_w(5)    
        
    def def_continue_rastr(self):
        #for l in range(len(self.change_var_NO2)):
        #    print(self.change_var_NO2[l].get())
        #for l in range(len(self.change_var_SO2)):
        #    print(self.change_var_SO2[l].get())
        #for l in range(len(self.change_var_HCHO)):
        #    print(self.change_var_HCHO[l].get())
        #for l in range(len(self.change_var_CO)):
        #    print(self.change_var_CO[l].get())
        #for l in range(len(self.change_var_CH4)):
        #    print(self.change_var_CH4[l].get())
        #for l in range(len(self.change_var_O3)):
        #    print(self.change_var_O3[l].get())
        self.rastr_calculation()
        self.tab_f_visualise()
        self.hide_w(4)
        self.ch_w(5)
      
    def create_view_change_widgets(self):
        length_of_all=(round(len(self.mean_NO2)+len(self.mean_SO2)+len(self.mean_HCHO)+len(self.mean_CO)+len(self.mean_CH4)+len(self.mean_O3))+7)*110
        self.e_tab.canv_frame = ttk.Frame(self.e_tab)
        self.e_tab.canv_frame.place(relheight=0.8, relwidth=0.985, relx=0, rely=0)
        self.e_tab.canvas = tk.Canvas(self.e_tab.canv_frame,scrollregion=(0, 0, 1000, length_of_all), bg="white", yscrollcommand=self.e_tab.v.set, xscrollcommand=self.e_tab.h.set)
        self.e_tab.h["command"] = self.e_tab.canvas.xview
        self.e_tab.v["command"] = self.e_tab.canvas.yview
        self.e_tab.canvas.place(relheight=1, relwidth=1, relx=0, rely=0)
        myx=10
        myy=20
        chk=[]
        self.change_var_NO2=[]
        self.change_var_SO2=[]
        self.change_var_HCHO=[]
        self.change_var_CO=[]
        self.change_var_CH4=[]
        self.change_var_O3=[]
        
        self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="black")
        self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=ttk.Label(text="NO2", background="black", foreground="white"), width=400, height=90)
        myy+=110
        for i in range(len(self.mean_NO2)):
            self.change_var_NO2.append(tk.IntVar(value=1))
            self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="gray")
            txtname=ttk.Label(text=str(self.mean_NO2[i][0]))
            self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=txtname, width=400, height=90)
            txtvalue=ttk.Label(text=str(self.mean_NO2[i][1]))
            self.e_tab.canvas.create_window(myx+410, myy+1, anchor=tk.NW, window=txtvalue, width=200, height=90)
            chk=tk.Checkbutton(variable=self.change_var_NO2[i])
            self.e_tab.canvas.create_window(myx+620, myy+1, anchor=tk.NW, window=chk, width=50, height=90)
            txthight=ttk.Label(text=str(self.mean_NO2[i][3]))
            self.e_tab.canvas.create_window(myx+680, myy+1, anchor=tk.NW, window=txthight, width=50, height=90)
            txtweidth=ttk.Label(text=str(self.mean_NO2[i][4]))
            self.e_tab.canvas.create_window(myx+740, myy+1, anchor=tk.NW, window=txtweidth, width=50, height=90)
            myy+=110
        self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="black")
        self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=ttk.Label(text="SO2", background="black", foreground="white"), width=400, height=90)
        myy+=110
        for i in range(len(self.mean_SO2)):
            self.change_var_SO2.append(tk.IntVar(value=1))
            self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="gray")
            txtname=ttk.Label(text=str(self.mean_SO2[i][0]))
            self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=txtname, width=400, height=90)
            txtvalue=ttk.Label(text=str(self.mean_SO2[i][1]))
            self.e_tab.canvas.create_window(myx+410, myy+1, anchor=tk.NW, window=txtvalue, width=200, height=90)
            chk=tk.Checkbutton(variable=self.change_var_SO2[i])
            self.e_tab.canvas.create_window(myx+620, myy+1, anchor=tk.NW, window=chk, width=50, height=90)
            txthight=ttk.Label(text=str(self.mean_SO2[i][3]))
            self.e_tab.canvas.create_window(myx+680, myy+1, anchor=tk.NW, window=txthight, width=50, height=90)
            txtweidth=ttk.Label(text=str(self.mean_SO2[i][4]))
            self.e_tab.canvas.create_window(myx+740, myy+1, anchor=tk.NW, window=txtweidth, width=50, height=90)
            myy+=110
        self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="black")
        self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=ttk.Label(text="HCHO", background="black", foreground="white"), width=400, height=90)
        myy+=110
        for i in range(len(self.mean_HCHO)):
            self.change_var_HCHO.append(tk.IntVar(value=1))
            self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="gray")
            txtname=ttk.Label(text=str(self.mean_HCHO[i][0]))
            self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=txtname, width=400, height=90)
            txtvalue=ttk.Label(text=str(self.mean_HCHO[i][1]))
            self.e_tab.canvas.create_window(myx+410, myy+1, anchor=tk.NW, window=txtvalue, width=200, height=90)
            chk=tk.Checkbutton(variable=self.change_var_HCHO[i])
            self.e_tab.canvas.create_window(myx+620, myy+1, anchor=tk.NW, window=chk, width=50, height=90)
            txthight=ttk.Label(text=str(self.mean_HCHO[i][3]))
            self.e_tab.canvas.create_window(myx+680, myy+1, anchor=tk.NW, window=txthight, width=50, height=90)
            txtweidth=ttk.Label(text=str(self.mean_HCHO[i][4]))
            self.e_tab.canvas.create_window(myx+740, myy+1, anchor=tk.NW, window=txtweidth, width=50, height=90)
            myy+=110
        self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="black")
        self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=ttk.Label(text="CO", background="black", foreground="white"), width=400, height=90)
        myy+=110
        for i in range(len(self.mean_CO)):
            self.change_var_CO.append(tk.IntVar(value=1))
            self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="gray")
            txtname=ttk.Label(text=str(self.mean_CO[i][0]))
            self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=txtname, width=400, height=90)
            txtvalue=ttk.Label(text=str(self.mean_CO[i][1]))
            self.e_tab.canvas.create_window(myx+410, myy+1, anchor=tk.NW, window=txtvalue, width=200, height=90)
            chk=tk.Checkbutton(variable=self.change_var_CO[i])
            self.e_tab.canvas.create_window(myx+620, myy+1, anchor=tk.NW, window=chk, width=50, height=90)
            txthight=ttk.Label(text=str(self.mean_CO[i][3]))
            self.e_tab.canvas.create_window(myx+680, myy+1, anchor=tk.NW, window=txthight, width=50, height=90)
            txtweidth=ttk.Label(text=str(self.mean_CO[i][4]))
            self.e_tab.canvas.create_window(myx+740, myy+1, anchor=tk.NW, window=txtweidth, width=50, height=90)
            myy+=110
        self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="black")
        self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=ttk.Label(text="CH4", background="black", foreground="white"), width=400, height=90)
        myy+=110
        for i in range(len(self.mean_CH4)):
            self.change_var_CH4.append(tk.IntVar(value=1))
            self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="gray")
            txtname=ttk.Label(text=str(self.mean_CH4[i][0]))
            self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=txtname, width=400, height=90)
            txtvalue=ttk.Label(text=str(self.mean_CH4[i][1]))
            self.e_tab.canvas.create_window(myx+410, myy+1, anchor=tk.NW, window=txtvalue, width=200, height=90)
            chk=tk.Checkbutton(variable=self.change_var_CH4[i])
            self.e_tab.canvas.create_window(myx+620, myy+1, anchor=tk.NW, window=chk, width=50, height=90)
            txthight=ttk.Label(text=str(self.mean_CH4[i][3]))
            self.e_tab.canvas.create_window(myx+680, myy+1, anchor=tk.NW, window=txthight, width=50, height=90)
            txtweidth=ttk.Label(text=str(self.mean_CH4[i][4]))
            self.e_tab.canvas.create_window(myx+740, myy+1, anchor=tk.NW, window=txtweidth, width=50, height=90)
            myy+=110
        self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="black")
        self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=ttk.Label(text="O3", background="black", foreground="white"), width=400, height=90)
        myy+=110
        for i in range(len(self.mean_O3)):
            self.change_var_O3.append(tk.IntVar(value=1))
            self.e_tab.canvas.create_rectangle(0,myy, 1300, myy+100, fill="gray")
            txtname=ttk.Label(text=str(self.mean_O3[i][0]))
            self.e_tab.canvas.create_window(myx, myy+1, anchor=tk.NW, window=txtname, width=400, height=90)
            txtvalue=ttk.Label(text=str(self.mean_O3[i][1]))
            self.e_tab.canvas.create_window(myx+410, myy+1, anchor=tk.NW, window=txtvalue, width=200, height=90)
            chk=tk.Checkbutton(variable=self.change_var_O3[i])
            self.e_tab.canvas.create_window(myx+620, myy+1, anchor=tk.NW, window=chk, width=50, height=90)
            txthight=ttk.Label(text=str(self.mean_O3[i][3]))
            self.e_tab.canvas.create_window(myx+680, myy+1, anchor=tk.NW, window=txthight, width=50, height=90)
            txtweidth=ttk.Label(text=str(self.mean_O3[i][4]))
            self.e_tab.canvas.create_window(myx+740, myy+1, anchor=tk.NW, window=txtweidth, width=50, height=90)
            myy+=110
    
    def rastr_calculation(self):
        sum_raastr=[]
        if len(self.filename_NO2)>0:
            if len(sum_raastr)>0:
                sum_raastr+=self.calc_reastr_end_rasterio(self.filepath_NO2, self.filename_NO2, 0, self.mean_NO2)
                meta = self.tif_meta(self.filepath_NO2, self.filename_NO2)
                print("1")
            else:
                sum_raastr=self.calc_reastr_end_rasterio(self.filepath_NO2, self.filename_NO2, 0, self.mean_NO2)
                meta = self.tif_meta(self.filepath_NO2, self.filename_NO2)
                print("0")
        if len(self.filename_SO2)>0:
            if len(sum_raastr)>0:
                sum_raastr+=self.calc_reastr_end_rasterio(self.filepath_SO2, self.filename_SO2, 1, self.mean_SO2)
                meta = self.tif_meta(self.filepath_SO2, self.filename_SO2)
                print("2")
            else:
                sum_raastr=self.calc_reastr_end_rasterio(self.filepath_SO2, self.filename_SO2, 1, self.mean_SO2)
                meta = self.tif_meta(self.filepath_SO2, self.filename_SO2)
                print("3")
        if len(self.filename_HCHO)>0:
            if len(sum_raastr)>0:
                sum_raastr+=self.calc_reastr_end_rasterio(self.filepath_HCHO, self.filename_HCHO, 2, self.mean_HCHO)
                meta = self.tif_meta(self.filepath_HCHO, self.filename_HCHO)
                print("4")
            else:
                sum_raastr=self.calc_reastr_end_rasterio(self.filepath_HCHO, self.filename_HCHO, 2, self.mean_HCHO)
                meta = self.tif_meta(self.filepath_HCHO, self.filename_HCHO)
                print("5")
        if len(self.filename_CO)>0:
            if len(sum_raastr)>0:
                sum_raastr+=self.calc_reastr_end_rasterio(self.filepath_CO, self.filename_CO, 3, self.mean_CO)
                meta = self.tif_meta(self.filepath_CO, self.filename_CO)
                print("6")
            else:
                sum_raastr=self.calc_reastr_end_rasterio(self.filepath_CO, self.filename_CO, 3, self.mean_CO)
                meta = self.tif_meta(self.filepath_CO, self.filename_CO)
                print("7")
        if len(self.filename_CH4)>0:
            if len(sum_raastr)>0:
                sum_raastr+=self.calc_reastr_end_rasterio(self.filepath_CH4, self.filename_CH4, 4, self.mean_CH4)
                meta = self.tif_meta(self.filepath_CH4, self.filename_CH4)
                print("8")
            else:
                sum_raastr=self.calc_reastr_end_rasterio(self.filepath_CH4, self.filename_CH4, 4, self.mean_CH4)
                meta = self.tif_meta(self.filepath_CH4, self.filename_CH4)
                print("9")
        if len(self.filename_O3)>0:
            if len(sum_raastr)>0:
                sum_raastr+=self.calc_reastr_end_rasterio(self.filepath_O3, self.filename_O3, 5, self.mean_O3)
                meta = self.tif_meta(self.filepath_O3, self.filename_O3)
                print("10")
            else:
                sum_raastr=self.calc_reastr_end_rasterio(self.filepath_O3, self.filename_O3, 5, self.mean_O3)
                meta = self.tif_meta(self.filepath_O3, self.filename_O3)
                print("11")
        self.meta=meta
        meta.update({"driver": "GTiff",
                     "height": sum_raastr.shape[1],
                     "width": sum_raastr.shape[2]
                        }
                        )
        with rasterio.open(str(self.ini['DEFAULT']['pathtoprogram'])+"/output.tif", 'w', **meta) as dst:
            dst.write(sum_raastr)
    
    def tif_meta(self,full_file_paths,full_file_names):
        tmp_tif_0=rasterio.open(full_file_paths[0]+"\\"+full_file_names[0])
        out_meta = tmp_tif_0.meta.copy()
        return out_meta
        
    def calc_reastr_end_rasterio(self,full_file_paths,full_file_names,k,mean):
        tmp_tif_0=rasterio.open(full_file_paths[0]+"\\"+full_file_names[0]).read()
        sum_rastr = (tmp_tif_0/mean[0][1])**self.danger_const[k]
        for r in range(1, len(full_file_names)):
            tmp_tif = rasterio.open(full_file_paths[r]+"\\"+full_file_names[r]).read()
            sum_rastr += (tmp_tif/mean[r][1])**self.danger_const[k]
            print(str(tmp_tif),str(mean[r][1]),str(self.danger_const[k]))
        return sum_rastr
    
    """def calc_one_rastr(self,full_file_paths,full_file_names,k):
        df_orders=[]
        for i in range(len(full_file_names)):
            try:
                expression = f"A**{self.danger_const[k]}"
                expression = f"A"
                output_raster = str(self.ini['DEFAULT']['pathtoprogram'])+"//output_pow2.tif"
                #expression = "(A/"+str(self.mean_NO2[i][1])+")^"+str(self.danger_const[k])
                params = {'INPUT_A': full_file_paths[i]+"\\"+full_file_names[i],
                 'BAND_A':1,
                 'FORMULA': expression,
                 'OUTPUT': output_raster,
                 'NO_DATA': None,
                 'RTYPE': 6 
                }
                Processing.initialize()
                processing.run("gdal:rastercalculator", params)
            except Exception as e:
                print(e)
                with open(str(self.ini['DEFAULT']['pathtoprogram'])+"//log.txt", 'a') as file:
                    file.writelines(str(e)) 
        return df_orders  """
    
    def tab_f_init_ui(self):
        self.f_tab.h = ttk.Scrollbar(self.f_tab,orient=tk.HORIZONTAL)
        self.f_tab.v = ttk.Scrollbar(self.f_tab,orient=tk.VERTICAL)
        self.f_tab.h.place(relheight=0.1, relwidth=0.98, relx=0, rely=0.765)
        self.f_tab.v.place(relheight=0.8, relwidth=0.1, relx=0.94, rely=0)
        self.f_tab.btncont=ttk.Button(self.f_tab, text="Продолжить",style='secondary.TButton', command = self.def_continue_result)
        self.f_tab.btncont.place(relheight=0.11, relwidth=0.2, relx=0.5, rely=0.87)
    
    def tab_f_visualise(self):
        self.f_tab.canv_frame = ttk.Frame(self.f_tab)
        self.f_tab.canv_frame.place(relheight=0.8, relwidth=0.985, relx=0, rely=0)
        options_list = [
                        '-ot Byte',
                        '-of PNG',
                        '-b 1',
                        '-scale'
                        ]  
        options_string = " ".join(options_list)
        gdal.Translate(
                        self.dir_path+"/output.png",
                        str(self.ini['DEFAULT']['pathtoprogram'])+"/output.tif",
                        options=options_string
                        )
        self.f_tab.Image=Image.open(self.dir_path+"/output.png")
        self.f_tab.photo = ImageTk.PhotoImage(self.f_tab.Image)
        self.f_tab.Image=self.f_tab.Image.resize((self.f_tab.photo.width()*3,self.f_tab.photo.height()*3),Image.LANCZOS)
        self.f_tab.photo = ImageTk.PhotoImage(self.f_tab.Image)
        os.remove(self.dir_path+"/output.png")
        try:
            os.remove(self.dir_path+"/output.png.aux.xml")
        except:
            pass
        self.f_tab.canvas = tk.Canvas(self.f_tab.canv_frame,scrollregion=(0, 0, self.f_tab.photo.width(), self.f_tab.photo.height()), bg="white", yscrollcommand=self.e_tab.v.set, xscrollcommand=self.e_tab.h.set)
        self.f_tab.h["command"] = self.f_tab.canvas.xview
        self.f_tab.v["command"] = self.f_tab.canvas.yview
        self.f_tab.canvas.place(relheight=1, relwidth=1, relx=0, rely=0)
        self.f_tab.canvas.create_image(0, 0, anchor=tk.NW, image=self.f_tab.photo)
     
    def def_continue_result(self):
        self.f_tab.canv_frame.destroy()
        self.ch_w(2)
        self.ch_w(1)
        self.ch_w(0)
        self.hide_w(3)   
        self.hide_w(4)
        self.hide_w(5) 
    
    
    def event_exit(self,event):
        try:
            index = self.notebook.index(f'@{event.x},{event.y}')
            if index==6:
                result=askyesno(title="Выход?", message="Вы уверены, что хотите выйти?")
                if result:
                    self.clese_window()
                else:
                    self.ch_w(0)
        except:
            pass
                
    @thread
    def ch_w(self,window):
        self.notebook.select(window)
        
    def hide_w(self,window):
        self.notebook.hide(window)
        
    def clese_window(self):
        self.window.destroy()
    
if __name__ == '__main__':
    program = MainInterface()
    del program