# -*- coding: utf-8 -*-
"""
Created on Sun May  3 10:12:59 2026

@author: Intel Core I9
"""

import json
import os
class languages_struct():
    def __init__(self,path,name):
        self.translations=None
        self.path=path+'\\settings\\'+name+'.json'
        if os.path.isfile(self.path):
            self.load_struct()
        else:
            self.create_struct()
            self.save_struct()
    def load_struct(self):
        with open(self.path,'r',encoding='utf-8') as file:
            self.translations=json.load(file)
    def save_struct(self):
        with open(self.path,'w',encoding='utf-8') as file:
            json.dump(self.translations, file, ensure_ascii=False,indent=4)
    def create_struct(self):
        self.translations = { "russian" : {
    "theme" : "Тема",
    "windsize" : "Размер окна",
    "O3mainbutton" : "Загрязнение воздуха\nO3",
    "SO2mainbutton" : "Загрязнение воздуха\nSO2",
    "CH4mainbutton" : "Загрязнение воздуха\nCH4",
    "COmainbutton" : "Загрязнение воздуха\nCO",
    "HCHOmainbutton" : "Загрязнение воздуха\nHCHO",
    "NOmainbutton" : "Загрязнение воздуха\nNO",
    "all6mainbutton" : "Выбрать шейп\nЗагрязнений воздуха",
    "all6startmainbutton" : "Комплексный индекс\nзагрязнения атмосферы",
    "language" : "Язык",
    "snowcoverarea" : "Изменение площади\nснежного покрова",
    "antropogenictransformation" : "Индекс\nантропогенной\nтрансформации",
    "landcoverdynamics" : "Динамика\nназемного\nпокрова",
    "landscapediversity" : "Ланшафтное\nразнообразие",
    "landcoverdata" : "Наземный\nпокров",
    "landscapetransf" : "Фрагментация\nландшафтов",
    "forestcover" : "Динамика\nлесного\nпокрова",
    "seismicity" : "Сейсмическая\nопасность",
    "populatanddynam" : "Динамика\nнаселения",
    "populatdensity" : "Динамика\nплотности\nнаселения",
    "DEMdata" : "DEM",
    "Altitude" : "Высота над\nуровнем моря",
    "Curvature" : "Кривизна\nрельефа",
    "topographicindex" : "Топографический\nиндекс\nрасчлененности",
    "proximity" : "Близость к\nдренажной\nсети",
    "Depth" : "Глубина\nрасчленения\nрельефа",
    "Density" : "Плотность\nрасчленения\nрельефа",
    "Steepness" : "Крутизна\nсклонов",
    "Aspect" : "Экспозиция",
    "temperature" : "Температура",
    "landsurftemperature" : "Температура\nповерхности",
    "thermalpollution" : "Тепловое\nзагрязнение",
    "droughtindices" : "Индекс\nзасухи",
    "desertification" : "Индекс\nопустынивания",
    "temperaturechange" : "Динамика\nтемпературы",
    "Firerisks" : "Пожары",
    "precipitationchange" : "Динамика\nколичества\nосадков",
    "precipitation" : "Осадки",
    "machanicalsoil" : "Механический\nсостав почв",
    "soilerosion" : "Потери почвы\nи эррозия",
    "NDWI" : "NDWI",
    "Landslides" : "Оползни",
    "distancefromroads" : "Расстояние\nот дорог",
    "FIRMS" : "FIRMS",
    "dynamicsNDVI" : "Динамика\nNDVI",
    "NDVI" : "NDVI",
    "lithology" : "Литология",
    "NDMI" : "NDMI",
    "floods" : "Наводнения",
    "fullscreen" : "Полный экран",
    "mainsays" : "Геоэкологическая оценка территории",
    "requirementsnone" : "Требуется: Нет",
    "requirementzero" : "",
    "requirementair" : "Требуется:\nЗагрязнение воздуха O3\nЗагрязнение воздуха SO2\nЗагрязнение воздуха CH4\nЗагрязнение воздуха CO\nЗагрязнение воздуха HCHO\nЗагрязнение воздуха NO",
    "canceled" : "Назад",
    "loadone" : "Выбрать растр",
    "loadshape" : "Выбрать шейп",
    "loaddir" : "Загрузить все\nрастры из папки",
    "deletesel" : "Удалить выбранные\nэлементы",
    "air_wait_hello" : "Обработка загрязнения воздуха",
    "continued" : "Продолжить",
    "stop" : "Стоп",
    "start" : "Старт",
    "savepath" : "путь сохранения",
    "meanview" : "Найденные средние",
    "save" : "Сохранить",
    "saveas" : "Сохранить как...",
    "meanselectedframe" : "Выбрать растры в работу",
    "onened" : "Включить",
    "offed" : "Выключить",
    "summ_air_end" : "Итоговая сумма"
    #"" : ""
    },
    "english" : {
        "theme" : "Theme",
        "windsize" : "Window size",
        "O3mainbutton" : "Air pollution\nO3",
        "SO2mainbutton" : "Air pollution\nSO2",
        "CH4mainbutton" : "Air pollution\nCH4",
        "COmainbutton" : "Air pollution\nCO",
        "HCHOmainbutton" : "Air pollution\nHCHO",
        "NOmainbutton" : "Air pollution\nNO",
        "all6mainbutton" : "Select shape of\nAir pollutions",
        "all6startmainbutton" : "Complex index\nof air pollution",
        "language" : "Language",
        "snowcoverarea" : "Change in snow\ncover area",
        "antropogenictransformation" : "Antropogenic\ntransformation\nindices",
        "landcoverdynamics" : "Land use/\nLand cover\nDynamics",
        "landscapediversity" : "Landscape\ndiversity",
        "landcoverdata" : "Land use/\nLand cover",
        "landscapetransf" : "Landscape\nfragmentation",
        "forestcover" : "Change in\nforest cover",
        "seismicity" : "Seismicity",
        "populatanddynam" : "Population and\nit's dynamics",
        "populatdensity" : "Population\ndensity and\nit's dynamic",
        "DEMdata" : "DEM",
        "Altitude" : "Altitude",
        "Curvature" : "Curvature\nof relief",
        "topographicindex" : "Topographic\nroughness\nIndex",
        "proximity" : "Proximity to\ndrainage\nnetwork",
        "Depth" : "Depth of relief\ndissection",
        "Density" : "Density of relief\ndissection",
        "Steepness" : "Steepness\nof slopes",
        "Aspect" : "Aspect",
        "temperature" : "Temperature",
        "landsurftemperature" : "Land surface\ntemperature",
        "thermalpollution" : "Thermal\npollution",
        "droughtindices" : "Drought\nindices",
        "desertification" : "Desertification",
        "temperaturechange" : "Temperature\nchange",
        "Firerisks" : "Fire risks",
        "precipitationchange" : "Precipitation\nchange",
        "precipitation" : "Precipitation",
        "machanicalsoil" : "Mechanical soil\ncomposition",
        "soilerosion" : "Soil\nErosion",
        "NDWI" : "NDWI",
        "Landslides" : "Landslides",
        "distancefromroads" : "Distance\nfrom roads",
        "FIRMS" : "FIRMS",
        "dynamicsNDVI" : "Dynamics\nof NDVI",
        "NDVI" : "NDVI",
        "lithology" : "Lithology",
        "NDMI" : "NDMI",
        "floods" : "Floods",
        "fullscreen" : "Fullscreen",
        "mainsays" : "Geoecological State of Territory",
        "requirementsnone" : "Requirements: None",
        "requirementzero" : "",
        "requirementair" : "Requirements:\nAir pollution O3\nAir pollution SO2\nAir pollution CH4\nAir pollution CO\nAir pollution HCHO\nAir pollution NO",
        "canceled" : "Назад",
        "loadone" : "Load rastr",
        "loadshape" : "Load shape",
        "loaddir" : "Load all\nrastrs from dir",
        "deletesel" : "Delete selected elements",
        "air_wait_hello" : "Processing Air pollution",
        "continued" : "Continue",
        "stop" : "Stop",
        "start" : "Start",
        "savepath" : "Save path",
        "meanview" : "Searched means",
        "save" : "Save",
        "saveas" : "Save as...",
        "meanselectedframe" : "Select rastrs to work",
        "onened" : "Turn on",
        "offed" : "Turn off",
        "summ_air_end" : "Calculated summ"
        }
    
    }















































