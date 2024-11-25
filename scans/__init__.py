import importlib
import os

from os.path import join
from pathlib import Path


from scans import deflunt
from scans.loger import logger
from importlib.util import spec_from_file_location
loaded_modules = []
module_path=Path(__file__).parent
for i in os.listdir(join(module_path,"pluns")):
        if i in["__init__.py", "__pycache__","deflunt.py"] :
            continue
        if not i.endswith(".py"):
                continue
        module_pa = join(join(module_path,"pluns"), i)


        module_name= i.split(".")[0]
        spec = spec_from_file_location(module_name, module_pa)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        loaded_modules.append(module)
        logger.info(f"成功加载模块: {module_name}")

