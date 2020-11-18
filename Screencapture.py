import numpy as np
import cv2 as screencap
from PIL import ImageGrab
import time
import pyautogui as pgi
# NUMPY - INSTALL VERSION 1.19.3

def game_movement(keyboard_input):
    # Value keyboard inputs  include: 
    # ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(',
    # ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
    # '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`',
    # 'a', 'b', 'c', 'd', 'e','f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    # 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~',
    # 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace',
    # 'browserback', 'browserfavorites', 'browserforward', 'browserhome',
    # 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear',
    # 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete',
    # 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10',
    # 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20',
    # 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9',
    # 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja',
    # 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail',
    # 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack',
    # 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
    # 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn',
    # 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn',
    # 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator',
    # 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab',
    # 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen',
    # 'command', 'option', 'optionleft', 'optionright']
    
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


