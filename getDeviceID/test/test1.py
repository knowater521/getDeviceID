# coding=utf-8
# auther:wangc
# 2020-06-02

from tkinter import *
import hashlib
class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name

    def str_trans_to_md5(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "").encode()
        # print("src =",src)
        if src:
            try:
                myMd5 = hashlib.md5()
                myMd5.update(src)
                myMd5_Digest = myMd5.hexdigest()
                # print(myMd5_Digest)
                # 输出到界面
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, myMd5_Digest)
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "字符串转MD5失败")
            else:
                print("ERROR")  # 界面左下角会有日志框，支持动态打印，下面会提到
 #设置窗口
    def set_init_window(self):
        self.init_window_name.title("机器码获取工具")  #窗口名
        self.init_window_name.geometry('800x600+250+100')     #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name["bg"] = "pink"       #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        # self.init_window_name.attributes("-alpha",0.9)     #虚化，值越小虚化程度越高
        self.init_data_label = Label(self.init_window_name, text="待处理数据")
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果")
        self.result_data_label.grid(row=0, column=12)
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  # 原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.result_data_Text = Text(self.init_window_name, width=70, height=49)  # 处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        # # 按钮
        # # 调用内部方法 加()为直接调用
        # self.str_trans_to_md5_button = Button(self.init_window_name, text="字符串转MD5", bg="lightblue", width=10,
        #                                       command=self.str_trans_to_md5)
        # self.str_trans_to_md5_button.grid(row=1, column=11)

def gui_start():
    init_window = Tk()    #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()
    init_window.mainloop()   #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示

gui_start()