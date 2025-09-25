# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 12:04:42 2025

@author: Intel Core I9
"""
import tkinter as tk    
from tkinter import Tk, ttk, font, filedialog
import os
import threading
import PIL
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno
import tkinter as tk
#import xlsxwriter
#import openpyxl
import time
from inimodule import *
from tab_a import TabA as TabA
from tab_b import TabB as TabB
from tab_c import TabC as TabC
from tab_d import TabD as TabD

def thread(fn):
    def execute(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return execute

path=os.path.dirname(os.path.abspath(__file__))
#print(path)

class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.dir_path=path
        self.ini = read_ini(path,'QGISPYITPS', self.dir_path)
        self.First_Settings()
        self.window.update_idletasks()
        self.create_widgets()
        self.work=1
        self.update()
        
    @thread
    def update(self):
        while self.work==1 and self.window:
            time.sleep(1)
            try:
                self.__on_update()
                self.notebook.style.theme_use(self.b_tab.selected_theme.get())
            except:
                pass
            try:
                if self.a_tab.start_command == 1:
                    self.a_tab.start_command = 0
                    self.ch_w(3)
                    self.hide_w(2)
                    self.hide_w(1)
                    self.hide_w(0)
                    self.copy_workfiles()
                    self.d_tab.global_calc_mean()
                    #print("hello")
                if self.d_tab.exit_command == 1:
                    self.d_tab.exit_command = 0
                    self.ch_w(2)
                    self.ch_w(1)
                    self.ch_w(0)
                    self.hide_w(3)
            except:
                pass
            try:
                self.d_tab.inipath=self.b_tab.ini['DEFAULT']['pathtoprogram']
            except:
                pass
    
    def __on_update(self):
        if self.b_tab.fullscreen_enabled.get() == 1:
            self.window.attributes("-fullscreen", True)
        else:
            self.window.attributes("-fullscreen", False)
    def copy_workfiles(self):
        self.d_tab.filepath_NO2=self.a_tab.filepath_NO2
        self.d_tab.filename_NO2=self.a_tab.filename_NO2
        self.d_tab.filepath_SO2=self.a_tab.filepath_SO2
        self.d_tab.filename_SO2=self.a_tab.filename_SO2
        self.d_tab.filepath_O3=self.a_tab.filepath_O3
        self.d_tab.filename_O3=self.a_tab.filename_O3
        self.d_tab.filepath_HCHO=self.a_tab.filepath_HCHO
        self.d_tab.filename_HCHO=self.a_tab.filename_HCHO
        self.d_tab.filepath_CO=self.a_tab.filepath_CO
        self.d_tab.filename_CO=self.a_tab.filename_CO
        self.d_tab.filepath_CH4=self.a_tab.filepath_CH4
        self.d_tab.filename_CH4=self.a_tab.filename_CH4
        self.d_tab.filename_Rstr=self.a_tab.filename_Rstr
        self.d_tab.filepath_Rstr=self.a_tab.filepath_Rstr
        #new_font = ("", round(self.window.winfo_height()/50), "bold")
        #self.change_font_recursive(self.window, new_font)
            
    def First_Settings(self):
        self.window.title('QGISPY-ITPS')
        self.window.geometry("1400x720+400+200")
        self.window.bind('<Destroy>', self.close_window)
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
        #print(self.notebook.style.theme_names())
        self.notebook.style.theme_use(self.ini['DEFAULT']['theme'])
        self.a_tab = TabA(self.notebook,self.dir_path)
        self.b_tab = TabB(self.notebook,self.dir_path)
        self.c_tab = TabC(self.notebook)
        self.d_tab = TabD(self.notebook,self.dir_path)
        
        self.notebook.add(self.a_tab, text="Главная Страница")
        self.notebook.add(self.b_tab, text="Параметры")
        self.notebook.add(self.c_tab, text="Справка")
        self.notebook.add(self.d_tab, text="Расчет")
        
        self.Exfr = ttk.Frame(self.notebook)
        self.notebook.add(self.Exfr, text="Выйти")
        
        self.notebook.pack(expand=True, fill=tk.BOTH)
        #self.notebook.bind("<Button-3>", self.event_handler)
        self.notebook.bind("<Button-1>", self.event_exit)
        self.hide_w(3)
        
    def event_exit(self,event):
        index = self.notebook.index(f'@{event.x},{event.y}')
        #print(event)
        """if index == 3:
            self.d_tab.credits.configure(state=tk.NORMAL)
            self.d_tab.credits.delete("0.0", tk.END)
            self.d_tab.credits.insert(tk.END,str(self.a_tab.filename_NO2))
            self.d_tab.credits.configure(state=tk.DISABLED)"""
        if index==4:
            result=askyesno(title="Выход?", message="Вы уверены, что хотите выйти?")
            if result:
                self.clese_window()
            else:
                self.ch_w(0)
                
    @thread
    def ch_w(self,window):
        self.notebook.select(window)
    def hide_w(self,window):
        self.notebook.hide(window)
    def clese_window(self):
        #QgsApplication.exitQgis()
        self.work=0
        self.window.destroy()
        self.window.quit()
    def close_window(self, event):
        #QgsApplication.exitQgis()
        self.work=0
        self.window.destroy()
        self.window.quit()
    def super_full_update(self,change_var):
        self.window.attributes("-fullscreen", change_var)
        self.update_idletasks()
    """def event_handler(self,event):
        if self.notebook.identify(event.x, event.y) == 'label':
            index = self.notebook.index(f'@{event.x},{event.y}')
            print(self.notebook.tab(index, 'text'))   # имя вкладки, например, Some
            print(index)"""
    
if __name__ == '__main__':
    program = MainInterface()
    program.window.mainloop()
    del program