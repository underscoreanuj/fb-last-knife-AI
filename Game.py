import numpy as np
import cv2
import pyautogui
from Vision import Vision
import time

class Game:
    def __init__(self, vision):
        self.vision = vision
        self.controller = pyautogui
        self.scene = 'turn_table'

    def getScreenObjects(self, template, threshold=0.9):
        matches = self.vision.findTemplate(template, threshold=threshold)

        return np.shape(matches)[1] >= 1

    def clickObject(self, template, offset=(0,0)):
        matches = self.vision.findTemplate(template)

        x = matches[1][0] + offset[0]
        y = matches[0][0] + offset[1]

        self.controller.moveTo(x, y)
        self.controller.click()

        time.sleep(1)

    def log(self, text):
        print('[%s]:  %s' % (time.strftime('%H:%M:%S'), text))

    def run(self):
        while True:
            screen = self.vision.grabScreenshot()
            cv2.imshow('screen', screen)

#            if cv2.waitKey(33) == ord('a'):
#                self.vision.getState()
            if cv2.waitKey(33) == ord('s'):
                self.vision.getScene()
       
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def skipTable(self):
        self.controller.click(1048, 195)
    def startGame(self):
        self.controller.click(1048, 488)
    def restartGame(self):
        self.controller.click(892, 160)

    def navigate(self):
        while True:
            self.scene = self.vision.getScene()
            print(self.scene)

            if(self.scene == 'turn_table'):
                self.skipTable()
            elif(self.scene == 'menu'):
                self.startGame()
            elif(self.scene == 'game'):
                continue
            elif(self.scene == 'game_over'):
                self.restartGame()
            else:
                print('****')
        

v = Vision()
g = Game(v)
g.navigate()
