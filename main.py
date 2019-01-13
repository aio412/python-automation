import tkinter as tk
import subprocess as sub
import summonAuto as sa
import cv2
import time
import PIL
from PIL import Image,ImageGrab
import math
import operator
from functools import reduce
import win32_mk as mk


img_exist = 'D:\Code\python\summonAuto\img\\'
def handle_img(pos,name):
    c_img = ImageGrab.grab(pos)
    o_img = Image.open(img_exist + name)
    
    h1=c_img.histogram()
    h2=o_img.histogram()

    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    return result
    # if name == "success.png":
    #     return result < 26
    # else:
    #     return result == 0
class Application(tk.Frame):
    def say_hi(self):
        output = "hi there, everyone!"
        self.text.insert("end", output) 
    
    def printLog(self,text):        
        self.text.insert("end", "%s\n"%text) 
        
    def do_one_iteration(self):
        msg = "记录日志%d"%self.count

        self.printLog(msg)

        # self.run
        if self.count < self.total:
            time.sleep(1)
            self.count+=1
            self.pid = root.after_idle(self.do_one_iteration)

    def stop_interation(self):
        root.after_cancel(self.pid)

    def createWidgets(self):
        self.text = tk.Text(root)
        self.text.pack()

        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})
        

        self.Run = tk.Button(self)
        self.Run["text"] = "Run",
        self.Run["command"] = self.run
        self.Run.pack({"side": "left"})

        self.loop = tk.Button(self)
        self.loop["text"] = "loop",
        self.loop["command"] = self.do_one_iteration

        self.loop.pack({"side": "left"})

        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "stop"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.stop_interation
        self.QUIT.pack({"side": "right"})        

        

    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.count = 0
        self.total = 10000
        self.pack()
        self.createWidgets()

    def run(self):
        self.printLog("...")
        #激活窗口
        tname = u"BlueStacks App Player"
        mk.show_window_by_title(tname)
        if self.count < self.total:
            self.count+=1
            self.pid = root.after_idle(self.run)
            turns = 0
            add_power = 0
            #开打
            win_pos = (720,150,892,228)
            start_button_pos = (1278,690,1438,732)
            if handle_img(start_button_pos,"start_button_pos.png") == 0:
                if handle_img(win_pos,"success.png") < 1 and turns > 0 : #火山不点这个
                    self.printLog("有狗粮满级了，退出")
                    self.stop_interation
                mk.click_pic(start_button_pos)
                time.sleep(1)
                turns +=1
            #开自动
            auto_fight = (272,860,331,913)
            if handle_img(auto_fight,"auto_fight.png")==0 or handle_img(auto_fight,"auto_fight1.png")==0:
                mk.click_pic(auto_fight)
                time.sleep(1)
            #胜利 
            
            if handle_img(win_pos,"success.png") < 26:
                
                self.printLog("第%d次成功" % turns)
                mk.click_pic(win_pos)
                time.sleep(0.5)
                mk.click_pic(win_pos)
                time.sleep(0.5)#等开宝箱动画
                mk.click_pic(win_pos)
                time.sleep(1)

                if handle_img(win_pos,"success.png") < 1:#火山卖符文
                    time.sleep(1)
                    mk.mouse_click(680,772)
                    time.sleep(0.5)
                    mk.mouse_click(670,608)
                    time.sleep(0.5)
                
                #材料
                mk.mouse_click(1085,270)
                #time.sleep(0.5)
                #厕纸，精髓
                mk.mouse_click(1085,282)
                #time.sleep(0.5)            
                #符文
                mk.mouse_click(1085,322)
                #time.sleep(0.5)
                                    
                #再来一次
                mk.mouse_click(518,540)            
                time.sleep(0.5)
                turns +=1
                self.printLog("第%d次开始" % turns)

                #体力不足
                no_power = (735,355,878,390)
                if handle_img(no_power,"no_power.png")==0:
                    if auto == 0:
                        self.printLog("没体力了，退出")
                        self.stop_interation
                    from_gift = (902,584,1016,626)#选择礼物箱
                    from_shop = (618,584,694,626)#选择商店
                    if handle_img(from_gift,"from_gift.png")==0:
                            
                        mk.click_pic(from_gift)
                        time.sleep(2)
                        get_power = (988,348,1056,386)
                        #点收取
                        mk.click_pic(get_power)
                        time.sleep(1)
                        #关闭
                        mk.mouse_click(1160,221)            
                        time.sleep(1)

                        add_power +=1
                        self.printLog("从邮箱自动补充体力第%d次成功" % add_power)

                        #再来一次
                        mk.mouse_click(518,540)            
                        time.sleep(1)
                    elif handle_img(from_shop,"from_shop.png")==0:
                        mk.click_pic(from_shop)
                        time.sleep(2)#慢点免得点到红水买了
                        #友情点
                        mk.mouse_click(315,478)
                        time.sleep(2)

                        #点确认
                        mk.mouse_click(674,600)
                        time.sleep(2)

                        no_fpoint = (670,376,904,414)
                        if handle_img(no_fpoint,"no_fpoint.png")==0:
                                self.printLog("友情点不足，退出")
                                self.stop_interation

                        add_power +=1
                        self.printLog("用友情点自动补充体力第%d次成功" % add_power)

                        #再来一次
                        mk.mouse_click(518,540)            
                        time.sleep(1)
                        pass
                    else: #没体力了退出
                        self.printLog("没体力了，退出")
                        self.stop_interation

            # else:#战斗失败
            #     self.printLog("战斗失败了退出")
            #     self.stop_interation
            time.sleep(1) #每秒1次循环
           
        

root = tk.Tk()
app = Application(master=root)
app.mainloop()
# root.destroy()