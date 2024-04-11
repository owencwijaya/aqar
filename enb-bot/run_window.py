import cv2
import numpy as np
import pygetwindow as gw
from mss import mss
import pyautogui

from time import time

window_title = "BlueStacks X"
cv2.namedWindow("Image")

loop_time = time()
with mss() as sct:
    while True:
        try:
            win = gw.getWindowsWithTitle(window_title)[0]
        except IndexError:
            print(f"Window with title '{window_title}' not found.")
            break
        

        bbox = {'top': win.top, 'left': win.left, 'width': win.width, 'height': win.height}
            
        img = np.array(sct.grab(bbox))
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        
        cv2.imshow("Image", img)
        
        print(f'FPS: {1 / (time() - loop_time)}')
        loop_time = time()
        
        k = cv2.waitKey(1) & 0xFF
        if k == 27:
            break

cv2.destroyAllWindows()