# coding=utf-8
# auther:wangc
# 2020-06-03

import os
import re
ipconfig = os.popen('ipconfig').read()
print(ipconfig)
reg = re.compile('IPv4 地址 . . . . . . . . . . . . : (.*)')
res = re.findall(reg, ipconfig)
print('获取到的所有ip信息如下：', res)
# print('本次使用ip为:', res[0])
# res_ip = '.'.join(res[0].split('.')[0:3])
# print(f'ip网段为{res_ip}')
