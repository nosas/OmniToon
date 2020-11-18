import numpy as np
import cv2 as screencap
from PIL import ImageGrab
import time
import pyautogui as pgi
# NUMPY - INSTALL VERSION 1.19.3

def game_movement(keyboard_input):
    # Simulates a keypress
    # Delay between press and release
    # Simulates release of keypress
    pgi.keyDown(keyboard_input)
    time.sleep(0.5)
    pgi.keyUp(keyboard_input)

# This function takes the original source and processes edges
def process_image(original_image):
    # Changes the ouput from colour to edge detection
    processed_image = screencap.cvtColor(original_image,screencap.COLOR_BGR2GRAY)
    processed_image = screencap.Canny(processed_image, threshold1=30,threshold2=30)
    return processed_image


while True:
    # Displays screen within bbox params
    screencapture_window = ImageGrab.grab(bbox=(0, 40, 800, 600)) #x, y, w, h
    screencapture_array = np.array(screencapture_window)
    output_screen = screencap.cvtColor(screencapture_array, screencap.COLOR_BGR2GRAY)
    screencap.imshow("Coloured Display Ouput Window", output_screen)
    
    #Edge Detection Screen
    #Runs the function process_image which converts original coloured output to edge detection
    edge_detection_output = process_image(screencapture_array)
    screencap.imshow("Edge Detection Ouput Window",edge_detection_output)

    # While in this window game_movement focuses in the range of bbox
    game_movement('up')
    game_movement('down')

    # Screen exits when q or the equivilant of q is pressed
    if screencap.waitKey(1) & 0Xff == ord('q'):
        break
    
screencap.destroyAllWindows()


