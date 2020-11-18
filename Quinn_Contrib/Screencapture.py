import numpy as np
import cv2
from PIL import ImageGrab
import time
# from Quinn_Contrib.qkey import PressKey , W, A, S, D
import pyautogui as pgi
# NUMPY - INSTALL VERSION 1.19.3

# print('Sleep')
# time.sleep(3)
# print('Run')

# print('Press Up Arrow')
# pgi.keyDown('up')
# pgi.keyDown('ctrlleft')
# time.sleep(2)
# pgi.keyUp('up')
# pgi.keyUp('ctrlleft')
# time.sleep(2)
# pgi.keyDown('left')





# This function takes the original source and processes edges
def process_image(original_image):
    processed_image = cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY)
    processed_image = cv2.Canny(processed_image, threshold1=30,threshold2=30)
    return processed_image




while True:
    img = ImageGrab.grab(bbox=(0, 40, 800, 600)) #x, y, w, h
    img_np = np.array(img)
    frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Original Frame", frame)
    #Edge Detection Screen
    new_screen = process_image(img_np)
    cv2.imshow("Edge Detection Window",new_screen)


    if cv2.waitKey(1) & 0Xff == ord('q'):
        break
    
cv2.destroyAllWindows()