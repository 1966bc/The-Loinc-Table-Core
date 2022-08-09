# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  The Loinc Table Core
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   aestas MMXXI
# -----------------------------------------------------------------------------
""" This is the main module of The Loinc Table Core."""

__author__ = "1966bc"
__copyright__ = "Copyleft"
__credits__ = ["hal9000", ]
__license__ = "GNU GPL Version 3, 29 June 2007"
__version__ = "2.72"
__maintainer__ = "1966bc"
__email__ = "giuseppecostanzi@gmail.com"
__date__ = "Aestas MMXXI"
__status__ = "production"
__icon__ = "LOINC® logo"

import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog as fd

import frames.license
import frames.item as ui
from engine import Engine


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__()

        self.dict_colors = {"ACTIVE": "white",
                            "TRIAL": "yellow",
                            "DISCOURAGED": "orange",
                            "DEPRECATED": "red",}

        self.parent = parent
        self.ops = ("Laboratory", "Clinical", "Claims attachments", "Surveys")
        self.option_id = tk.IntVar()
        self.type_id = tk.IntVar()
        self.search = tk.StringVar()
        self.status_bar_text = tk.StringVar()
        self.init_menu()
        self.init_toolbar()
        self.init_status_bar()
        self.init_ui()
        self.center_ui()

    def init_menu(self):

        m_main = tk.Menu(self, bd=1)
        m_file = tk.Menu(m_main, tearoff=0, bd=1)
        m_about = tk.Menu(m_main, tearoff=0, bd=1)
        s_databases = tk.Menu(m_file)

        items = (("File", m_file), ("?", m_about),)

        for i in items:
            m_main.add_cascade(label=i[0], underline=0, menu=i[1])

        m_file.add_cascade(label="Database", menu=s_databases, underline=0)

        items = (("Import", self.on_import),
                 ("Dump", self.on_dump),
                 ("Vacuum", self.on_vacuum),)

        for i in items:
            s_databases.add_command(label=i[0], underline=0, command=i[1])

        m_file.add_command(label="Log", underline=1, command=self.on_log)

        m_file.add_separator()

        m_file.add_command(label="Exit", underline=0, command=self.parent.on_exit)

        items = (("About", self.on_about),
                 ("License", self.on_license),
                 ("Python", self.on_python_version),
                 ("Tkinter", self.on_tkinter_version),)

        for i in items:
            m_about.add_command(label=i[0], underline=0, command=i[1])

        for i in (m_main, m_file, ):
            i.config(bg=self.master.engine.get_rgb(240, 240, 237),)
            i.config(fg="black")

        self.master.config(menu=m_main)

    def init_toolbar(self):

        toolbar = tk.Frame(self, bd=1, relief=tk.RAISED)

        img_exit = tk.PhotoImage(data=self.master.engine.get_icon("exit"))
        img_info = tk.PhotoImage(data=self.master.engine.get_icon("info"))

        exitButton = tk.Button(toolbar, width=20, image=img_exit,
                               relief=tk.FLAT, command=self.parent.on_exit)
        infoButton = tk.Button(toolbar, width=20, image=img_info,
                               relief=tk.FLAT, command=self.on_about)

        exitButton.image = img_exit
        infoButton.image = img_info

        exitButton.pack(side=tk.LEFT, padx=2, pady=2)
        infoButton.pack(side=tk.LEFT, padx=2, pady=2)

        toolbar.config(bg=self.master.engine.get_rgb(240, 240, 237))
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def init_status_bar(self):

        self.status = ttk.Label(self,
                                textvariable=self.status_bar_text,
                                style='StatusBar.TLabel',
                                anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

    def init_ui(self):
        """create widgets"""

        self.pack(fill=tk.BOTH, expand=1)

        container_frame = ttk.Frame(self, style='W.TFrame')
        left_frame = ttk.LabelFrame(container_frame,
                                    style="W.TLabelframe",
                                    text="Classes",
                                    padding=2)

        self.lstClasses = self.master.engine.get_listbox(left_frame,)
        self.lstClasses.bind("<<ListboxSelect>>", self.on_class_selected)
        self.lstClasses.bind("<Double-Button-1>", self.on_class_activated)


        middle_frame = ttk.Frame(container_frame, style='W.TFrame')

        ttk.Label(middle_frame,
                  style='W.TLabel',
                  text="Search",
                  anchor=tk.W,).pack(fill=tk.X)

        self.txtSearch = ttk.Entry(middle_frame, textvariable=self.search)
        self.txtSearch.bind("<Return>", self.on_search)
        self.txtSearch.bind("<KP_Enter>", self.on_search)
        self.txtSearch.pack(fill=tk.X,)

        cols = (["#0", "Number", "w", True, 80, 80],
                ["#1", "Component", "w", True, 300, 300],
                ["#2", "System", "w", True, 100, 100],
                ["#3", "Property", "w", True, 50, 50],
                ["#4", "Class", "w", True, 50, 50],
                ["#5", "Status", "w", True, 50, 50],)

        self.lblItems = ttk.LabelFrame(middle_frame,
                                       style="W.TLabelframe",
                                       text="Items",
                                       padding=2)
        self.lstItems = self.master.engine.get_tree(self.lblItems, cols,)
        for k, v in self.dict_colors.items():
            self.lstItems.tag_configure(k, background=v)
        self.lstItems.bind("<<TreeviewSelect>>", self.on_item_selected)
        self.lstItems.bind("<Double-1>", self.on_item_double)
        self.lblItems.pack(fill=tk.BOTH, expand=1)

        right_frame = ttk.Frame(container_frame, style='W.TFrame')

        bts = [("Search", 0, self.on_search, "<Alt-s>"),
               ("Reset", 0, self.on_reset, "<Alt-r>"),
               ("Close", 0, self.parent.on_exit, "<Alt-c>")]

        for btn in bts:
            ttk.Button(right_frame,
                       style='W.TButton',
                       text=btn[0],
                       underline=btn[1],
                       command=btn[2], ).pack(fill=tk.X, padx=5, pady=5)
            self.parent.bind(btn[3], btn[2])

        self.master.engine.get_radio_buttons(right_frame,
                                             "Classes",
                                             self.ops,
                                             self.option_id,
                                             self.set_classes).pack(fill=tk.BOTH,
                                                                    padx=5, pady=5)

        self.master.engine.get_radio_buttons(right_frame,
                                             "Search type",
                                             ("Component", "Number",),
                                             self.type_id,
                                             self.set_classes).pack(fill=tk.BOTH,
                                                                    padx=5, pady=5)

        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=0)
        middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5, pady=5, expand=1)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=5, expand=0)
        container_frame.pack(fill=tk.BOTH, expand=1, padx=5, pady=5)

    def center_ui(self):

        ws = self.master.winfo_screenwidth()
        hs = self.master.winfo_screenheight()
        # calculate position x, y
        d = self.master.engine.get_dimensions()
        w = int(d["w"])
        h = int(d["h"])
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.master.geometry("%dx%d+%d+%d" % (w, h, x, y))

    def on_open(self, evt=None):

        self.on_reset()

    def on_reset(self, evt=None):

        sql = "SELECT COUNT(*) FROM LoincTableCore;"

        rs = self.master.engine.read(False, sql, ())

        count = rs[0]

        s = "{0} {1} {2}".format(self.master.title(), "items", count)

        self.status_bar_text.set(s)

        self.set_classes()

        self.clear_items()

        self.search.set("")

        self.txtSearch.focus()

    def on_search(self, evt=None):

        fields = ("[COMPONENT]", "[LOINC_NUM]", "[SHORTNAME]")

        sql = "SELECT [LOINC_NUM],[COMPONENT],\
                      [SYSTEM],[PROPERTY],[CLASS],[STATUS]\
               FROM  LoincTableCore WHERE {0}\
               LIKE ?\
               ORDER BY [COMPONENT] ASC;".format(fields[self.type_id.get()])

        args = tuple(self.get_sql_args())

        self.set_items(sql, args)

    def get_values(self,):

        return [self.search.get(), ]

    def get_sql_args(self):

        args = self.get_values()

        for n, arg in enumerate(args):
            if len(arg) == 0 and n > 0:
                args[n] = "%"
            else:
                args[n] = args[n]+"%"

        return args

    def set_classes(self,):

        sql = "SELECT [CLASS]\
               FROM LoincTableCore\
               WHERE [classtype]=?\
               GROUP BY [class];"

        self.lstClasses.delete(0, tk.END)

        rs = self.master.engine.read(True, sql, (self.option_id.get()+1,))

        if rs:
            for i in rs:
                s = "{0}".format(i[0])
                self.lstClasses.insert(tk.END, s)

    def on_class_selected(self, evt=None):

        sql = "SELECT [LOINC_NUM],[COMPONENT],\
                      [SYSTEM],[PROPERTY],[CLASS],[STATUS]\
               FROM LoincTableCore\
               WHERE [CLASS] =?\
               ORDER BY [COMPONENT] ASC;"

        if self.lstClasses.curselection():
            selected_class = self.lstClasses.get(self.lstClasses.curselection())
            args = (selected_class,)
            self.selected_class = selected_class
            self.set_items(sql, args)

    def on_class_activated(self, evt=None):

        if self.lstClasses.curselection():
            selected_class = self.lstClasses.get(self.lstClasses.curselection())
            self.obj = ui.UI(self)
            self.obj.on_open(selected_class)

        else:
            messagebox.showwarning(self.master.title(),
                                   self.master.engine.no_selected,
                                   parent=self)

    def clear_items(self):

        for i in self.lstItems.get_children():
            self.lstItems.delete(i)

    def set_items(self, sql, args):

        self.master.engine.busy(self)

        self.clear_items()

        rs = self.master.engine.read(True, sql, args)

        if rs:

            for i in rs:

                tag_config = (i[5])

                self.lstItems.insert("", tk.END, iid=i[0], text=i[0],
                                     values=(i[1], i[2], i[3], i[4], i[5],),
                                     tags=tag_config)

        s = "{0} {1}".format("Items", len(self.lstItems.get_children()))

        self.lblItems["text"] = s

        self.master.engine.not_busy(self)

    def on_item_double(self, evt):
        self.on_edit(self)

    def on_item_selected(self, evt):

        if self.lstItems.focus():
            item_iid = self.lstItems.selection()
            pk = item_iid[0]
            self.selected_item = self.master.engine.get_selected("LoincTableCore",
                                                                 "LOINC_NUM",
                                                                 pk)

    def on_edit(self, evt):

        if self.lstItems.focus():

            item_iid = self.lstItems.selection()

            ui.UI(self, item_iid).on_open(self.selected_class, self.selected_item,)

        else:
            messagebox.showwarning(self.master.title(),
                                   self.master.engine.no_selected,
                                   parent=self)

    def on_import(self, args=None):

        selected_file = fd.askopenfilename(title="Select file",
                                           filetypes=(("csv files", "*.csv"),
                                                      ("all files", "*.*")))

        try:

            if os.path.isfile(selected_file):

                self.master.engine.busy(self)

                p = self.master.engine.get_table_core(selected_file)

                if p == 0:

                    s = "The import operation has been successful.\nRetuned value:{0}".format(p)
                else:
                    s = "The import operation has failed.\nRetuned value:{0}".format(p)


                self.on_reset()

                messagebox.showinfo(self.master.title(), s, parent=self)

        except:
            s = "Houston we've had a problem here.\n{0}\nx{1}"
            msg = s.format(sys.exc_info()[1], sys.exc_info()[0])
            messagebox.showinfo(self.master.title(), msg, parent=self)
        finally:
            self.master.engine.not_busy(self)


    def on_license(self):
        frames.license.UI(self).on_open()

    def on_python_version(self):
        s = self.master.engine.get_python_version()
        messagebox.showinfo(self.master.title(), s, parent=self)

    def on_tkinter_version(self):
        s = "Tkinter patchlevel\n{0}".format(self.master.tk.call("info", "patchlevel"))
        messagebox.showinfo(self.master.title(), s, parent=self)

    def on_about(self,):
        messagebox.showinfo(self.master.title(),
                            self.master.info,
                            parent=self)

    def on_dump(self):
        self.master.engine.busy(self)
        self.master.engine.dump()
        self.master.engine.not_busy(self)
        messagebox.showinfo(self.master.title(), "Dump executed.", parent=self)

    def on_vacuum(self):
        sql = "VACUUM;"
        self.master.engine.busy(self)
        self.master.engine.write(sql)
        self.master.engine.not_busy(self)
        messagebox.showinfo(self.master.title(), "Vacuum executed.", parent=self)

    def on_log(self,):
        self.master.engine.get_log_file()


class App(tk.Tk):
    """Application start here"""
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.engine = Engine()
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.engine.set_style(kwargs["theme"])
        self.set_title(kwargs["title"])
        self.set_icon()
        self.set_info()

        Main(self).on_open()

    def set_title(self, title):
        s = "{0}".format(title)
        self.title(s)

    def set_icon(self):
        icon = tk.PhotoImage(data=self.engine.get_icon("app"))
        self.call("wm", "iconphoto", self._w, "-default", icon)

    def set_info(self,):
        msg = "{0}\nauthor: {1}\ncopyright: {2}\ncredits: {3}\nlicense: {4}\nversion: {5}\
               \nmaintainer: {6}\nemail: {7}\ndate: {8}\nstatus: {9}"
        info = msg.format(self.title(), __author__, __copyright__, __credits__,
                          __license__, __version__, __maintainer__, __email__,
                          __date__, __status__)
        self.info = info

    def on_exit(self, evt=None):
        if messagebox.askokcancel(self.title(), "Do you want to quit?", parent=self):
            self.engine.con.close()
            self.destroy()


def main():
    # if you want pass a number of arbitrary args or kwargs...
    args = []

    for i in sys.argv:
        args.append(i)
    # ('clam', 'alt', 'default', 'classic')
    kwargs = {"theme": "default", "title": "The Loinc Table Core"}

    app = App(*args, **kwargs)

    app.mainloop()


if __name__ == "__main__":
    main()
