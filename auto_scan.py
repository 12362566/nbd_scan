import argparse
import json
import os
import pprint
import shutil
import  subprocess
from pathlib import Path


from scans import runr
def find_unused_nbd_devices():
    result = subprocess.run(['sudo', 'qemu-nbd', '--list'], capture_output=True, text=True)
    unused_devices = []

    for line in result.stdout.splitlines():
        if 'disconnected' in line:
            unused_devices.append(line.split(':')[0].strip())
    return unused_devices


def get_largest_partition(device):
    result = subprocess.run(['sudo', 'fdisk', '-l', device], capture_output=True, text=True)
    partitions = []
    for line in result.stdout.splitlines():
        if line.startswith(device):
            parts = line.split()
            size = int(parts[-2].replace('G', ''))  # 假设大小是 G
            partitions.append((parts[0], size))

    if partitions:
        return max(partitions, key=lambda x: x[1])
    return None
def mount_nbd(nbd_path):
    subprocess.run([ 'modprobe', 'nbd'])
    nbd_device = find_unused_nbd_devices()[0]
    subprocess.run([ 'qemu-nbd', f'--connect={nbd_device}', nbd_path])
    max_nbd_partition=get_largest_partition(nbd_device)
    subprocess.run([ 'mkdir', f'/mnt/{max_nbd_partition[0].split("/")[-1]}'])
    subprocess.run([ 'mount', max_nbd_partition[0], f'/mnt/{max_nbd_partition[0].split("/")[-1]}'])
    return f'/mnt/{max_nbd_partition[0].split("/")[-1]}'


def main(a):
    if a.nbd:
        a.input= mount_nbd(a.input)
    retdata = runr.scan_all(a.input,"./")
    # pprint.pprint(retdata)
    print("result.txt")
    open("result.txt","w").write(json.dumps(retdata))



    pass


if __name__ == '__main__':
    if os.getuid() != 0:
        print("请以root权限运行本程序")
        exit(1)
    argpser = argparse.ArgumentParser()


    argpser.add_argument("input", type=str ,default="/" , help="输出ip地址")
    argpser.add_argument("-nbd", type=bool, default=False, help="输出ip地址")
    a = argpser.parse_args()

    main(a)













