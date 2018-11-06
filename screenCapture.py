import numpy as np
import cv2
from mss import mss
from screeninfo import get_monitors
import time
import pyautogui


#       monitor(1366x768+0+0) 
# m = str(get_monitors())
# m = m.split('x')
# W = int(m[0].split('(')[1])         #(1366) width of monitor
# H = int(m[1].split('+')[0])         #(720) height of monitor

#monitor = {'top': int(0.56640625*H), 'left': int(0.695461201*W), 'width': int(0.146412884*W), 'height': int(0.065104167*H)}

monitor = {'top': 457, 'left': 1010, 'width': 70, 'height': 30}
x1 = x2 = int(monitor['width']/2)
y1 = monitor['height']
y2 = 0

sct = mss()

last_time = time.time()

cursor_x = int(monitor['left'] + monitor['width']/2)
cursor_y = monitor['top']
# pyautogui.moveTo(cursor_x, cursor_y)
# pyautogui.click(cursor_x, cursor_y)

view_limit = 30

def convert_rgb_to_bgr(img):
    return img[:, :, ::-1]

while True:
    
    screen =  np.array(sct.grab(monitor))
    
    screen_bgr = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    screen_gray = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2GRAY)
    
    cv2.line(screen, (x1, y1), (x2, y2), (0,0,255), 2)
    cv2.line(screen, (x1+view_limit, y1), (x2+view_limit, y2), (255,0,0), 2)
    cv2.line(screen, (x1-view_limit, y1), (x2-view_limit, y2), (255,0,0), 2)

    hsv = cv2.cvtColor(screen_bgr, cv2.COLOR_BGR2HSV)

    lower_white = np.array([80,0,0], dtype=np.uint8)
    upper_white = np.array([185,255,230], dtype=np.uint8)

    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_white, upper_white)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(screen_bgr, screen_bgr, mask= mask)

    shoot = 1

    for a in res:
        for b in a:
            for c in b:
                if c != 0:
                    shoot = 0
                    break
    
    if shoot:
        pyautogui.click(cursor_x, cursor_y)
        time.sleep(0.025)
        pyautogui.click(cursor_x, cursor_y)
    
    print(shoot)

    #cv2.imshow('screen_bgr', screen_bgr)
    #cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    cv2.imshow('screen_rgb',screen)
    #cv2.imshow('gray',screen_gray)

    print('loop took {} seconds'.format(time.time() - last_time))
    last_time = time.time()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break