# -*- coding: utf-8 -*-

"""
Created on Sat May  2 16:16:24 2026

@author: Intel Core I9
"""

import os
import tkinter as tk
from functools import partial
import ttkbootstrap as ttk
from tkinter import filedialog
from tkinter.messagebox import showerror,askyesno
from ttkbootstrap.widgets.tableview import Tableview
#from ttkbootstrap.tableview import Tableview
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import rasterio
from rasterio.plot import show
import matplotlib
from matplotlib.figure import Figure
#from ttkbootstrap.tooltip import ToolTip as TT
from ttkbootstrap.widgets import ToolTip as TT
import configparser
from ttkbootstrap.widgets.scrolled import ScrolledText
#from ttkbootstrap.scrolled import ScrolledText
import threading
from rasterstats import zonal_stats
import geopandas
import pandas as pd
import re
import numpy as np
from rasterio.fill import fillnodata
import json

from tk_class import tk_class

def main():
    #path=os.path.dirname(os.path.abspath(__file__))
    path=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    root = tk_class(path)
    root.mainloop()
    del root


if __name__ == "__main__":
    main()