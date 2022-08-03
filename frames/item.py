# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  The Loinc Table Core
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   aestas MMXXI
# -----------------------------------------------------------------------------
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class UI(tk.Toplevel):
    def __init__(self, parent, index=None):
        super().__init__(name="item")

        self.parent = parent
        self.set_style()
        self.index = index
        self.transient(parent)
        self.resizable(0, 0)
        self.loinc_num = tk.StringVar()
        self.component = tk.StringVar()
        self.property = tk.StringVar()
        self.time_aspct = tk.StringVar()
        self.system = tk.StringVar()
        self.scale_typ = tk.StringVar()
        self.method_typ = tk.StringVar()
        self.class_ = tk.StringVar()
        self.class_type = tk.StringVar()
        self.long_common_name = tk.StringVar()
        self.short_name = tk.StringVar()
        self.external_copyright_notice = tk.StringVar()
        self.status = tk.StringVar()
        self.version_first_released = tk.StringVar()
        self.version_last_changed = tk.StringVar()

        self.init_ui()
        self.master.engine.center_me(self)

    def set_style(self):
        s = ttk.Style()

        s.configure("Mandatory.TLabel",
                    foreground=self.master.engine.get_rgb(0, 0, 255),
                    background=self.master.engine.get_rgb(255, 255, 255))

    def init_ui(self):

        w = self.master.engine.get_init_ui(self)

        r = 0
        c = 1
        ttk.Label(w, style="Mandatory.TLabel", text="Loinc Num:",).grid(row=r, sticky=tk.W)
        self.txtLoinc = ttk.Entry(w, textvariable=self.loinc_num)
        self.txtLoinc.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, style="Mandatory.TLabel", text="Component:",).grid(row=r, sticky=tk.W)
        self.txtComponent = ttk.Entry(w, textvariable=self.component)
        self.txtComponent.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Property:",).grid(row=r, sticky=tk.W)
        cbo = ttk.Combobox(w, values=self.get_records("PROPERTY"), textvariable=self.property)
        cbo.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Time Aspct:",).grid(row=r, sticky=tk.W)
        cbo = ttk.Combobox(w, values=self.get_records("TIME_ASPCT"), textvariable=self.time_aspct)
        cbo.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="System:",).grid(row=r, sticky=tk.W)
        cbo = ttk.Combobox(w, values=self.get_records("SYSTEM"), textvariable=self.system)
        cbo.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Scale Typ:",).grid(row=r, sticky=tk.W)
        cbo = ttk.Combobox(w, values=self.get_records("SCALE_TYP"), textvariable=self.scale_typ)
        cbo.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Method Typ:",).grid(row=r, sticky=tk.W)
        cbo = ttk.Combobox(w, values=self.get_records("METHOD_TYP"), textvariable=self.method_typ)
        cbo.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, style="Mandatory.TLabel", text="Class:",).grid(row=r, sticky=tk.W)
        self.cbClass = ttk.Combobox(w, values=self.get_records("CLASS"), textvariable=self.class_)
        self.cbClass.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="ClassType:",).grid(row=r, sticky=tk.W)
        cbo = ttk.Combobox(w, values=self.get_records("CLASSTYPE"), textvariable=self.class_type)
        cbo.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Long Common Name:",).grid(row=r, sticky=tk.W)
        ttk.Entry(w, textvariable=self.long_common_name).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, style="Mandatory.TLabel", text="ShortName:",).grid(row=r, sticky=tk.W)
        self.txtShortName = ttk.Entry(w, textvariable=self.short_name)
        self.txtShortName.grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="External Copyright Notice:",).grid(row=r, sticky=tk.W)
        ttk.Entry(w, textvariable=self.external_copyright_notice).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="Status:",).grid(row=r, sticky=tk.W)
        ttk.Combobox(w, values=self.get_records("STATUS"), textvariable=self.status).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="VersionFirstReleased:",).grid(row=r, sticky=tk.W)
        ttk.Entry(w, width=8, textvariable=self.version_first_released).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        r += 1
        ttk.Label(w, text="VersionLastChanged:",).grid(row=r, sticky=tk.W)
        ttk.Entry(w, width=8, textvariable=self.version_last_changed).grid(row=r, column=c, sticky=tk.W, padx=5, pady=5)

        self.master.engine.get_save_cancel(self, w)

    def on_open(self, selected_class, selected_item=None):

        self.selected_class = selected_class

        if self.index is not None:
            self.selected_item = selected_item
            msg = "Edit {0}".format(self.winfo_name().capitalize())
            self.txtLoinc.config(state="disabled")
            self.set_values()
            self.txtComponent.focus()
        else:
            msg = "Add {0}".format(self.winfo_name().capitalize())
            self.class_.set(self.selected_class)
            self.txtLoinc.focus()

        self.title(msg)

    def get_records(self, field):
        sql = " SELECT DISTINCT({0}) FROM LoincTableCore ORDER BY {0} ASC;".format(field)
        return self.master.engine.read(True, sql, ())

    def set_values(self,):

        self.loinc_num.set(self.selected_item[0])
        self.component.set(self.selected_item[1])
        self.property.set(self.selected_item[2])
        self.time_aspct.set(self.selected_item[3])
        self.system.set(self.selected_item[4])
        self.scale_typ.set(self.selected_item[5])
        self.method_typ.set(self.selected_item[6])
        self.class_.set(self.selected_item[7])
        self.class_type.set(self.selected_item[8])
        self.long_common_name.set(self.selected_item[9])
        self.short_name.set(self.selected_item[10])
        self.external_copyright_notice.set(self.selected_item[11])
        self.status.set(self.selected_item[12])
        self.version_first_released.set(self.selected_item[13])
        self.version_last_changed.set(self.selected_item[14])

    def get_values(self,):

        return [self.component.get(),
                self.property.get(),
                self.time_aspct.get(),
                self.system.get(),
                self.scale_typ.get(),
                self.method_typ.get(),
                self.class_.get(),
                self.class_type.get(),
                self.long_common_name.get(),
                self.short_name.get(),
                self.external_copyright_notice.get(),
                self.status.get(),
                self.version_first_released.get(),
                self.version_last_changed.get(),]

    def on_save(self, evt=None):

        if self.on_fields_control() == False: return
        if self.check_code() == False: return
        if messagebox.askyesno(self.master.title(),
                               self.master.engine.ask_to_save,
                               parent=self) == True:

            args = self.get_values()

            if self.index is not None:

                sql = self.master.engine.get_update_sql("LoincTableCore", "LOINC_NUM")

                args.append(self.selected_item[0])

            else:

                args.insert(0, self.loinc_num.get())

                sql = "INSERT INTO LoincTableCore VALUES({0});".format(",".join("?"*(len(args))))

            last_id = self.master.engine.write(sql, args)

            self.parent.on_class_selected()

            if self.index is not None:
                self.parent.lstItems.selection_set(self.index)
                self.parent.lstItems.see(self.index)
            else:
                self.parent.lstItems.selection_set(last_id)
                self.parent.lstItems.see(last_id)

            self.on_cancel()

        else:
            messagebox.showinfo(self.master.title(),
                                self.master.engine.abort,
                                parent=self)

    def check_code(self):

        sql = "SELECT LOINC_NUM, COMPONENT FROM LoincTableCore WHERE LOINC_NUM = ?"

        rs = self.master.engine.read(False, sql, (self.loinc_num.get(),))

        if rs:

            if self.index is not None:
                if rs[0] != self.selected_item[0]:
                    msg = "LOINC Code {0} has already been assigned!".format(self.loinc_num.get(),)
                    messagebox.showwarning(self.master.title(), msg, parent=self)
                    return 0
            else:
                msg = "LOINC code {0} has already been assigned!".format(self.loinc_num.get(),)
                messagebox.showwarning(self.master.title(), msg, parent=self)
                return 0

    def on_fields_control(self):

        dict_fields = {self.txtLoinc:"Loinc Num",
                       self.txtComponent:"Component",
                       self.cbClass:"Class",
                       self.txtShortName:"Short Name"}

        for k, v in dict_fields.items():
            if not k.get():
                msg = "The {0} field is mandatory".format(dict_fields[k])
                messagebox.showwarning(self.master.title(), msg, parent=self)
                self.focus()
                k.focus_set()
                return 0

    def on_cancel(self, evt=None):
        self.destroy()
