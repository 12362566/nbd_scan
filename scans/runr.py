import importlib
import inspect
import os

from os.path import join
from pathlib import Path
import scans
from scans import logger

# from scans import , logger


ok_module_list=[]
return_data = {}


def scan_all(scan_path,out_path):

    for i in scans.loaded_modules:
       # try :

           scan = i.scan(scan_path,out_path)

           if scan.ischecked ==False:
               logger.error(f"{i.__name__}    scan failed")
               continue
           rdata = scan.run()
           return_data[i.__name__]=rdata

       # except Exception as e:
       #    logger.error(e)
       #    ...
    return return_data
def get_loads_name():
    return [i.__name__ for i in scans.loaded_modules]
