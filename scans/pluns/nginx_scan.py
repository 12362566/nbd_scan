import os
import pathlib
import shutil
import subprocess
from os.path import join
import re



from scans import deflunt
from scans.loger import logger


class scan(deflunt.Default_scan):

    def __init__(self,root_path,out_path):


        super().__init__(root_path,out_path)

        nginx_list = self.find_nginx_conf()
        if nginx_list == []:
            self.ischecked = False
            logger.error("no_nginx")
            return
        else:
            self.ischecked=True
    def run(self):
        for i in self.find_nginx_conf():
            if i in "etc/nginx/nginx.conf":
                conf_path = pathlib.Path(i)
                shutil.copy(i, self.out_path)
                logger.info(conf_path)
                nginx_conf=open(i, "r").read()
                self.parse_nginx_config(nginx_conf)
                nginx_servers = []
                foudlist = self.parse_include_directives(nginx_conf)
                for i in foudlist:
                   nginx_confs = open(join(conf_path.parent, i), "r")
                   foudlist+=self.parse_include_directives(nginx_confs)
                   nginx_servers+=self.parse_nginx_config(nginx_confs)

        return  nginx_servers




        ...

    def find_nginx_conf(self):
        result = subprocess.run(["find", self.root_path, "-name", "nginx.conf"], stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8").strip()
    def parse_nginx_config(self,config_content):
        # 匹配 server 块
        server_blocks = re.findall(r'server\s*\{([^}]*)\}', config_content, re.DOTALL)

        parsed_config = []
        for block in server_blocks:
            # 匹配 server 块内的配置项
            config_items = re.findall(r'(\w+)\s+(\S+);', block)
            parsed_config.append(dict(config_items))

        return parsed_config

    def parse_include_directives(self,config_content):
        include_pattern = re.compile(r'include\s+([^\s;]+);')
        matches = include_pattern.findall(config_content)
        return matches
