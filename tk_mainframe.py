# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:41:32 2026

@author: Intel Core I9
"""

import tkinter as tk
import ttkbootstrap as ttk

from tk_tooltip import ToolTip


class tk_mainframe(ttk.Frame):
    def __init__(self,path):
        super().__init__()
        self.btn={}
        self.btn_tooltips={}
        self.atmospheric_math()

    def atmospheric_math(self):
        #      name style row column rowspan columnspan tooltip
        self.bths=[["O3mainbutton",'my.TButton',0,8,1,1,'requirementsnone'],
              ["SO2mainbutton",'my.TButton',1,8,1,1,'requirementsnone'],
              ["CH4mainbutton",'my.TButton',2,8,1,1,'requirementsnone'],
              ["COmainbutton",'my.TButton',3,8,1,1,'requirementsnone'],
              ["HCHOmainbutton",'my.TButton',4,8,1,1,'requirementsnone'],
              ["NOmainbutton",'my.TButton',5,8,1,1,'requirementsnone'],
              ["all6mainbutton",'my.TButton',6,8,1,1,'requirementsnone'],
              ["all6startmainbutton",'purple.TButton',7,8,1,1,'requirementair'],
              ["landcoverdata",'my.TButton',2,6,1,1,'requirementsnone'],
              ["snowcoverarea", 'DodgerBlue.TButton',0,6,1,1,'requirementsnone'],
              ["antropogenictransformation", 'SlateGray.TButton',0,7,1,1,'requirementsnone'],
              ["landscapediversity",'LimeGreen.TButton',1,7,1,1,'requirementsnone'],
              ["landscapetransf",'LimeGreen.TButton',3,7,1,1,'requirementsnone'],
              ["landcoverdynamics",'LimeGreen.TButton',1,5,1,1,'requirementsnone'],
              ["forestcover",'LimeGreen.TButton',4,7,1,1,'requirementsnone'],
              ["seismicity",'DodgerBlue.TButton',5,6,1,1,'requirementsnone'],
              ["dynamicsNDVI",'DeepPink.TButton',4,5,1,1,'requirementsnone'],
              ["NDVI", 'my.TButton',4,4,1,1,'requirementsnone'],
              ["lithology",'my.TButton',5,4,1,1,'requirementsnone'],
              ["NDMI",'my.TButton',7,3,1,1,'requirementsnone'],
              ["floods", 'DodgerBlue.TButton',7,4,1,1,'requirementsnone'],
              ["populatanddynam", 'SlateGray.TButton',7,5,1,1,'requirementsnone'],
              ["populatdensity", 'SlateGray.TButton',6,7,1,1,'requirementsnone'],
              ["precipitationchange", 'DodgerBlue.TButton',0,5,1,1,'requirementsnone'],
              ["precipitation", 'my.TButton',0,4,1,1,'requirementsnone'],
              ["machanicalsoil", 'my.TButton',1,4,1,1,'requirementsnone'],
              ["soilerosion", 'DodgerBlue.TButton',2,4,1,1,'requirementsnone'],
              ["NDWI", 'my.TButton',4,2,1,1,'requirementsnone'],
              ["Landslides", 'DodgerBlue.TButton',5,3,1,1,'requirementsnone'],
              ["distancefromroads", 'my.TButton',5,2,1,1,'requirementsnone'],
              ["FIRMS", 'my.TButton',7,2,1,1,'requirementsnone'],
              ["Aspect", 'Sienna.TButton',4,0,1,1,'requirementsnone'],
              ["temperature", 'my.TButton',0,1,1,1,'requirementsnone'],
              ["landsurftemperature", 'my.TButton',2,0,1,1,'requirementsnone'],
              ["thermalpollution",'Gold.TButton',1,0,1,1,'requirementsnone'],
              ["droughtindices", 'Gold.TButton',1,2,1,1,'requirementsnone'],
              ["desertification", 'Gold.TButton',2,2,1,1,'requirementsnone'],
              ["temperaturechange",'Tomato.TButton',1,1,1,1,'requirementsnone'],
              ["Firerisks", 'Tomato.TButton',6,2,1,1,'requirementsnone'],
              ["DEMdata", 'my.TButton',3,0,1,1,'requirementsnone'],
              ["Altitude", 'Sienna.TButton',2,1,1,1,'requirementsnone'],
              ["Curvature", 'Sienna.TButton',5,1,1,1,'requirementsnone'],
              ["topographicindex", 'my.TButton',4,3,1,1,'requirementsnone'],
              ["proximity", 'my.TButton',6,4,1,1,'requirementsnone'],
              ["Depth", 'Sienna.TButton',6,0,1,1,'requirementsnone'],
              ["Density", 'Sienna.TButton',7,1,1,1,'requirementsnone'],
              ["Steepness", 'Sienna.TButton',6,3,1,1,'requirementsnone'],
              
            ]
        for c in range(9): self.columnconfigure(index=c, weight=1)
        for r in range(9): self.rowconfigure(index=r, weight=1)
        
        #["mainsays", 'LimeGreen.TButton',8,0,1,9,'requirementzero'],
        self.mainsays=ttk.Label(self,
             textvariable=self.master.transtatedict["mainsays"], style='LimeGreen.TLabel', anchor="center")
        self.mainsays.grid(row=8,column=0, padx=6, pady=6,rowspan=1,columnspan=9, sticky=tk.NSEW)
        for i in self.bths:    
            self.btn[i[0]]=ttk.Button(self,
                 textvariable=self.master.transtatedict[i[0]], style=i[1])
            self.btn[i[0]].grid(row=i[2],column=i[3], padx=6, pady=6,rowspan=i[4],columnspan=i[5], sticky=tk.NSEW)    
   
            self.btn_tooltips[i[0]]= ToolTip(self.btn[i[0]],text=self.master.translations[self.master.language][i[6]])
        
        names_work=["all6startmainbutton", "snowcoverarea", "antropogenictransformation", "landscapediversity", "landscapetransf",
                    "landcoverdynamics", "forestcover", "dynamicsNDVI", "floods", "precipitationchange", "soilerosion", "Landslides",
                    "Aspect", "thermalpollution", "droughtindices", "desertification", "temperaturechange", "Firerisks", "Altitude",
                    "Curvature", "Depth", "Density", "Steepness"]
        for i in names_work:
            self.btn[i].config(state="disabled")
            
    def lang_change(self):
        
        for i in self.bths:
            self.btn_tooltips[i[0]].change_text(self.master.translations[self.master.language][i[6]])
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            