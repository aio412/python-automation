import win32api
import win32con
import win32gui
import time
VK_CODE = {
    'backspace':0x08,
    'tab':0x09,
    'clear':0x0C,
    'enter':0x0D,
    'shift':0x10,
    'ctrl':0x11,
    'alt':0x12,
    'pause':0x13,
    'caps_lock':0x14,
    'esc':0x1B,
    'spacebar':0x20,
    'page_up':0x21,
    'page_down':0x22,
    'end':0x23,
    'home':0x24,
    'left_arrow':0x25,
    'up_arrow':0x26,
    'right_arrow':0x27,
    'down_arrow':0x28,
    'select':0x29,
    'print':0x2A,
    'execute':0x2B,
    'print_screen':0x2C,
    'ins':0x2D,
    'del':0x2E,
    'help':0x2F,
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    'numpad_0':0x60,
    'numpad_1':0x61,
    'numpad_2':0x62,
    'numpad_3':0x63,
    'numpad_4':0x64,
    'numpad_5':0x65,
    'numpad_6':0x66,
    'numpad_7':0x67,
    'numpad_8':0x68,
    'numpad_9':0x69,
    'multiply_key':0x6A,
    'add_key':0x6B,
    'separator_key':0x6C,
    'subtract_key':0x6D,
    'decimal_key':0x6E,
    'pide_key':0x6F,
    'F1':0x70,
    'F2':0x71,
    'F3':0x72,
    'F4':0x73,
    'F5':0x74,
    'F6':0x75,
    'F7':0x76,
    'F8':0x77,
    'F9':0x78,
    'F10':0x79,
    'F11':0x7A,
    'F12':0x7B,
    'F13':0x7C,
    'F14':0x7D,
    'F15':0x7E,
    'F16':0x7F,
    'F17':0x80,
    'F18':0x81,
    'F19':0x82,
    'F20':0x83,
    'F21':0x84,
    'F22':0x85,
    'F23':0x86,
    'F24':0x87,
    'num_lock':0x90,
    'scroll_lock':0x91,
    'left_shift':0xA0,
    'right_shift ':0xA1,
    'left_control':0xA2,
    'right_control':0xA3,
    'left_menu':0xA4,
    'right_menu':0xA5,
    'browser_back':0xA6,
    'browser_forward':0xA7,
    'browser_refresh':0xA8,
    'browser_stop':0xA9,
    'browser_search':0xAA,
    'browser_favorites':0xAB,
    'browser_start_and_home':0xAC,
    'volume_mute':0xAD,
    'volume_Down':0xAE,
    'volume_up':0xAF,
    'next_track':0xB0,
    'previous_track':0xB1,
    'stop_media':0xB2,
    'play/pause_media':0xB3,
    'start_mail':0xB4,
    'select_media':0xB5,
    'start_application_1':0xB6,
    'start_application_2':0xB7,
    'attn_key':0xF6,
    'crsel_key':0xF7,
    'exsel_key':0xF8,
    'play_key':0xFA,
    'zoom_key':0xFB,
    'clear_key':0xFE,
    '+':0xBB,
    ',':0xBC,
    '-':0xBD,
    '.':0xBE,
    '/':0xBF,
    '`':0xC0,
    ';':0xBA,
    '[':0xDB,
    '//':0xDC,
    ']':0xDD,
    "'":0xDE,
    '`':0xC0}


def get_mouse_point():#获取鼠标位置
    return win32api.GetCursorPos()
def mouse_click(x=None,y=None):#单击（左键）
    #print(x,y)
    #传了个数组进来的话
    if  isinstance(x,tuple) or isinstance(x,list):
       a,b = x[::1]     
    else :
        a=x
        b=y
    if not a is None and not b is None:
        mouse_move(a,b)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)#按下
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)#弹起
    
def mouse_dclick(x=None,y=None):#双击
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def mouse_move(x,y):#移动鼠标
    x= int(x)
    y= int(y)
    win32api.SetCursorPos((x, y))
    
def mouse_click_move(pos1,pos2):#拖动鼠标
    mouse_move(pos1[0],pos1[1])
    time.sleep(1)#
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    mouse_move(pos2[0],pos2[1])
    time.sleep(1)#
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def put(str='',flag=0):#flag默认为0，则表示输入的字符串，为1：字符要表示的是快捷组合按键
    if flag==0:
        for c in str:
            if c == ' ':#处理空格
                win32api.keybd_event(VK_CODE['spacebar'],0,0,0)
                win32api.keybd_event(VK_CODE['spacebar'],0,win32con.KEYEVENTF_KEYUP,0)
            else:
                win32api.keybd_event(VK_CODE[c],0,0,0)
                win32api.keybd_event(VK_CODE[c],0,win32con.KEYEVENTF_KEYUP,0)
    else:
        cmd = str.split(' ')
        for i in cmd:
            win32api.keybd_event(VK_CODE[i],0,0,0)
        cmd.reverse()
        for i in cmd:#快捷键释放的时候要逆序释放
            win32api.keybd_event(VK_CODE[i],0,win32con.KEYEVENTF_KEYUP,0)
    time.sleep(1)
def click_pic(pos):#点击图片，pos=(1,2,3,4)
    # print("点击图片：")
    # print(pos)
    x= pos[0] +int( (pos[2]-pos[0]) / 2)
    y= pos[1] +int( (pos[3]-pos[1]) / 2)
    mouse_click(x,y)
def show_window_by_title(tname,toTop = 1):#获取窗口句柄并激活窗口,toTop=1窗口置顶
    app = win32gui.FindWindow(None,tname)
    rect = win32gui.GetWindowRect(app)  
    print(rect)
    w = rect[2]-rect[0]
    h = rect[3]-rect[1]
    #bottom_height = 
    if toTop == 1:
        win32gui.SetWindowPos(app,win32con.HWND_TOP,0,0,w,h,win32con.SWP_SHOWWINDOW) #有时候获取到的坐标不规范会置顶失败
    win32gui.SetForegroundWindow(app) 
    return rect
def enum_windows():#遍历并返回所有可用窗口的title
    titles =[]
    def get_visible_hwnds(hwnd,mouse):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
            titles.append(win32gui.GetWindowText(hwnd))    
    win32gui.EnumWindows(get_visible_hwnds,titles)
    return titles
   
if __name__ == "__main__":
    # mouse_dclick(1083,139)
    # put('hello      world',0)
    # put('ctrl v',1) #快捷键要用空格分开
    print(enum_windows())
    show_window_by_title("BlueStacks App Player",1)