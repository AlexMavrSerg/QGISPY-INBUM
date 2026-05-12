# -*- coding: utf-8 -*-
"""
Created on Mon May 11 22:05:52 2026

@author: Intel Core I9
"""

import threading
import rasterio
import re
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from rasterio.plot import show
from matplotlib.figure import Figure
from rasterio.fill import fillnodata

class air_poll_last_calc(threading.Thread):
    def __init__(self,tk_self,names,mean,dangercoef,debugger,path):
        super().__init__()
        self.should_stop = threading.Event()  # Create an unset event on init
        self.tk_self=tk_self
        self.names=names
        self.mean=mean
        self.debugger=debugger
        self.savepath=path
        self.dangercoef=dangercoef
    def run(self):
        self.tk_self.after(0,lambda: self.tk_self.forget_grid("start"))
        #default_crs = 'EPSG:4326'
        rastr_sum=None
        c=0
        if self.should_stop.wait(1):
            self.on_exit()
        else:
            try:
                for i in self.names:
                    if self.should_stop.wait(1):
                        self.on_exit()
                    else:
                        if i!="all6mainbutton":
                            self.text_insert("end",str(i)+"\n")
                            for k in self.mean[i]:
                                if self.should_stop.wait(1):
                                    self.on_exit()
                                else:
                                    if k[3]==1:
                                        self.text_insert("end",str(k[0])+"\n")
                                        rastr,profile,nodata_val,mask,transform=self.rastr_calc(k[0],k[1],self.dangercoef[i])
                                        if c!=0:
                                            rastr_sum+=rastr
                                            rastr_sum = fillnodata(rastr_sum, mask=mask, max_search_distance=100.0)
                                        else:
                                            c=1
                                            rastr_sum=rastr
                                        if self.debugger==1:
                                            self.save_rstr(self.savepath,"rastr_sum_.tif",rastr_sum, profile)
                                        self.visualible_image(rastr_sum,"rastr_sum",transform)                    
                self.tk_self.after(0,lambda: self.tk_self.master.atm_sum_rastrs_set([rastr_sum,profile,transform]))
                self.tk_self.continue_button.after(0,lambda: self.tk_self.continue_button.config(state="normal"))
            except Exception as err:
                self.text_insert("end",str(err)+"\n")
                if self.should_stop.wait(1):
                    self.on_exit()
        self.on_exit()
            
    def rastr_calc(self,file,mean,dangerc):
        self.text_insert("end",str(file)+"\n")
        name_file=re.split(r'[\\/]', file)[-1]
        with rasterio.open(file) as rstr:
            data=rstr.read(1,masked=True)
            profile=rstr.profile
            nodata_val=rstr.nodata
            mask = rstr.dataset_mask() 
            transform=rstr.transform
        self.visualible_image(data,str(name_file),transform)
        if self.should_stop.wait(1):
            self.on_exit()
        else:
            divided_mean=data.astype('float32') / mean
            if self.debugger==1:
                self.save_rstr(self.savepath,"divided_mean_"+name_file,divided_mean,profile)
            self.visualible_image(divided_mean,"divided_mean",transform)
            #divided_mean_nodata=divided_mean.filled(nodata_val)
            divided_mean_nodata = fillnodata(divided_mean, mask=mask, max_search_distance=100.0)
            if self.debugger==1:
                self.save_rstr(self.savepath,"divided_mean_nodata_"+name_file,divided_mean_nodata,profile)
            self.visualible_image(divided_mean_nodata,"divided_mean_nodata",transform)
            profile.update(dtype=rasterio.float32, count=1)
            #divided_mean_nodata_floated=divided_mean_nodata.filled(profile["nodata"])
            if self.debugger==1:
                self.save_rstr(self.savepath,"divided_mean_nodata_floated_"+name_file,divided_mean_nodata,profile)
            with np.errstate(invalid='ignore'):
                divided_mean_powered=divided_mean_nodata**dangerc
            if self.debugger==1:
                self.save_rstr(self.savepath,"divided_mean_powered_"+name_file,divided_mean_powered,profile)
            self.visualible_image(divided_mean_powered,"divided_mean_powered",transform)
            divided_mean_powered = np.ma.masked_invalid(divided_mean_powered)
            if self.debugger==1:
                self.save_rstr(self.savepath,"divided_mean_powered_to_raster_"+name_file,divided_mean_powered,profile)
            self.visualible_image(divided_mean_powered,"divided_mean_powered_to_raster",transform)
            #divided_mean_powered_nodata=divided_mean_powered.filled(nodata_val)
            divided_mean_powered_nodata = fillnodata(divided_mean_powered, mask=mask, max_search_distance=100.0)
            if self.debugger==1:
                self.save_rstr(self.savepath,"divided_mean_powered_nodata_"+name_file,divided_mean_powered_nodata,profile)
            self.visualible_image(divided_mean_powered_nodata,"divided_mean_powered_nodata",transform)
            return divided_mean_powered_nodata, profile, nodata_val, mask,transform
    def save_rstr(self,path,name,data,profile):
        with rasterio.open(path+name,'w',**profile) as dstr:
            dstr.write(data,1)
    def visualible_image(self,raster,name,transform):
        fig = Figure(figsize=(5, 3.5), dpi=100)
        canvas = FigureCanvasTkAgg(fig, master=self.tk_self.text_errors)
        ax = fig.add_subplot()
        show(raster,ax=ax,transform=transform, cmap='terrain')
        canvas.draw()
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.text.config(state="normal"))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.window_create("end",window=canvas.get_tk_widget()))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.insert("end",str(name)+"\n"))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.text.config(state="disabled"))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.see("end"))
    def text_insert(self,pos,mytext):
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.text.config(state="normal"))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.insert(pos,mytext))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.text.config(state="disabled"))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.see("end"))
    def on_exit(self):
        self.tk_self.after(0,lambda: self.tk_self.forget_grid("stop"))
        self.tk_self.progbar.after(0,lambda: self.tk_self.progbar.stop())  
        self.tk_self.after(0,lambda: self.tk_self.on_calc())
    def Stop(self):
        self.should_stop.set()