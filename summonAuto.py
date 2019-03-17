import win32gui,win32api,win32con
import time
from PIL import Image,ImageGrab
import math
import operator
from functools import reduce
import win32_mk as mk
import aircv as ac
import numpy as np
import os
import json

img_exist = 'D:\Code\python\summonAuto\img\\'   #图片路径
json_file = "pos960x540.json"                   #配置文件
tname = u"BlueStacks App Player"                #模拟器

def writelog(text):
    print(text)

def get_pos_dict(name=""):    
    with open(json_file,'r') as load_f:
        posdict = json.load(load_f)
        if(name!=""):
            return posdict[name]
        else:
            return posdict

def match_img(name,show=0):
    pos = get_pos_dict(name)
    current_img = ImageGrab.grab(pos)
    save_img = Image.open(img_exist + name +".png")
    
    #转灰度图
    l1= current_img.convert('L') 
    l2= save_img.convert('L') 

    #把图像对象转换为直方图数据，存在list h1、h2 中
    h1= l1.histogram()
    h2= l2.histogram()

    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    '''
    sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
    operator.add(x,y)对应表达式：x+y
    这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)
    '''   
    if show ==1:
        print("%s图片比对值：%d" %(name,result))
    return result 

#用来补充图片的方法
def get_img(name):   
         #激活窗口    
    mk.show_window_by_title(tname)
    with open(json_file,'r') as load_f:
        posdict = json.load(load_f)
        pos = posdict[name]
        img = ImageGrab.grab(pos)
        img.save(name + ".png")
        writelog("save picture:%s" % name)


#自动龙十,魔力10，光10，地狱火山带狗粮
def run_by_piont(sell=0,auto=0,maxturns=999):
    print("是否出售符文：%d"%sell)
    print("自动从邮箱补体力：%d"%auto)
    print("总次数%d"%maxturns)

    
    #激活窗口
    mk.show_window_by_title(tname)
    turns = 0
    add_power = 0
    pos_dict = get_pos_dict()
    
    start = time.time()
    writelog("开始：%s"% time.ctime())
    while turns < maxturns:
 
        if match_img("start_button_pos") < 6:
            if sell == 1 and turns > 0 : #火山不点这个
                writelog("有狗粮满级了，退出")
                break
            if match_img("no_power") < 1:
                writelog("没体力了，退出")
                break
            mk.click_pic(pos_dict["start_button_pos"])
            # writelog("开始副本战斗：%s"% time.ctime())
            time.sleep(1)
        #开自动
        auto_fight = pos_dict["auto_fight"]
        if match_img("auto_fight") < 1:
            mk.click_pic(auto_fight)
            writelog("开启自动")
            time.sleep(1)

        # 失败
        if match_img("fail") < 15 :
            writelog("战斗失败")
            mk.mouse_click(pos_dict["fail_no"])            
            time.sleep(1)
            mk.mouse_click(pos_dict["again"])    
            writelog("重新开始")        

            time.sleep(1)
            mk.click_pic(pos_dict["fail"])
            time.sleep(2)
            mk.click_pic(pos_dict["start_button_pos"])
            turns +=1
            writelog("第%d次开始" % turns)
            
        #胜利 
        if match_img("success") < 11:
            success = pos_dict["success"]
            finish = time.time()
            use = (finish - start) 
            writelog("第%d次成功:%s" % (turns , time.ctime()))
            writelog("用时%.2f秒" % use)
            mk.click_pic(success)
            time.sleep(0.5)
            mk.click_pic(success)
            time.sleep(0.5)#等开宝箱动画
            mk.click_pic(success)
            time.sleep(1.5) #取决于程序响应速度

            if sell == 1:#火山卖符文
                mk.mouse_click(pos_dict["sell"])
                time.sleep(0.5)
                mk.mouse_click(pos_dict["sell_confirm"])
                time.sleep(0.5)
            
            #材料
            mk.mouse_click(pos_dict["close1"])
            #time.sleep(0.5)
            #厕纸，精髓
            mk.mouse_click(pos_dict["close2"])
            #time.sleep(0.5)            
            #符文
            mk.mouse_click(pos_dict["close3"])
            #time.sleep(0.5)
                               
            #再来一次
            time.sleep(0.5)
            mk.mouse_click(pos_dict["again"])
            time.sleep(1)
            mk.mouse_click(pos_dict["again"])
            turns +=1
            start = time.time()
            writelog("第%d次开始" % turns)

            # if match_img("start_button_pos"):
            #     mk.mouse_click(pos_dict["again"])    
            #     writelog("重新开始")   

            #体力不足
            #no_power = pos_dict["no_power"]
            if match_img("no_power") < 1:
                if auto == 0:
                    writelog("没体力了，退出")
                    break
                from_gift = pos_dict["from_gift"] #选择礼物箱
                if match_img("from_gift")< 1:
                     
                    mk.click_pic(from_gift)
                    time.sleep(2)
                    get_power = pos_dict["get_gift"]
                    #点收取
                    mk.click_pic(get_power)
                    time.sleep(1)
                    #关闭
                    mk.mouse_click(pos_dict["gift_close"])           
                    time.sleep(1)

                    add_power +=1
                    writelog("从邮箱自动补充体力第%d次成功" % add_power)

                    #再来一次
                    mk.mouse_click(pos_dict["again"])
                    time.sleep(1)
               
                                
                else: #没体力了退出
                    writelog("没体力了，退出")
                    break

       
        time.sleep(1) #每秒1次循环

if __name__ =='__main__':

    # get_img("start_button_pos")

    # tname = u"BlueStacks App Player"
    # screen = mk.show_window_by_title(tname)
    # print(match_img("fail",1))
    mk.show_window_by_title(tname)
    res = match_img("start_button_pos",1)
    print(res)

    # with open("position.json",'r') as load_f:
    #     load_dict = json.load(load_f)
    #     #print(load_dict)

    #     new_dict = {}
    #     for k,v in load_dict.items():
    #         # print(k)
    #         # print(v)
    #         # print(fix_pos(v[0],v[1],v[2],v[3]))
    #         new_dict[k] = fix_pos(v[0],v[1],v[2],v[3])
    #     print(new_dict)

    #     with open("pos960X540.json","w") as new_f:
    #         json.dump(new_dict,new_f)

    # print(time.ctime())
    # start = time.time()
    
    # time.sleep(2.3)

    # finish = time.time()
    # print("%.2f"%(finish - start)) #显示两位小数点