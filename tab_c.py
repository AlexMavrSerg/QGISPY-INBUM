# -*- coding: utf-8 -*-
"""
Created on Thu Aug 14 11:55:11 2025

@author: Intel Core I9
"""

import tkinter as tk
from tkinter import Tk, ttk, font

class TabC(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.credits = tk.Text(self)
        self.credits.place(relheight=0.95, relwidth=0.95, relx=0, rely=0)
        self.ys = ttk.Scrollbar(self,orient = "vertical", command = self.credits.yview)
        self.ys.place(relheight=0.95, relwidth=0.05, relx=0.95, rely=0)
        self.xs = ttk.Scrollbar(self,orient = "horizontal", command = self.credits.xview)
        self.xs.place(relheight=0.05, relwidth=0.95, relx=0, rely=0.95)
        self.credits["yscrollcommand"] = self.ys.set
        self.credits["xscrollcommand"] = self.xs.set
        self.credits.insert("1.0", """Команда проекта:
                                    Греков Александр Николаевич
                                    Маврин Александр Сергеевич
                                    Табунщик Владимир""")
        self.credits.configure(state=tk.DISABLED)
        
        self.pack(expand=True, fill=tk.BOTH)