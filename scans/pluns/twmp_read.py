from scans.deflunt import Default_scan
from utmp import UTmpRecordType
from scans import IPLocator, loger


class scan(Default_scan):

    def __init__(self, scan_path, out_path):
        super().__init__(scan_path, out_path)
        try:
            self.wtmp=self.read_wtmp(self.root_path + "/var/log/wtmp")
            self.ischecked = True
            return
        except FileNotFoundError as e:
            loger.logger.error(e)

        self.ischecked = False


    def run(self):
        super().run()
        return_data=[["用户名","ip","ip归属地","时间"]]
        csip = IPLocator.CzIp()

        for i in self.wtmp:

            if i.type == UTmpRecordType.user_process:
                try:
                    ipgps = csip.get_addr_by_ip(i.host)
                except:
                    ipgps = "未知"
                return_data.append([i.user, i.host, ipgps, i.time.strftime("%Y-%m-%d %H:%M:%S")])
        return return_data
    def read_wtmp(self,path, utmp=None):
        wtmp_array = []
        with open(path, 'rb') as fd:
            buf = fd.read()

            for entry in utmp.read(buf):
                wtmp_array.append(entry)
            return wtmp_array