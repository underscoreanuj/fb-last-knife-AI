import cv2
from mss import mss
import numpy as np
from PIL import Image
import time
import os

class Vision:
    def __init__(self):
        self.static_templates = {
            'turn_table': 1,
            'menu': 4,
            'game': 3,
            'game_over': 2
        }

        self.top_pad = 133
        self.left_pad = 872
        self.width_pad = 350
        self.height_pad = 615
        self.monitor = {'top': self.top_pad, 'left': self.left_pad, 'width': self.width_pad, 'height': self.height_pad}
        self.screen = mss()
        self.frame = None

        self.num = 1

    def convertRGB2BGR(self, img):
        return img[:, :, ::-1]

    def grabScreenshot(self):
        screen = np.array(self.screen.grab(self.monitor))
        img = self.convertRGB2BGR(screen)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.frame = screen

        return img_gray

    def getState(self):
        self.grabScreenshot()
        img = Image.fromarray(self.frame)
        output = "monitor-{}.png".format(self.num)
        self.num = self.num + 1
        img.save(output)

    def getScene(self):
        self.monitor = {'top': self.top_pad, 'left': self.left_pad, 'width': self.width_pad, 'height': int(self.height_pad/5)}
        self.grabScreenshot()
        self.monitor = {'top': self.top_pad, 'left': self.left_pad, 'width': self.width_pad, 'height': self.height_pad}
        
        img_mean = int(self.frame.mean())//10
#        print(img_mean)
        
        for (k,v) in self.static_templates.items():
            if v == img_mean:
#                print(k)
                return k
        
        return None