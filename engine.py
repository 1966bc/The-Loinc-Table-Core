# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  The Loinc Table Core
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   aestas MMXXI
# -----------------------------------------------------------------------------
import os
import sys
import inspect
import datetime
import subprocess

from dbms import DBMS
from importer import Importer
from tools import Tools


class Engine(DBMS, Importer, Tools):
    def __init__(self,):
        super(Engine, self).__init__()

        self.no_selected = "Attention!\nNo record selected!"
        self.ask_to_delete = "Delete data?"
        self.ask_to_save = "Save data?"
        self.abort = "Operation aborted!"

    def __str__(self):
        return "class: {0}\nMRO:{1}".format(self.__class__.__name__,
                       [x.__name__ for x in Engine.__mro__])

    def get_python_version(self,):
        return "Python version:\n{0}".format(".".join(map(str, sys.version_info[:3])))

    def get_file(self, file):
        """# return full path of the directory where program resides."""
        return os.path.join(os.path.dirname(__file__), file)

    def open_file(self, path):
        """open file on linux and windows"""
        if os.path.exists(path):
            if os.name == 'posix':
                subprocess.call(["xdg-open", path])
            else:
                os.startfile(path)

    def on_log(self, container, function, exc_value, exc_type, module):

        now = datetime.datetime.now()
        log_text = "{0}\n{1}\n{2}\n{3}\n{4}\n\n".format(now, function, exc_value, exc_type, module)
        log_file = open("log.txt", "a")
        log_file.write(log_text)
        log_file.close()

    def get_dimensions(self):

        try:
            d = {}
            with open("dimensions", "r") as filestream:
                for line in filestream:
                    currentline = line.split(",")
                    d[currentline[0]] = currentline[1]

            return d

        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_license(self):
        """get license"""
        try:
            path = self.get_file("LICENSE")
            f = open(path, "r")
            v = f.read()
            f.close()
            return v
        except FileNotFoundError:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_icon(self, which):

        try:
            path = self.get_file(which)
            f = open(path, "r")
            v = f.readline()
            f.close()
            return v
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def get_log_file(self):

        try:
            path = self.get_file("log.txt")
            self.open_file(path)
        except FileNotFoundError:
            self.on_log(self,
                        inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

    def busy(self, caller):
        caller.config(cursor="watch")
        caller.update()

    def not_busy(self, caller):
        caller.config(cursor="")
        caller.update()

def main():
    #if you want testing some stuff
    foo = Engine()
    print(foo)
    #print(foo.set_connection())
    sql = "SELECT name FROM sqlite_master WHERE type = 'table'"
    rs = foo.read(True, sql)
    if rs:
        for i in enumerate(rs):
            table = i[1][0]
            print(i)
            sql = "SELECT COUNT(*) FROM {0}".format(table)
            print(sql)
            rs_table_rows = foo.read(False, sql)
            print("table {0} len {1}".format(table, rs_table_rows[0]))

        sql = "SELECT [CLASS] FROM {0} WHERE [CLASSTYPE]=1 GROUP BY [CLASS];".format(table)
        rs = foo.read(True, sql , ())
        for i in rs:
            print(i)

    else:
        print("Something is gone wrong!")
    foo.con.close()

    input('end')

if __name__ == "__main__":
    main()
