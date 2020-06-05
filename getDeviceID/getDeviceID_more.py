import os
import subprocess
import time
import re
import threading

from subprocess import Popen, PIPE
# result = Popen('curl https://ip.cn', stdout=PIPE, shell=True).stdout.read().decode()
# print(result)
# def popen(cmd):
#     try:
#         popen = subprocess.Popen(cmd, stdout=subprocess.PIPE)
#         popen.wait()
#         lines = popen.stdout.readlines()
#         return [line.decode('gbk') for line in lines]
#     except BaseException as e:
#         return -1


#获取本机ip
def get_local_ip():
    ipconfig = os.popen('ipconfig').read()
    print(ipconfig)
    str1 = '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'
    res = re.findall(str1, ipconfig)
    print('获取到的所有ip信息如下：', res)
    print('本次使用ip为:', res[0])
    return res[0][:-4]

ips = []
#获取局域网内所有ip
def get_ips(local_ip ,i):
    ip = f'{local_ip}.{i}'
    if 'TTL=' in os.popen(f'ping {ip}').read():
        print(ip)
        ips.append(ip)
        return ip

def multi_threading(local_ip):
    threads = []
    for i in range(0,256):
       t = threading.Thread(target=get_ips, args=(local_ip, i,))
       threads.append(t)
    for i in range(0,256):
       threads[i].start()
    for i in range(0, 256):
       threads[i].join()



# 连接设备
def connect_device(ip):
    # subprocess.Popen("cat test.txt")
    # res_text = os.popen(f'adb connect {ip}:5555').read()
    res_text = Popen(f'adb connect {ip}:5555', stdout=PIPE, shell=True).stdout.read().decode()
    if 'already connected to' in res_text:
        return True
    else:
        return False

# 启动getdeviceid的APP,生成文件
def start_app(ip):
    ip = ip+":5555"
    package_name = 'cn.com.imi.getdeviceid'
    activity_name = '/.MainActivity'
    file_name = 'IMI_GetDeviceID.txt'
    os.system(f'adb -s {ip} shell am start -n {package_name}{activity_name}')
    time.sleep(2)
    os.system(f'adb -s {ip} shell am force-stop {package_name}')

# 获取文件内容
def get_txt(ip):
    ip = ip + ":5555"
    # current_path = os.popen('echo %cd%').read()
    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    #读取
    device_id = os.popen(f'adb -s {ip} shell cat ./sdcard/IMI_GetDeviceID.txt').read()
    if device_id:
        device_id = device_id + ','
        print(device_id)
        print(f'echo {device_id} >>{desktop_path}\device_ids.txt')
        os.system(f'echo {device_id} >>{desktop_path}\device_ids.txt')

if __name__ == '__main__':
    local_ip = get_local_ip()
    multi_threading(local_ip)
    print(ips)
    for ip in ips:
        if connect_device(ip):
            start_app(ip)
            get_txt(ip)

    # res = connect_device('192.168.0.100')
    # print(res)