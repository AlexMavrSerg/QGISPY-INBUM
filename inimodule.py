# -*- coding: utf-8 -*-
"""
Created on Fri Aug 15 19:31:45 2025

@author: Intel Core I9
"""

import configparser
import os

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
