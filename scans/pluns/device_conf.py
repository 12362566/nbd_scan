from scans import loger
from scans.deflunt import Default_scan

class scan(Default_scan):

    def __init__(self, scan_path, out_path):
        super().__init__(scan_path, out_path)
        self.ischecked=True
        
    def run(self):

        return self.get_system_info()

    def get_system_info(self):
        files = {
            "os-re": "/etc/os-release",
            "issue": "/etc/issue",
            "hostname": "/etc/hostname",
            "hosts": "/etc/hosts",
            "users": "/etc/passwd",
            "passwords": "/etc/shadow"
        }

        retdata = {}
        for key, value in files.items():
            try:
                retdata[key] = self.read_file(f"{self.root_path}{value}")
            except FileNotFoundError as e:
                loger.logger.error(f"{key},{e}")
        login_user=[]
        user_home = []
        for i in retdata["users"].split("\n"):
            li = i.split(":")
            if li == [""]:
                continue
            # print(li)
            if li[-1] != "/usr/sbin/nologin":
                login_user.append(li[0])
                user_home.append(li[-2])
        retdata["login_user"]=login_user



        retdata["user_home"] = user_home
        return retdata

    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return f"没找到 {file_path}"
        except Exception as e:
            return f"Error reading file {file_path}: {e}"


