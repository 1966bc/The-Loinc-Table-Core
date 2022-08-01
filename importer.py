# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# project:  The Loinc Table Core
# authors:  1966bc
# mailto:   [giuseppecostanzi@gmail.com]
# modify:   aestas MMXXI
# -----------------------------------------------------------------------------
import sys
import inspect
import csv
import subprocess

class Importer:
    """This class is used for csv data import 
    """

    def __str__(self):
        return "class: {0}".format(self.__class__.__name__, )


    def get_table_core(self, path):

        """This function load a LoincTableCode.csv to  populate LoincTableCode table on loinc.db database
           using subprocess library to execute sqlite's import commands.
           
        @param name: path, the file path,
        @return: CompletedProcess(args=['sqlite3', 'loinc.db', '-cmd', '.mode csv', '.import /home/bc/Documents/loinc/LoincTableCore.csv LoincTableCore'], returncode=0, stdout=b'', stderr=b'')
        @rtype: string
        """

        try:

            self.delete_table_core()

            p = subprocess.run(['sqlite3', "loinc.db", '-cmd', '.mode csv',
                                     '.import ' +  path + ' LoincTableCore'],
                                    capture_output=True)
            return p.returncode

         
                    
        except:
            self.on_log(inspect.stack()[0][3],
                        sys.exc_info()[1],
                        sys.exc_info()[0],
                        sys.modules[__name__])

   
def main():

    foo = Importer()
    path = "LoincTableCore.csv"
    foo.get_table_core(path)
    print(foo)
    input('end')

if __name__ == "__main__":
    main()
