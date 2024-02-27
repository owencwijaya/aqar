import cv2 as cv
import numpy as np
import os
from time import time
from PIL import ImageGrab
# import win32gui, win32ui, win32con

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# def window_capture(filename=None):
#     w = 1920
#     h = 1080

#     # hwnd = win32gui.FindWindow(None, windowname)
#     hwnd = None
#     wDC = win32gui.GetWindowDC(hwnd)
#     dcObj = win32ui.CreateDCFromHandle(wDC)
#     cDC = dcObj.CreateCompatibleDC()
#     dataBitMap = win32ui.CreateBitmap()
#     dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
#     cDC.SelectObject(dataBitMap)
#     cDC.BitBlt((0, 0), (w, h), dcObj, (0, 0), win32con.SRCCOPY)

#     dataBitMap.SaveBitmapFile(cDC, 'debug.hmp')

#     dcObj.DeleteDC()
#     cDC.DeleteDC()
#     win32gui.ReleaseDC(hwnd, wDC)
#     win32gui.DeleteObject(dataBitMap.GetHandle())

loop_time = time()
while(True):

    # screenshot = pyautogui.screenshot()
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)

    cv.imshow('Computer Vision', screenshot)

    print('FPS: {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    # press 'q' to close the window
    # wait 1 ms every loop

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
    
# window_capture()

print('Program exited.')



      points = []
        if len(rectangles):

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rectangles:
                # Determine the center position
                center_x = x + int(w / 2)
                center_y = y + int(h / 2)
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # Save the points
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    # Determine the box position
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
                elif debug_mode == 'points':
                    # Draw the center point
                    cv.drawMarker(haystack_img, (center_x, center_y), 
                                color=line_color, markerType=marker_type, 
                                markerSize=40, thickness=2)
                elif debug_mode == "complete":
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, color=line_color, 
                                lineType=line_type, thickness=2)
                    # Draw the center point
                    cv.drawMarker(haystack_img, (center_x, center_y), 
                                color=line_color, markerType=marker_type, 
                                markerSize=40, thickness=2)

        if debug_mode:
            cv.imshow('PRO-KORIKA-Bot', haystack_img)

        return points