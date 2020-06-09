# 获取局域网IP为多线程，后续启动APP获取设备码为多线程
import os
import time
import logging
import threading

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from subprocess import Popen, PIPE

local_ip = ''
local_ip_segment = ''


# 获取本机ip
def get_local_ip():
    with open('cfg.txt', 'r') as f:
        cfg_list = f.readline().splitlines()
        print(cfg_list)
    global local_ip
    local_ip = cfg_list[0]
    print('本次使用ip为:', local_ip)
    global local_ip_segment
    local_ip_segment = '.'.join(cfg_list[0].split('.')[0:3])
    print(f'ip网段为{local_ip_segment}')
    return local_ip_segment


# 先定义一个列表存储同网段的所有IP
ips = []

# 通过ping命令验证ip能否ping通
import subprocess
def get_ip(local_ip_segment, i, timeout=4):
    """执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    cmd - 要执行的命令
    timeout - 最长等待时间，单位：秒
    """
    target_ip = f'{local_ip_segment}.{i}'
    print(target_ip, time.time())
    if target_ip != local_ip:
        cmd = f'ping {target_ip}'
        p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        print(cmd)
        t_beginning = time.time()
        while True:
            if p.poll() is not None:
                break
            seconds_passed = time.time() - t_beginning
            if timeout and seconds_passed > timeout:
                p.terminate()
                raise TimeoutError(f'{target_ip}未连接')
            time.sleep(0.1)
        p.wait()
        print(target_ip, time.time())
        ips.append(target_ip)
        return target_ip
        # res = p.stdout.read().decode('gbk')
        # print(res)
        # print(target_ip, time.time())
        # if 'TTL=' in res and target_ip not in ips:
        #     ips.append(target_ip)
        #     return target_ip


# 获取局域网内所有ip
def multi_threading_get_ips(local_ip_segment):
    threads = []
    print(time.time())
    with open('cfg.txt', 'r') as f:
        con = f.read().splitlines()
        start_ip, end_ip = int(con[1]), int(con[2])
    for i in range(start_ip, end_ip):
        t = threading.Thread(target=get_ip, args=(local_ip_segment, i))
        threads.append(t)
    for i in range(start_ip, end_ip):
        threads[i - start_ip].start()
    for i in range(start_ip, end_ip):
        threads[i - start_ip].join()
    print(time.time())
    return ips


# 通过adb connect命令连接设备
def connect_device(ip, timeout=2):
    """执行命令cmd，返回命令输出的内容。
    如果超时将会抛出TimeoutError异常。
    cmd - 要执行的命令
    timeout - 最长等待时间，单位：秒
    """
    cmd = f'adb connect {ip}:5555'
    p = subprocess.Popen(cmd, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    t_beginning = time.time()
    while True:
        if p.poll() is not None:
            break
        seconds_passed = time.time() - t_beginning
        if timeout and seconds_passed > timeout:
            p.terminate()
            raise TimeoutError(f'{ip}无法通过adb连接')
        time.sleep(0.1)
    p.wait()
    return True
    # res = p.stdout.read().decode('gbk')
    # if 'failed' not in res:
    #     logger.info(f'{ip}已经成功adb连接')
    #     return True


# 启动getdeviceid的APP,生成文件
def start_app(ip):
    ip = ip + ":5555"
    package_name = 'cn.com.imi.getdeviceid'
    activity_name = '/.MainActivity'
    # file_name = 'IMI_GetDeviceID.txt'
    os.system(f'adb -s {ip} shell am start -n {package_name}{activity_name}')
    logger.info(f'{ip}设备APP启动成功')
    time.sleep(2)
    # os.system(f'adb -s {ip} shell am force-stop {package_name}')
    # logger.info(f'{ip}设备APP启动停止')


get_success_num = 0

# 获取文件内容
def get_txt(ip):
    ip = ip + ":5555"
    # current_path = os.popen('echo %cd%').read()
    # 获取桌面路径
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    # 读取txt文件内容
    device_id = os.popen(f'adb -s {ip} shell cat ./sdcard/IMI_GetDeviceID.txt').read()
    # 如果txt文件有内容,则将文件内容输出到电脑桌面文件
    # set / p = % test1 % < nul >> test.txt
    if device_id:
        device_id = device_id + ','
        print(device_id)
        print(f'set /p ={device_id}<nul >>{desktop_path}\device_ids.txt')
        os.system(f'set /p ={device_id}<nul >>{desktop_path}\device_ids.txt')
        global get_success_num
        get_success_num += 1


# 关闭adb连接
def close_adb_conn(ip):
    ip = ip + ":5555"
    os.system(f'adb disconnect {ip}')

# 获取device id
def get_device_id(ip):
    try:
        close_adb_conn(ip)
        if connect_device(ip):
            start_app(ip)
            get_txt(ip)
    finally:
        close_adb_conn(ip)

# 多线程获取device id
def multi_threading_device_id(ips):
    desktop_path = os.path.join(os.path.expanduser("~"), 'Desktop')
    if f'{desktop_path}\device_ids.txt':
        with open(f'{desktop_path}\device_ids.txt', 'w') as f:
            f.truncate()
    threads = []
    for ip in ips:
        t = threading.Thread(target=get_device_id, args=(ip,))
        threads.append(t)
    for i in range(len(ips)):
        threads[i].start()
    for i in range(len(ips)):
        threads[i].join()
    print(f'本次共成功获取{get_success_num}个设备码,已存储在桌面device_ids.txt文件中')
    return True





import tkinter as tk

def show_ips(t):
    global ips
    ips = []
    t.insert('end', f'\n扫描中，请稍等。。。')
    t.update()
    local_ip_segment = get_local_ip()
    ips = multi_threading_get_ips(local_ip_segment)
    # print(time.time())
    con = f'\n本次共扫描到{len(ips)}台设备,分别是{ips}'
    t.delete('1.0', 'end')
    t.insert('end', f'\n本机ip是{local_ip}')
    t.insert('end', con)


def show_res(t):
    global get_success_num
    get_success_num = 0
    t.insert('end', f'\n\n设备码获取中，请稍等。。。')
    t.update()
    res = multi_threading_device_id(ips)
    tips = f'\n本次共成功获取{get_success_num}个设备码,已存储在桌面device_ids.txt文件中'
    t.insert('end', tips)



def show_gui():
    gui = tk.Tk()
    gui.title('机器码获取工具')
    gui.geometry('900x600+280+100')
    gui.iconbitmap('icon.ico')
    t = tk.Text(gui)
    t.pack()
    # s = tk.Scrollbar(gui)
    # s.pack()
    # s.config(command=t.yview)
    # t.config(yscrollcommand=s.set)


    # b = tk.Button(gui, text='获取本机ip', bg='lightblue', width=15, command=lambda: show_local_ip(t))
    # b.pack()
    b1 = tk.Button(gui, text='扫描设备', bg='lightblue', width=15, height=2, command=lambda: show_ips(t))
    b1.place(x=400, y=350)

    b2 = tk.Button(gui, text='获取设备码', bg='lightblue', width=15, height=2, command=lambda: show_res(t))
    b2.place(x=400, y=420)

    gui.mainloop()


if __name__ == '__main__':
    # get_device_id()
    show_gui()

    # get_local_ip()
