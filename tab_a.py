# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 11:54:32 2025

@author: Intel Core I9
"""
import tkinter as tk    
from tkinter import Tk, ttk, font, filedialog
import os
import threading
from PIL import Image, ImageTk
from inimodule import *

def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute

class TabA(ttk.Frame):
    """Главное окно"""
    def __init__(self, parent,dir_path):
        """Инициализация"""
        super().__init__(parent)
        self.parent = parent
        """Данные о файлах для подгрузки"""
        self.start_command=0
        self.selected=-1
        self.dir_path=dir_path
        self.Image=Image.open(self.dir_path+"\\pngegg.png").resize((20,20),Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.Image)
        self.filepath_NO2=[]; self.filename_NO2=[]; self.filepath_SO2=[]
        self.filename_SO2=[]; self.filepath_O3=[]; self.filename_O3=[]
        self.filepath_HCHO=[]; self.filename_HCHO=[]; self.filepath_CO=[]
        self.filename_CO=[]; self.filepath_CH4=[]; self.filename_CH4=[]
        self.filename_Rstr=[]; self.filepath_Rstr=[]
        self.config(style='primary.TButton')
        self.init_ui()
        
    def init_ui(self):
        """Сохдание виджетов""" 
        self.filepath_select = tk.StringVar(value="")
        self.create_Listbox()
        self.Frame_Rastr()
        self.Frame_NO2()
        self.Frame_SO2()
        self.Frame_O3()
        self.Frame_HCHO()
        self.Frame_CO()
        self.Frame_CH4()
        self.btndel=ttk.Button(self, text="Удалить",style='danger.TButton',command=self.delete)
        self.btndel.place(relheight=0.04, relwidth=0.2, relx=0, rely=0.61)
        self.lblpath=ttk.Label(self, textvariable=self.filepath_select,style='secondary.TButton')
        self.lblpath.place(relheight=0.04, relwidth=0.4, relx=0.2, rely=0.61)
        self.btnstart=ttk.Button(self, text="Начать",style='success.TButton',command=self.startbutton)
        self.btnstart.place(relheight=0.1, relwidth=0.4, relx=0.3, rely=0.65)
        
        self.pack(expand=True, fill=tk.BOTH)
    
    def startbutton(self):
        if len(self.filename_Rstr)==0:
            tk.messagebox.showerror("Ошибка", f"Не выбран векторный файл")
        elif len(self.filename_NO2)==0 and len(self.filename_SO2)==0 and len(self.filename_O3)==0 and len(self.filename_HCHO)==0 and len(self.filename_CO)==0 and len(self.filename_CH4)==0:
            tk.messagebox.showerror("Ошибка", f"Не выбран ни одюин растровый файл")
        else:
            self.start_command=1
        
    def create_Listbox(self):
        self.languages_var = tk.StringVar(value=[])
        self.lb = tk.Listbox(self, listvariable=self.languages_var, selectmode=tk.SINGLE)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.lb.yview)
        self.scrollbar.place(relheight=0.6, relwidth=0.01, relx=0.6, rely=0)
        self.lb["yscrollcommand"]=self.scrollbar.set
        self.lb.place(relheight=0.6, relwidth=0.6, relx=0, rely=0)
        self.lb.bind("<<ListboxSelect>>", self.listbox_selected)
    
    def listbox_selected(self, event):
        self.filepath_select
        selection = self.lb.curselection()
        selected_language = self.lb.get(selection[0])
        match self.selected:
            case 0:
                index = self.filename_Rstr.index(selected_language)
                self.filepath_select.set(self.filepath_Rstr[index])
            case 1:
                index = self.filename_NO2.index(selected_language)
                self.filepath_select.set(self.filepath_NO2[index])
            case 2:
                index = self.filename_SO2.index(selected_language)
                self.filepath_select.set(self.filepath_SO2[index])
            case 3:
                index = self.filename_O3.index(selected_language)
                self.filepath_select.set(self.filepath_O3[index])
            case 4:
                index = self.filename_HCHO.index(selected_language)
                self.filepath_select.set(self.filepath_HCHO[index])
            case 5:
                index = self.filename_CO.index(selected_language)
                self.filepath_select.set(self.filepath_CO[index])
            case 6:
                index = self.filename_CH4.index(selected_language)
                self.filepath_select.set(self.filepath_CH4[index])
                
    def Frame_Rastr(self):
        self.Rstr_files = tk.StringVar(value=str(len(self.filename_Rstr)))
        self.RstrLb=ttk.Label(self,text="Shape. Файлов выбрано ",style='secondary.TButton')
        self.RstrLb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0, bordermode=tk.OUTSIDE)
        self.RstrLbNum=ttk.Label(self,textvariable=self.Rstr_files,style='secondary.TButton')
        self.RstrLbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0, bordermode=tk.OUTSIDE)
        self.Rstrbtnf=ttk.Button(self, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(0,1))
        self.Rstrbtnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0, bordermode=tk.OUTSIDE)
        self.btnRstr=ttk.Button(self, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(0,1))
        self.btnRstr.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0, bordermode=tk.OUTSIDE)
        self.btnRstrfind=tk.Button(self, image=self.photo,command=lambda: self.add(0))
        #self.btnRstrfind=tk.Button(self, text="Показать",command=lambda: self.add(0))
        self.btnRstrfind.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0, bordermode=tk.OUTSIDE)

    def Frame_NO2(self):
        self.NO2_files = tk.StringVar(value=str(len(self.filename_NO2)))
        self.NO2Lb=ttk.Label(self,text="NO2. Файлов выбрано ",style='secondary.TButton')
        self.NO2Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.09, bordermode=tk.OUTSIDE)
        self.NO2LbNum=ttk.Label(self,textvariable=self.NO2_files,style='secondary.TButton')
        self.NO2LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.09, bordermode=tk.OUTSIDE)
        self.NO2btnf=ttk.Button(self, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(1,2))
        self.NO2btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.09, bordermode=tk.OUTSIDE)
        self.btnNO2=ttk.Button(self, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(1,2))
        self.btnNO2.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.09, bordermode=tk.OUTSIDE)
        self.btnNO2find=tk.Button(self, image=self.photo,command=lambda: self.add(1))
        #self.btnNO2find=tk.Button(self, text="Показать",command=lambda: self.add(1))
        self.btnNO2find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.09, bordermode=tk.OUTSIDE)
   
    def Frame_SO2(self):
        self.SO2_files = tk.StringVar(value=str(len(self.filename_SO2)))
        self.SO2Lb=ttk.Label(self,text="SO2. Файлов выбрано ",style='secondary.TButton')
        self.SO2Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.18, bordermode=tk.OUTSIDE)
        self.SO2LbNum=ttk.Label(self,textvariable=self.SO2_files,style='secondary.TButton')
        self.SO2LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.18, bordermode=tk.OUTSIDE)
        self.SO2btnf=ttk.Button(self, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(2,2))
        self.SO2btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.18, bordermode=tk.OUTSIDE)
        self.btnSO2=ttk.Button(self, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(2,2))
        self.btnSO2.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.18, bordermode=tk.OUTSIDE)
        self.btnSO2find=tk.Button(self, image=self.photo,command=lambda: self.add(2))
        #self.btnSO2find=tk.Button(self, text="Показать",command=lambda: self.add(2))
        self.btnSO2find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.18, bordermode=tk.OUTSIDE)
           
    def Frame_O3(self):
        self.O3_files = tk.StringVar(value=str(len(self.filename_O3)))
        self.O3Lb=ttk.Label(self,text="O3. Файлов выбрано ",style='secondary.TButton')
        self.O3Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.27, bordermode=tk.OUTSIDE)
        self.O3LbNum=ttk.Label(self,textvariable=self.O3_files,style='secondary.TButton')
        self.O3LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.27, bordermode=tk.OUTSIDE)
        self.O3btnf=ttk.Button(self, text="Выбрать файлы",style='secondary.TButton',command=lambda: self.openFile(3,2))
        self.O3btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.27, bordermode=tk.OUTSIDE)
        self.btnO3=ttk.Button(self, text="Выбрать папку",style='secondary.TButton',command=lambda: self.openDir(3,2))
        self.btnO3.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.27, bordermode=tk.OUTSIDE)
        self.btnO3find=tk.Button(self, image=self.photo,command=lambda: self.add(3))
        #self.btnO3find=tk.Button(self, text="Показать",command=lambda: self.add(3))
        self.btnO3find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.27, bordermode=tk.OUTSIDE)
   
    def Frame_HCHO(self):
        self.HCHO_files = tk.StringVar(value=str(len(self.filename_HCHO)))
        self.HCHOLb=ttk.Label(self,style='secondary.TButton',text="HCHO. Файлов выбрано ")
        self.HCHOLb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.36, bordermode=tk.OUTSIDE)
        self.HCHOLbNum=ttk.Label(self,textvariable=self.HCHO_files,style='secondary.TButton')
        self.HCHOLbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.36, bordermode=tk.OUTSIDE)
        self.HCHObtnf=ttk.Button(self,style='secondary.TButton', text="Выбрать файлы",command=lambda: self.openFile(4,2))
        self.HCHObtnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.36, bordermode=tk.OUTSIDE)
        self.btnHCHO=ttk.Button(self,style='secondary.TButton', text="Выбрать папку",command=lambda: self.openDir(4,2))
        self.btnHCHO.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.36, bordermode=tk.OUTSIDE)
        self.btnHCHOfind=tk.Button(self, image=self.photo,command=lambda: self.add(4))
        #self.btnHCHOfind=tk.Button(self, text="Показать",command=lambda: self.add(4))
        self.btnHCHOfind.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.36, bordermode=tk.OUTSIDE)
   
    def Frame_CO(self):
        self.CO_files = tk.StringVar(value=str(len(self.filename_CO)))
        self.COLb=ttk.Label(self,style='secondary.TButton',text="CO. Файлов выбрано ")
        self.COLb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.45, bordermode=tk.OUTSIDE)
        self.COLbNum=ttk.Label(self,textvariable=self.CO_files,style='secondary.TButton')
        self.COLbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.45, bordermode=tk.OUTSIDE)
        self.CObtnf=ttk.Button(self,style='secondary.TButton', text="Выбрать файлы",command=lambda: self.openFile(5,2))
        self.CObtnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.45, bordermode=tk.OUTSIDE)
        self.btnCO=ttk.Button(self,style='secondary.TButton', text="Выбрать папку",command=lambda: self.openDir(5,2))
        self.btnCO.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.45, bordermode=tk.OUTSIDE)
        self.btnCOfind=tk.Button(self, image=self.photo,command=lambda: self.add(5))
        #self.btnCOfind=tk.Button(self, text="Показать",command=lambda: self.add(5))
        self.btnCOfind.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.45, bordermode=tk.OUTSIDE)
  
    def Frame_CH4(self):
        self.CH4_files = tk.StringVar(value=str(len(self.filename_CH4)))
        self.CH4Lb=ttk.Label(self,style='secondary.TButton',text="CH4. Файлов выбрано ")
        self.CH4Lb.place(relheight=0.08, relwidth=0.17, relx=0.62, rely=0.54, bordermode=tk.OUTSIDE)
        self.CH4LbNum=ttk.Label(self,textvariable=self.CH4_files,style='secondary.TButton')
        self.CH4LbNum.place(relheight=0.08, relwidth=0.05, relx=0.77, rely=0.54, bordermode=tk.OUTSIDE)
        self.CH4btnf=ttk.Button(self,style='secondary.TButton', text="Выбрать файлы",command=lambda: self.openFile(6,2))
        self.CH4btnf.place(relheight=0.08, relwidth=0.08, relx=0.81, rely=0.54, bordermode=tk.OUTSIDE)
        self.btnCH4=ttk.Button(self,style='secondary.TButton', text="Выбрать папку",command=lambda: self.openDir(6,2))
        self.btnCH4.place(relheight=0.08, relwidth=0.08, relx=0.89, rely=0.54, bordermode=tk.OUTSIDE)
        self.btnCH4find=tk.Button(self, image=self.photo,command=lambda: self.add(6))
        #self.btnCH4find=tk.Button(self, text="Показать",command=lambda: self.add(6))
        self.btnCH4find.place(relheight=0.08, relwidth=0.03, relx=0.97, rely=0.54, bordermode=tk.OUTSIDE)
    
    def update_files(self):
        self.Rstr_files.set(str(len(self.filename_Rstr)))
        self.NO2_files.set(str(len(self.filename_NO2)))
        self.SO2_files.set(str(len(self.filename_SO2)))
        self.O3_files.set(str(len(self.filename_O3)))
        self.HCHO_files.set(str(len(self.filename_HCHO)))
        self.CO_files.set(str(len(self.filename_CO)))
        self.CH4_files.set(str(len(self.filename_CH4)))
    
    def delete(self):
        try:
            selection = self.lb.curselection()
            selected_language = self.lb.get(selection[0])
        except:
            return
        self.lb.delete(selection[0])
        match self.selected:
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
        self.lb.delete(0,tk.END)
        match n:
            case 0:
                self.selected=0
                if len(self.filename_Rstr)>0:
                    for i in self.filename_Rstr:
                        self.lb.insert(tk.END, i)
            case 1:
                self.selected=1
                if len(self.filename_NO2)>0:
                    for i in self.filename_NO2:
                        self.lb.insert(tk.END, i)
            case 2:
                self.selected=2
                if len(self.filename_SO2)>0:
                    for i in self.filename_SO2:
                        self.lb.insert(tk.END, i)
            case 3:
                self.selected=3
                if len(self.filename_O3)>0:
                    for i in self.filename_O3:
                        self.lb.insert(tk.END, i)
            case 4:
                self.selected=4
                if len(self.filename_HCHO)>0:
                    for i in self.filename_HCHO:
                        self.lb.insert(tk.END, i)
            case 5:
                self.selected=5
                if len(self.filename_CO)>0:
                    for i in self.filename_CO:
                        self.lb.insert(tk.END, i)
            case 6:
                self.selected=6
                if len(self.filename_CH4)>0:
                    for i in self.filename_CH4:
                        self.lb.insert(tk.END, i)
    
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