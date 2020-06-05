# 获取局域网IP为多线程，后续启动APP获取设备码为单线程
import os
import time
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from subprocess import Popen, PIPE

#获取本机ip
def get_local_ip():
    ipconfig = os.popen('ipconfig').read()
    print(ipconfig)
    str1 = '[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}'
    res = re.findall(str1, ipconfig)
    print('获取到的所有ip信息如下：', res)
    print('本次使用ip为:', res[0])
    res_ip = '.'.join(res[0].split('.')[0:3])
    print(f'ip网段为{res_ip}')
    return res_ip

ips = []
#获取局域网内所有ip
def get_ips(local_ip ,i):
    ip = f'{local_ip}.{i}'
    # print(ip)
    if 'TTL=' in os.popen(f'ping {ip}').read():
        print(ip)
        ips.append(ip)
        return ip
    else:
        print(f'{ip}未连接')


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
    print(res_text)
    if 'failed' not in res_text:
        logger.info(f'{ip}已经成功adb连接')
        return True
    else:
        logger.info(f'{ip}无法通过adb连接')
        return False

# 启动getdeviceid的APP,生成文件
def start_app(ip):
    ip = ip+":5555"
    package_name = 'cn.com.imi.getdeviceid'
    activity_name = '/.MainActivity'
    # file_name = 'IMI_GetDeviceID.txt'
    os.system(f'adb -s {ip} shell am start -n {package_name}{activity_name}')
    logger.info(f'{ip}设备APP启动成功')
    time.sleep(2)
    os.system(f'adb -s {ip} shell am force-stop {package_name}')
    logger.info(f'{ip}设备APP启动停止')

# 获取文件内容
def get_txt(ip):
    ip = ip + ":5555"
    # current_path = os.popen('echo %cd%').read()
    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    #读取txt文件内容
    device_id = os.popen(f'adb -s {ip} shell cat ./sdcard/IMI_GetDeviceID.txt').read()
    #如果txt文件有内容,则将文件内容输出到电脑桌面文件
    if device_id:
        device_id = device_id + ','
        print(device_id)
        print(f'echo {device_id} >>{desktop_path}\device_ids.txt')
        os.system(f'echo {device_id} >>{desktop_path}\device_ids.txt')
# 关闭adb连接
def close_adb_conn(ip):
    ip = ip + ":5555"
    os.system(f'adb disconnect {ip}')


def get_device_id():
    local_ip = get_local_ip()
    multi_threading(local_ip)
    print(ips)
    for ip in ips:
        try:
            close_adb_conn(ip)
            if connect_device(ip):
                start_app(ip)
                get_txt(ip)
        finally:
            close_adb_conn(ip)

from tkinter import *
def gui():


    gui = Tk()
    lbl = Label(gui, text="Hello")
    lbl.grid(column=0, row=0)

    gui.title('机器码获取工具')
    gui.geometry('800x600+280+100')
    get_local_ip_btn = Button(gui,text='获取本机ip',bg='lightblue',width=10,command=get_device_id)
    get_local_ip_btn.grid(row=1, column=3)

    # btn_area = Text(gui, width='50', height='50')
    # btn_area.grid(row=2, column=10)

    gui.mainloop()

if __name__ == '__main__':
    # get_device_id()
    gui()