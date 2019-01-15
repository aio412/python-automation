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

img_exist = 'D:\Code\python\summonAuto\img\\'

def writelog(text):
    print(text)

def get_pos_dict(name=""):
    json_file = "pos960x540.json"
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
    w = int(pos[2]-pos[0])
    h = int(pos[3]-pos[1])

    l1= current_img.convert('L') 
    l2= save_img.convert('L') #转灰度图

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
    tname = u"BlueStacks App Player"
    mk.show_window_by_title(tname)

    json_file = "pos960x540.json"
    with open(json_file,'r') as load_f:
        posdict = json.load(load_f)
        pos = posdict[name]
        img = ImageGrab.grab(pos)
        img.save(name + ".png")
        writelog("save picture:%s" % name)


#自动龙十,魔力10，光10，地狱火山带狗粮
def run_by_piont(sell=0,auto=0):
    print("是否出售符文：%d"%sell)
    print("自动从邮箱补体力：%d"%auto)

    win_pic_name = "success.png"
    writelog("开始")
    #激活窗口
    tname = u"BlueStacks App Player"
    screen = mk.show_window_by_title(tname)

    turns = 0
    add_power = 0
    pos_dict = get_pos_dict()
    while True:
        #开打
        start_button_pos = pos_dict["start_button_pos"]
        if match_img("start_button_pos") <1:
            if sell == 1 and turns > 0 : #火山不点这个
                writelog("有狗粮满级了，退出")
                break
            mk.click_pic(start_button_pos)
            writelog("开始副本战斗")
            time.sleep(1)
            turns +=1
        #开自动
        auto_fight = pos_dict["auto_fight"]
        if match_img("auto_fight") < 1:
            mk.click_pic(auto_fight)
            writelog("开启自动")
            time.sleep(1)
        #胜利 
        success = pos_dict["success"]
        if match_img("success") < 11:
            
            writelog("第%d次成功" % turns)
            mk.click_pic(success)
            time.sleep(1)
            mk.click_pic(success)
            time.sleep(1)#等开宝箱动画
            mk.click_pic(success)
            time.sleep(1.5)

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
            mk.mouse_click(pos_dict["again"])            
            time.sleep(0.5)
            turns +=1
            writelog("第%d次开始" % turns)

            #体力不足
            no_power = pos_dict["no_power"]
            if match_img("no_power") < 1:
                if auto == 0:
                    writelog("没体力了，退出")
                    break
                from_gift = pos_dict["from_gift"] #选择礼物箱
                from_shop = pos_dict["from_shop"] #选择商店
                if match_img(from_gift)< 1:
                     
                    mk.click_pic(from_gift)
                    time.sleep(2)
                    get_power = pos_dict["get_power"]
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
                elif match_img(from_shop)< 1:
                    mk.click_pic(from_shop)
                    time.sleep(2)#慢点免得点到红水买了
                    #友情点
                    mk.mouse_click(fix_point(315,478))
                    time.sleep(2)

                    #点确认
                    mk.mouse_click(pos_dict["gift_confirm"])
                    time.sleep(2)

                    no_fpoint = pos_dict["no_fpoint"]
                    if match_img(no_fpoint)< 1:
                         writelog("友情点不足，退出")
                         break

                    add_power +=1
                    writelog("用友情点自动补充体力第%d次成功" % add_power)

                    #再来一次
                    mk.mouse_click(fix_point(518,540))            
                    time.sleep(1)
                    pass
                else: #没体力了退出
                    writelog("没体力了，退出")
                    break

        # else:#战斗失败
        #     writelog("战斗失败了退出")
        #     break
        time.sleep(1) #每秒1次循环

if __name__ =='__main__':

    get_img("fail")

    # tname = u"BlueStacks App Player"
    # screen = mk.show_window_by_title(tname)
    # print(match_img("success",1))



    # start_button_pos = [770, 431, 864, 456]
    # res = match_img(start_button_pos,"start_button_pos.png",1)
    # print(res)

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
