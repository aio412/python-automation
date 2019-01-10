import autopy
import win32gui,win32api,win32con
import time
import PIL
from PIL import Image,ImageGrab
import math
import operator
from functools import reduce
import win32_mk as mk
import aircv as ac
import numpy as np

img_exist = 'D:\Code\python\summonAuto\img\\'
log = ''
log_flie = 'temp.log'
window_pos = ()

def writelog(text):
    global log
    print(text)
    log += text + r"\n"

def handle_img(pos,name):
    c_img = ImageGrab.grab(pos)
    o_img = Image.open(img_exist + name)
    
    h1=c_img.histogram()
    h2=o_img.histogram()

    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    if name == "success.png":
        return result < 26
    else:
        return result == 0

def find_img(pname):
    global window_pos
    img = ImageGrab.grab(bbox=(483,225,883,525))#设置窗口大小
    img_np = np.array(img)
    cv2.imshow('img',img_np)
    #res = 


#用来补充图片的方法
def get_img():   

    # dead10_pos = (548,620,1150,724)
    
    # dragon10_pos = (548,620,1150,724)    

    # start_button_pos = (1278,690,1438,732)    

    # auto_fight = (282,860,321,913)    

    # turn3_dragon = (954,366,1072,466)
    
    # dragon_success = (720,150,892,228)
    
    # dragon_close_pos =  (1066,270,103,308)    

    # close_gift_pos = (1066,270,103,308)    

    # no_power = (735,355,878,390)    

    # from_gift = (902,584,1016,626)    

    # from_shop = (618,584,694,626)
    
    # get_power = (988,348,1056,386)    

    # mana_success = (720,150,892,228)    

    # light10_success = (720,150,892,228)    

    # fire_hell_success = (720,150,892,228)    

    # no_fpoint = (670,376,904,414) 友情点不足

     #激活窗口
    tname = u"BlueStacks App Player"
    mk.show_window_by_title(tname)

    pos = (272,860,331,913)
    name = "auto_fight1_stop.png"
    img = ImageGrab.grab(pos)
    img.save(img_exist + name)
    writelog("save picture:%s" % name)


#自动龙十,魔力10，光10，地狱火山带狗粮
def run_by_piont(mname,auto=0):
   
    win_pic_name = "success.png"
    writelog(win_pic_name)
    #exit(0)
    #激活窗口
    tname = u"BlueStacks App Player"
    mk.show_window_by_title(tname)

    turns = 0
    add_power = 0
    while True:
       
        #开打
        start_button_pos = (1278,690,1438,732)
        if handle_img(start_button_pos,"start_button_pos.png"):
            if mname == "fire_hell" and turns > 0 : #火山不点这个
                writelog("有狗粮满级了，退出")
                exit(0)
            mk.click_pic(start_button_pos)
            time.sleep(1)
            turns +=1
        #开自动
        auto_fight = (272,860,331,913)
        if handle_img(auto_fight,"auto_fight.png") or handle_img(auto_fight,"auto_fight1.png"):
            mk.click_pic(auto_fight)
            time.sleep(1)
        #胜利 
        win_pos = (720,150,892,228)
        if handle_img(win_pos,win_pic_name):
            
            writelog("第%d次成功" % turns)
            mk.click_pic(win_pos)
            time.sleep(1)
            mk.click_pic(win_pos)
            time.sleep(1)#等开宝箱动画
            mk.click_pic(win_pos)
            time.sleep(0.5)

            if mname == "fire_hell":#火山卖符文
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
            writelog("第%d次开始" % turns)

            #体力不足
            no_power = (735,355,878,390)
            if handle_img(no_power,"no_power.png"):
                if auto == 0:
                    writelog("没体力了，退出")
                    exit(0)
                from_gift = (902,584,1016,626)#选择礼物箱
                from_shop = (618,584,694,626)#选择商店
                if handle_img(from_gift,"from_gift.png"):
                     
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
                    writelog("从邮箱自动补充体力第%d次成功" % add_power)

                    #再来一次
                    mk.mouse_click(518,540)            
                    time.sleep(1)
                elif handle_img(from_shop,"from_shop.png"):
                    mk.click_pic(from_shop)
                    time.sleep(2)#慢点免得点到红水买了
                    #友情点
                    mk.mouse_click(315,478)
                    time.sleep(2)

                    #点确认
                    mk.mouse_click(674,600)
                    time.sleep(2)

                    no_fpoint = (670,376,904,414)
                    if handle_img(no_fpoint,"no_fpoint.png"):
                         writelog("友情点不足，退出")
                         exit(0)

                    add_power +=1
                    writelog("用友情点自动补充体力第%d次成功" % add_power)

                    #再来一次
                    mk.mouse_click(518,540)            
                    time.sleep(1)
                    pass
                else: #没体力了退出
                    writelog("没体力了，退出")
                    exit(0)

        # else:#战斗失败
        #     writelog("战斗失败了退出")
        #     exit(0)
        time.sleep(1) #每秒1次循环


def run_by_pic(mname,auto):
    win_pic_name = "success.png"
    writelog(win_pic_name)
    #exit(0)
    #激活窗口
    tname = u"BlueStacks App Player"
    mk.show_window_by_title(tname)

    turns = 0
    add_power = 0
    while True:
        #开打
        start_button_pos = (1278,690,1438,732)
        if handle_img(start_button_pos,"start_button_pos.png"):
            if mname == "fire_hell" and turns > 0 : #火山不点这个
                writelog("有狗粮满级了，退出")
                exit(0)
            mk.click_pic(start_button_pos)
            time.sleep(1)
            turns +=1
        #开自动
        auto_fight = (272,860,331,913)
        if handle_img(auto_fight,"auto_fight.png") or handle_img(auto_fight,"auto_fight1.png"):
            mk.click_pic(auto_fight)
            time.sleep(1)
        #胜利 
        win_pos = (720,150,892,228)
        if handle_img(win_pos,win_pic_name):
            
            writelog("第%d次成功" % turns)
            mk.click_pic(win_pos)
            time.sleep(1)
            mk.click_pic(win_pos)
            time.sleep(1)#等开宝箱动画
            mk.click_pic(win_pos)
            time.sleep(0.5)

            if mname == "fire_hell":#火山卖符文
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
            writelog("第%d次开始" % turns)

            #体力不足
            no_power = (735,355,878,390)
            if handle_img(no_power,"no_power.png"):
                if auto == 0:
                    writelog("没体力了，退出")
                    exit(0)
                from_gift = (902,584,1016,626)#选择礼物箱
                from_shop = (618,584,694,626)#选择商店
                if handle_img(from_gift,"from_gift.png"):
                     
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
                    writelog("从邮箱自动补充体力第%d次成功" % add_power)

                    #再来一次
                    mk.mouse_click(518,540)            
                    time.sleep(1)
                elif handle_img(from_shop,"from_shop.png"):
                    mk.click_pic(from_shop)
                    time.sleep(2)#慢点免得点到红水买了
                    #友情点
                    mk.mouse_click(315,478)
                    time.sleep(2)

                    #点确认
                    mk.mouse_click(674,600)
                    time.sleep(2)

                    no_fpoint = (670,376,904,414)
                    if handle_img(no_fpoint,"no_fpoint.png"):
                         writelog("友情点不足，退出")
                         exit(0)

                    add_power +=1
                    writelog("用友情点自动补充体力第%d次成功" % add_power)

                    #再来一次
                    mk.mouse_click(518,540)            
                    time.sleep(1)
                    pass
                else: #没体力了退出
                    writelog("没体力了，退出")
                    exit(0)

        # else:#战斗失败
        #     writelog("战斗失败了退出")
        #     exit(0)
        time.sleep(1) #每秒1次循环


if __name__ =='__main__':
    check_img()