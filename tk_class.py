# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:16:55 2026

@author: Intel Core I9
"""
import tkinter as tk
from functools import partial
import ttkbootstrap as ttk
from tkinter import filedialog

from ini_modules import ini_programm
from translations import languages_struct
from tk_mainframe import tk_mainframe
from tk_loadframe import tk_loadframe
from tk_waitframe import tk_waitframe
from tk_loadframe_shape import tk_loadframe_shape
from tk_show_mean import tk_show_mean
from tk_air_pollution_select_to_work import tk_air_pollution_select_to_work
from tk_waitframe_air_poll_last import tk_waitframe_air_poll_last
from tk_air_poll_visualise import tk_air_poll_visualise

class tk_class(ttk.Window):
    def __init__(self,path):
        super().__init__()
        self.atm_shape=None
        self.atm_means_rastrs=None
        self.atm_sum_rastrs=None
        self.dir_path=path
        
        self.danger_const={"NOmainbutton" : 1.3, "SO2mainbutton" : 1, "HCHOmainbutton" : 1.7, "COmainbutton" : 1.3, "CH4mainbutton" : 0.9, "O3mainbutton" : 0.9}
        self.ini=ini_programm(self.dir_path,'QGISPYINBUM_settings')
        self.Atm_State=tk.IntVar(value="active")
        self.debugger = tk.IntVar(value=int(self.ini.settings_get('debugger')))
        self.translations_dict=languages_struct(self.dir_path,'QGISPYINBUM_languages')
        self.translations=self.translations_dict.translations
        self.language=self.ini.settings_get('language')
        self.tk_configure()
        self.theme_use(self.ini.settings_get('theme'))
        
        self.load_frames={}
        self.load_frames_names={}
        self.worked_frames={}
        
        self.transtatedict={}
        for i in self.translations[self.language].keys():
            self.transtatedict[i]=tk.StringVar(value=self.translations[self.language][i])
        
        self.main_menu_add()
        self.style_configure()
        
        self.main_frame_create()
        self.load_frames_create()
        self.bind("<Configure>", self.canvas_configure)

    def canvas_configure(self,event):
        self.style_configure()

    def style_configure(self):
        self.style.configure('.', font=('arial', round(self.winfo_height()/77)))
        
        self.style.configure('my.TButton', background='white', foreground="black", anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('purple.TButton', background='#800080',
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('purple.TLabel', background='#800080', foreground="white", anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('SlateGray.TButton', background='#708090', anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('DeepPink.TButton', background='#FF1493', anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('LimeGreen.TButton', background='#32CD32', anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('LimeGreen.TLabel', background='#32CD32', foreground="white", anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('DodgerBlue.TButton', background='#1E90FF', anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('Gold.TButton', background='#FFD700', foreground="black", anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('Tomato.TButton', background='#FF6347', anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.configure('Sienna.TButton', background='#A0522D', anchor="center",
                             font=('arial',round(self.winfo_height()/77)),justify=tk.CENTER)
        self.style.map("Treeview",rowheight=[("!disabled",round(self.winfo_height()/77*2.5))])
        """try:
            for i in self.load_frames_names:
                self.load_frames[i].data_table.autofit_columns()
        except:
            pass"""
    def main_menu_add(self):
        self.resize_menu_create()
        self.theme_menu_create()
        self.lang_menu_create()
        self.debug_menu_create()
        self.main_menu = tk.Menu()
        self.main_menu.add_cascade(label=self.translations[self.language]["language"], menu = self.lang_menu)
        self.main_menu.add_cascade(label=self.translations[self.language]["theme"], menu = self.theme_menu)
        self.main_menu.add_cascade(label=self.translations[self.language]["windsize"], menu = self.size_menu)
        self.main_menu.add_cascade(label=self.translations[self.language]["fullscreen"], command=self.toggle_maximize)
        self.main_menu.add_cascade(label=self.translations[self.language]["savepath"], command=self.path_save_set)
        self.main_menu.add_cascade(label="debugger", menu=self.debug_menu)
        self.main_menu.add_cascade(label="exit", command=self.destroy)
        #self.main_menu.add_checkbutton(label="debugger on/off", onvalue=1, offvalue=0, variable=self.debugger, command=self.debugger_change)
        self.config(menu=self.main_menu)
    def path_save_set(self):
        directory=filedialog.askdirectory()
        if directory:
            self.ini.settings_set(directory,'pathtosave')
    def toggle_maximize(self,*args):
        if self.attributes('-fullscreen') == True:
            self.attributes('-fullscreen', False)
            self.ini.settings_set(0,'fullscreen')
        else:
            self.attributes('-fullscreen', True)
            self.ini.settings_set(1,'fullscreen')
    def theme_use(self,i):
        self.style.theme_use(i)
        self.ini.settings_set(i,'theme')
        self.style_configure()
    def language_set(self,lang):
        old_lang=self.language
        self.language=lang
        self.ini.settings_set(lang,'language')
        self.main_menu.entryconfigure(self.translations[old_lang]["language"],
             label=self.translations[self.language]["language"])
        self.main_menu.entryconfigure(self.translations[old_lang]["theme"],
             label=self.translations[self.language]["theme"])
        self.main_menu.entryconfigure(self.translations[old_lang]["windsize"],
             label=self.translations[self.language]["windsize"])       
        self.main_menu.entryconfigure(self.translations[old_lang]["fullscreen"],
             label=self.translations[self.language]["fullscreen"]) 
        self.main_menu.entryconfigure(self.translations[old_lang]["savepath"],
             label=self.translations[self.language]["savepath"]) 
                               
        for i in self.translations[self.language].keys():
            self.transtatedict[i].set(self.translations[self.language][i])  
        try:                                
            self.main_frame.lang_change()
        except:
            pass                           
    def lang_menu_create(self):
        self.lang_menu = tk.Menu()
        for i in self.translations.keys():
            self.lang_menu.add_command(label=i,
                 command = partial(self.language_set,i))
    def debugger_change(self):
        self.ini.settings_set(str(self.debugger.get()),'debugger')
        
    def debug_menu_create(self):
        self.debug_menu = tk.Menu()
        self.debug_menu.add_checkbutton(label="debugger on/off", onvalue=1, offvalue=0, variable=self.debugger, command=self.debugger_change)

    def theme_menu_create(self):
        self.theme_menu = tk.Menu()
        for i in self.style.theme_names():
            self.theme_menu.add_command(label=i,
                 command = partial(self.theme_use,i))
    def resize_menu_start(self,size):
        self.geometry(size)
        self.ini.settings_set(size,'screensize')
        self.toggle_maximize
    def resize_menu_create(self):
        self.size_menu = tk.Menu()
        self.size_menu.add_command(label="1400x720",
                                   command= partial(self.resize_menu_start,"1400x720"))
        self.size_menu.add_command(label="1280x720",
                                   command= partial(self.resize_menu_start,"1280x720"))
        self.size_menu.add_command(label="1600x900",
                                   command= partial(self.resize_menu_start,"1600x900"))
        self.size_menu.add_command(label="1920x1080",
                                   command= partial(self.resize_menu_start,"1920x1080"))
        self.size_menu.add_command(label="2048x1152",
                                   command= partial(self.resize_menu_start,"2048x1152"))
        self.size_menu.add_command(label="2560x1440",
                                   command= partial(self.resize_menu_start,"2560x1440"))
        self.size_menu.add_command(label="1024x768",
                                   command= partial(self.resize_menu_start,"1024x768"))
    def tk_configure(self):
        self.title('QGISPY-INBUM')
        self.geometry(self.ini.settings_get('screensize')+"+10+10")
        self.minsize(1200,600)
        self.resizable(True, True)
        self.attributes('-fullscreen',self.ini.settings_get('fullscreen'))
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        #self.state('zoomed')
        #self.attributes('-topmost', True)
        self.update_idletasks()
    def on_closing(self):
        self.destroy()
    #Здесь создадим главное окно
    def main_frame_create(self):
        #self.main_frame = ttk.Frame(self)
        self.main_frame = tk_mainframe(self)
        self.main_frame.pack(fill='both', expand=True)
        self.main_frame.bind("<Enter>",self.update_start_buttons)
    def update_start_buttons(self,event):
        try:
            countshape=0
            countrastr=0
            for i in self.load_frames_names:
                if i!="all6mainbutton":
                    if self.load_frames[i].shape_rastr_load_check()==True:
                        countrastr+=1
                else:
                    if self.load_frames[i].shape_rastr_load_check()==True:
                        countshape+=1
            if countshape==1 and countrastr>0:
                self.main_frame.btn["all6startmainbutton"].config(state=["active"])                
            else:
                self.main_frame.btn["all6startmainbutton"].config(state=["disabled"])
        except:
            pass
    def change_frame(self,old_frame,new_frame):
        old_frame.pack_forget()
        new_frame.pack(fill='both', expand=True)
    def atmospheric_calc_start(self,frame):
        self.change_frame(frame,self.worked_frames["all6startmainbutton"])
    def load_frames_create(self):
        self.load_frames_names=[
            "O3mainbutton",
            "SO2mainbutton",
            "CH4mainbutton",
            "COmainbutton",
            "HCHOmainbutton",
            "NOmainbutton",
            "all6mainbutton",
            ]
        
        
        for i in self.load_frames_names:
            if i!="all6mainbutton":
                self.load_frames[i]= tk_loadframe(self, i)
            else:
                self.load_frames[i]= tk_loadframe_shape(self, i)
            self.main_frame.btn[i].configure(command=partial(self.change_frame,self.main_frame,self.load_frames[i]))
        
        for i in self.load_frames_names:
            for j in self.load_frames_names:
                self.load_frames[i].change_frames_buttons[j].config(command=partial(self.change_frame,self.load_frames[i],self.load_frames[j]))
        self.worked_frames["all6startmainbutton"]=tk_waitframe(self)   
        self.show_mean_frame=tk_show_mean(self)
        self.tk_air_pollution_select_to_work_frame=tk_air_pollution_select_to_work(self)
        self.tk_waitframe_air_poll_last=tk_waitframe_air_poll_last(self)
        self.tk_air_poll_visualise=tk_air_poll_visualise(self)
        self.main_frame.btn["all6startmainbutton"].configure(command=partial(self.atmospheric_calc_start,self.main_frame))
        
    def atm_shape_set(self,shape):
        self.atm_shape=shape     
        
    def atm_means_rastrs_set(self,rastrs):    
        self.atm_means_rastrs=rastrs
        
    def atm_sum_rastrs_set(self,rastrs):    
        self.atm_sum_rastrs=rastrs
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        