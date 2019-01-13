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
import os

img_exist = 'D:\Code\python\summonAuto\img\\'
win_screen = (0,0,1600,960)

def writelog(text):
    print(text)

def fix_pos(x1,y1,x2,y2):

    nw = 960/1600
    nh = 540/900  

    #原坐标系基于1600X900
    x = ( (x2-x1)/2 + x1 ) * nw
    y = ( (y2-y1)/2 + y1 - 40 ) * nh + 40 #标题栏高度   

    w = (x2-x1)/2* nw
    h = (y2-y1)/2* nh  

    #newpost = (x-w,y-h,x+w,y+h)
    #print((x-w,y-h,x+w,y+h))
    return int(x-w),int(y-h),int(x+w),int(y+h)

def fix_point(x,y):
    nw = 960/1600
    nh = 540/900
    nx = int(x*nw )
    ny = int((y-40)*nh +40) #标题栏高度
    #print("fix_point:%d,%d"%(nx,ny))
    
    return nx,ny

def match_img(pos,name):
    current_img = ImageGrab.grab(pos)
    save_img = Image.open(img_exist + name)
    w = int(pos[2]-pos[0])
    h = int(pos[3]-pos[1])
    new_img = save_img.resize((w,h), Image.ANTIALIAS)
    
    # current_img.show()
    # new_img.show()
    

    l1= current_img.convert('L') 
    l2= new_img.convert('L') #转灰度图

    #把图像对象转换为直方图数据，存在list h1、h2 中
    h1= l1.histogram()
    h2= l2.histogram()

    result = math.sqrt(reduce(operator.add,  list(map(lambda a,b: (a-b)**2, h1, h2)))/len(h1) )
    '''
    sqrt:计算平方根，reduce函数：前一次调用的结果和sequence的下一个元素传递给operator.add
    operator.add(x,y)对应表达式：x+y
    这个函数是方差的数学公式：S^2= ∑(X-Y) ^2 / (n-1)
    '''   
    #print("%s图片比对值：%d" %(name,result))
    return result

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
def run_by_piont(sell=0,auto=0):
   # global win_screen
    print("是否出售符文：%d"%sell)
    print("自动从邮箱补体力：%d"%auto)

    win_pic_name = "success.png"
    writelog("开始")
    #exit(0)
    #激活窗口
    tname = u"BlueStacks App Player"
    screen = mk.show_window_by_title(tname)
    #win_screen = screen

    turns = 0
    add_power = 0
    while True:
       
        #开打
        start_button_pos = fix_pos(1278,690,1438,732)
        if match_img(start_button_pos,"start_button_pos.png") <= 15:
            if sell == 1 and turns > 0 : #火山不点这个
                writelog("有狗粮满级了，退出")
                break
            mk.click_pic(start_button_pos)
            writelog("开始副本战斗")
            time.sleep(1)
            turns +=1
        #开自动
        auto_fight = fix_pos(272,860,331,913)
        if match_img(auto_fight,"auto_fight.png")< 8 or match_img(auto_fight,"auto_fight1.png")< 1:
            mk.click_pic(auto_fight)
            writelog("开启自动")
            time.sleep(1)
        #胜利 
        win_pos = fix_pos(720,150,892,228)
        if match_img(win_pos,win_pic_name) <= 27:
            
            writelog("第%d次成功" % turns)
            mk.click_pic(win_pos)
            time.sleep(1)
            mk.click_pic(win_pos)
            time.sleep(1)#等开宝箱动画
            mk.click_pic(win_pos)
            time.sleep(1.5)

            if sell == 1:#火山卖符文
                mk.mouse_click(fix_point(680,772))
                time.sleep(0.5)
                mk.mouse_click(fix_point(670,608))
                time.sleep(0.5)
            
            #材料
            mk.mouse_click(fix_point(1085,270))
            #time.sleep(0.5)
            #厕纸，精髓
            mk.mouse_click(fix_point(1085,282))
            #time.sleep(0.5)            
            #符文
            mk.mouse_click(fix_point(1085,322))
            #time.sleep(0.5)
                               
            #再来一次
            mk.mouse_click(fix_point(518,540))            
            time.sleep(0.5)
            turns +=1
            writelog("第%d次开始" % turns)

            #体力不足
            no_power = fix_pos(735,355,878,390)
            if match_img(no_power,"no_power.png")< 1:
                if auto == 0:
                    writelog("没体力了，退出")
                    break
                from_gift = fix_pos(902,584,1016,626)#选择礼物箱
                from_shop = fix_pos(618,584,694,626)#选择商店
                if match_img(from_gift,"from_gift.png")< 1:
                     
                    mk.click_pic(from_gift)
                    time.sleep(2)
                    get_power = fix_pos(988,348,1056,386)
                    #点收取
                    mk.click_pic(get_power)
                    time.sleep(1)
                    #关闭
                    mk.mouse_click(fix_point(1160,221))           
                    time.sleep(1)

                    add_power +=1
                    writelog("从邮箱自动补充体力第%d次成功" % add_power)

                    #再来一次
                    mk.mouse_click(fix_point(518,540))            
                    time.sleep(1)
                elif match_img(from_shop,"from_shop.png")< 1:
                    mk.click_pic(from_shop)
                    time.sleep(2)#慢点免得点到红水买了
                    #友情点
                    mk.mouse_click(fix_point(315,478))
                    time.sleep(2)

                    #点确认
                    mk.mouse_click(fix_point(674,600))
                    time.sleep(2)

                    no_fpoint = (670,376,904,414)
                    if match_img(no_fpoint,"no_fpoint.png")< 1:
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
    #check_img()
    #激活窗口
    #global win_screen
    tname = u"BlueStacks App Player"
    screen = mk.show_window_by_title(tname)
    win_screen = screen
    # win_pos = (720,150,892,228)
    # print(match_img(win_pos,"success.png"))

    #newpost = 


    start_button_pos = fix_pos(1278,690,1438,732)
    res = match_img(start_button_pos,"start_button_pos.png")
    print(res)