# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  The Loinc Table Core
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   aestas MMXXI
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk


class UI(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(name="license")

        self.parent = parent
        #self.resizable(0, 0)
        self.init_ui()
        self.master.engine.center_me(self)

    def init_ui(self):

        w = ttk.Frame(self, padding=4)

        self.txLicense = self.master.engine.get_text_box(w,)

        w.pack(fill=tk.BOTH, expand=1)

    def on_open(self):

        msg = self.master.engine.get_license()

        if msg:
            self.txLicense.insert("1.0", msg)

        self.title(self.master.title())

