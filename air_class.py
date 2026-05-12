# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:30:44 2026

@author: Intel Core I9
"""
#from ttkbootstrap.widgets.tableview import Tableview
import threading
import rasterio
from rasterstats import zonal_stats
import geopandas

class air_calc(threading.Thread):
    def __init__(self,tk_self,names,files):
        super().__init__()
        self.should_stop = threading.Event()
        self.tk_self=tk_self
        self.names=names
        self.files=files
    
    def run(self):
        self.tk_self.after(0,lambda: self.tk_self.forget_grid("start"))
        default_crs = 'EPSG:4326'
        rastrs={}
        shape={}
        if self.should_stop.wait(1):
            self.tk_self.after(0,lambda: self.tk_self.forget_grid("stop"))
            self.tk_self.progbar.after(0,lambda: self.tk_self.progbar.stop())  
            self.tk_self.after(0,lambda: self.tk_self.on_calc())
            return None
        try:
            for i in self.names:
                self.text_insert("end",str(i)+"\n")
                if self.should_stop.wait(1):
                    self.tk_self.after(0,lambda: self.tk_self.forget_grid("stop"))
                    self.tk_self.progbar.after(0,lambda: self.tk_self.progbar.stop())  
                    self.tk_self.after(0,lambda: self.tk_self.on_calc())
                    return None
                rastrs_temp=[]
                shape_temp=[]
                if i!="all6mainbutton":
                    for k in self.files[i]:
                        self.text_insert("end",str(k)+"\n")
                        rastrs_temp.append(rasterio.open(k))
                    rastrs[i]=rastrs_temp
                else:
                    self.text_insert("end",str(self.files[i][0])+"\n")
                    shape=geopandas.read_file(self.files[i][0])
                    if shape.crs is None:
                        shape = shape.set_crs(default_crs)
            mean_values={}
            for i in self.names:
                self.text_insert("end",str(i)+"\n")
                if self.should_stop.wait(1):
                    self.tk_self.after(0,lambda: self.tk_self.forget_grid("stop"))
                    self.tk_self.progbar.after(0,lambda: self.tk_self.progbar.stop())  
                    self.tk_self.after(0,lambda: self.tk_self.on_calc())
                    return None
                if i!="all6mainbutton":
                    mean_values[i]=[]
                    for j in range(len(rastrs[i])):
                        self.text_insert("end",str(j)+"\n")
                        if self.should_stop.wait(1):
                            self.tk_self.after(0,lambda: self.tk_self.forget_grid("stop"))
                            self.tk_self.progbar.after(0,lambda: self.tk_self.progbar.stop()) 
                            self.tk_self.after(0,lambda: self.tk_self.on_calc())
                            return None
                        k=rastrs[i][j]
                        arr = k.read(1)
                        affine=k.transform
                        if k.crs != shape.crs:
                            shape_temp = shape.to_crs(k.crs)
                        else:
                            shape_temp=shape
                        stats = zonal_stats(shape_temp, arr, affine=affine, nodata=-999, stats="mean")
                        mean_values[i].append([self.files[i][j]]+[feat['mean'] for feat in stats if feat['mean']!=None]+[k.width]+[1]+[i]+[k.height])
                        self.text_insert("end",str(mean_values[i][-1][0])+" mean: "+str(mean_values[i][-1][1])+"\n")
            self.tk_self.after(0,lambda: self.tk_self.master.atm_shape_set(shape))
            self.tk_self.after(0,lambda: self.tk_self.master.atm_means_rastrs_set(mean_values))
            self.tk_self.continue_button.after(0,lambda: self.tk_self.continue_button.config(state="normal"))
        except Exception as err:
            if self.should_stop.wait(1):
                self.tk_self.after(0,lambda: self.tk_self.forget_grid("stop"))
                self.tk_self.progbar.after(0,lambda: self.tk_self.progbar.stop())   
                self.tk_self.after(0,lambda: self.tk_self.on_calc())
                return None
            self.text_insert("end",str(err)+"\n")
        self.tk_self.after(0,lambda: self.tk_self.forget_grid("stop"))
        self.tk_self.progbar.after(0,lambda: self.tk_self.progbar.stop())   
        self.tk_self.after(0,lambda: self.tk_self.on_calc())
    def text_insert(self,pos,mytext):
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.text.config(state="normal"))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.insert(pos,mytext))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.text.config(state="disabled"))
        self.tk_self.text_errors.after(0, lambda: self.tk_self.text_errors.see("end"))
    
    def Stop(self):
        self.should_stop.set()
        

















































