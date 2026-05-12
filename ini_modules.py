# -*- coding: utf-8 -*-
"""
Created on Sat May  2 16:31:57 2026

@author: Intel Core I9
"""
import configparser
import os

class ini_programm():
    def __init__(self,path,name):
        self.__settings = configparser.ConfigParser()
        self.__settings.sections()
        self.spath=path
        self.orig_path=path+"/output"
        self.path=path+'\\settings\\'+name+'.ini'
        self.settings_read()

        
    def settings_get(self,name,section="DEFAULT"):
        return self.__settings[section][name]

    def settings_set(self,value,name,section="DEFAULT"):
        self.__settings[section][name]=str(value)
        self.settings_save()
        self.create_dirs()
    def settings_read(self):
        self.create_dirs()
        if os.path.isfile(self.path):
            self.__settings.read(self.path)
        else:
            self.settings_create()
            self.settings_save()
        self.create_dirs()
    def settings_create(self):
        if not os.path.isfile(self.path):
            self.__settings['DEFAULT'] = {'pathtosave': str(self.orig_path),
                                 'theme': 'cosmo',
                                 'fullscreen': '0',
                                 'language': 'russian',
                                 'screensize': '1200x720',
                                 'debugger' : '0'}
    def settings_save(self):
        with open(self.path, 'w') as configfile:
          self.__settings.write(configfile)
          
    def create_dirs(self):
        try:
            if os.path.isdir(self.spath+"/settings")==False:
                os.mkdir(self.spath+"/settings")
            if os.path.isdir(str(self.__settings['DEFAULT']['pathtosave']))==False:
                os.mkdir(str(self.__settings['DEFAULT']['pathtosave']))
            if int(self.__settings['DEFAULT']['debugger'])==1:
                if os.path.isdir(str(self.__settings['DEFAULT']['pathtosave'])+"/debug")==False:
                    os.mkdir(str(self.__settings['DEFAULT']['pathtosave'])+"/debug")
        except:
            pass