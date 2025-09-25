# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 11:55:11 2025

@author: Intel Core I9
"""

import tkinter as tk
from tkinter import Tk, ttk, font
import pandas as pd
import sys
import os
import processing
from processing.core.Processing import Processing
#import xlsxwriter
#import openpyxl
from inimodule import *

class TabD(ttk.Frame):
    def __init__(self, parent, dir_path):
        super().__init__(parent)
        self.dir_path=dir_path
        self.parent = parent
        self.text=[]
        self.inipath = ""
        self.init_ui()
        self.filepath_NO2=[]; self.filename_NO2=[]; self.mean_NO2=[]
        self.filepath_SO2=[]; self.filename_SO2=[]; self.mean_SO2=[]
        self.filepath_O3=[]; self.filename_O3=[]; self.mean_O3=[]
        self.filepath_HCHO=[]; self.filename_HCHO=[]; self.mean_HCHO=[]
        self.filepath_CO=[]; self.filename_CO=[]; self.mean_CO=[]
        self.filepath_CH4=[]; self.filename_CH4=[]; self.mean_CH4=[]
        self.filename_Rstr=[]; self.filepath_Rstr=[]
        self.exit_command=0
        
    def init_ui(self):
        self.credits = tk.Text(self)
        self.credits.place(relheight=0.25, relwidth=0.95, relx=0, rely=0)
        self.ys = ttk.Scrollbar(self,orient = "vertical", command = self.credits.yview)
        self.ys.place(relheight=0.25, relwidth=0.05, relx=0.95, rely=0)
        self.xs = ttk.Scrollbar(self,orient = "horizontal", command = self.credits.xview)
        self.xs.place(relheight=0.05, relwidth=0.95, relx=0, rely=0.95)
        self.credits["yscrollcommand"] = self.ys.set
        self.credits["xscrollcommand"] = self.xs.set
        self.credits.insert("1.0", str(self.text))
        self.credits.configure(state=tk.DISABLED)
        self.pack(expand=True, fill=tk.BOTH)
        self.cred_ins("""\n\n\n          ПОДОЖДИТЕ\n          ИДЕТ ОБРАБОТКА\n\n\n""")
        self.btnret=ttk.Button(self, text="Назад",style='secondary.TButton', command = self.def_return)
        self.btnret.place(relheight=0.2, relwidth=0.5, relx=0.3, rely=0.27)
        
        
    def def_return(self):
        self.exit_command=1
        
    def cred_ins(self,text):
        self.credits.configure(state=tk.NORMAL)
        self.credits.delete("0.0", tk.END)
        self.credits.insert(tk.END,text)
        self.credits.configure(state=tk.DISABLED)
    def global_calc_mean(self):
        self.btnret["text"]="Назад"
        self.cred_ins("""\n\n\n          ПОДОЖДИТЕ\n          ИДЕТ ОБРАБОТКА\n\n\n""")
        #print(str(self.filename_NO2))
        #folder_path = 'C:\\Users\\Intel Core I9\\Downloads\\data for Sasha'
        """file_names = []
        full_file_names = []
        for file_name in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, file_name)):
                if file_name.endswith(".tif"):
                    file_names.append(file_name)
                    full_file_names.append(folder_path+"\\"+file_name)
        print(file_names)"""
        if len(self.filename_NO2)>0:
            self.mean_NO2=self.calc_mean(self.filepath_NO2, self.filename_NO2)
            #print("000")
        if len(self.filename_SO2)>0:
            self.mean_SO2=self.calc_mean(self.filepath_SO2, self.filename_SO2)
            #print("000")
        if len(self.filename_HCHO)>0:
            self.mean_HCHO=self.calc_mean(self.filepath_HCHO, self.filename_HCHO)
            #print("000")
        if len(self.filename_CO)>0:
            self.mean_CO=self.calc_mean(self.filepath_CO, self.filename_CO)
            #print("000")
        if len(self.filename_CH4)>0:
            self.mean_CH4=self.calc_mean(self.filepath_CH4, self.filename_CH4)
            #print("000")
        if len(self.filename_O3)>0:
            self.mean_O3=self.calc_mean(self.filepath_O3, self.filename_O3)
            #print("000")
        self.save_excel()
        self.btnret["text"]="Готово"
        
    def save_excel(self):
        new_list=[]
        #print("001")
        if len(self.filename_NO2)>0:
            for i in range(len(self.filename_NO2)):
                #print(i)
                new_list.append([self.filename_NO2[i],float(self.mean_NO2[i].iloc[0])])
        if len(self.filename_SO2)>0:
            for i in range(len(self.filename_SO2)):
                new_list.append([self.filename_SO2[i],float(self.mean_SO2[i].iloc[0])])
        if len(self.filename_HCHO)>0:
            for i in range(len(self.filename_HCHO)):
                new_list.append([self.filename_HCHO[i],float(self.mean_HCHO[i].iloc[0])])
        if len(self.filename_CO)>0:
            for i in range(len(self.filename_CO)):
                new_list.append([self.filename_CO[i],float(self.mean_CO[i].iloc[0])])
        if len(self.filename_CH4)>0:   
            for i in range(len(self.filename_CH4)):
                new_list.append([self.filename_CH4[i],float(self.mean_CH4[i].iloc[0])])
        if len(self.filename_O3)>0:
            for i in range(len(self.filename_O3)):
                new_list.append([self.filename_O3[i],float(self.mean_O3[i].iloc[0])])
        self.cred_ins(str(new_list).replace("]","\n").replace("[","").replace(",",""))
        #print("003")
        
        #print(str(self.inipath))
        pd.DataFrame(new_list).to_excel(str(self.inipath)+"//output.xlsx")
        
        """workbook = xlsxwriter.Workbook(str(self.inipath)+'//output.xlsx')
        worksheet = workbook.add_worksheet()
        for row_num, data in enumerate(new_list):
            #print(str(row_num), str(data))
            worksheet.write_row(row_num, 0, data)"""
        #workbook.close()
        #print("004")
        return True
        
        
        """with xlsxwriter.Workbook(str(self.inipath)+'//output.xlsx') as workbook:
            print("005")
            worksheet = workbook.add_worksheet()
            print("006")
            for row_num, data in enumerate(new_list):
                print(str(row_num), str(data))
                worksheet.write_row(row_num, 0, data)"""
        """df = pd.DataFrame(new_list)
        print("004")
        writer = pd.ExcelWriter(self.dir_path+"\\"+'test.xlsx', engine='xlsxwriter')
        print("005")
        df.to_excel(writer, sheet_name='welcome', index=False)
        print("006")
        writer.save()"""
    def calc_mean(self,full_file_paths,full_file_names):
        df_orders=[]
        for i in range(len(full_file_names)):
            #print("00")
            Processing.initialize()
            #print("01")
            processing.run("native:zonalstatisticsfb", 
                           {'INPUT': self.filepath_Rstr[0]+"\\"+self.filename_Rstr[0],
                            'INPUT_RASTER': full_file_paths[i]+"\\"+full_file_names[i],
                            'RASTER_BAND':1,
                            'COLUMN_PREFIX':'_',
                            'STATISTICS':[2],
                            'OUTPUT':self.dir_path+"\\calc_"+full_file_names[i].replace(".tif",".xlsx")})
            #print("02")
            df_orders.append(pd.read_excel(self.dir_path+"\\calc_"+full_file_names[i].replace(".tif",".xlsx"), usecols=[0,30], index_col=0))
            #print("03")
            os.remove(self.dir_path+"\\calc_"+full_file_names[i].replace(".tif",".xlsx"))
            #print("04")
            #print(full_file_names[i], df_orders[i].head())
            #print("05")
        return df_orders