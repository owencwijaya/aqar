from mss import mss
import numpy as np
import pywinctl as pwc
# import pygetwindow as gw
import cv2 as cv


class MacOSWindowCapture:
    def __init__(self, window_name, monitor_number=1, border=1):
        # Get mandatory attributes
        # Including window, monitor ID, name
        self.npw = pwc.getWindowsWithTitle(window_name)
        self.monitor_number = monitor_number
        self.window_name = window_name
        self.border = border
        # Existence validation
        if not self.npw:
            raise Exception(f'Window not found: {window_name}')
        self.npw = self.npw[0]

        # Get window location
        # Get window size
        self.left,self.top = self.npw.rect[0], self.npw.rect[1]
        self.w,self.h = self.npw.rect[2] - self.npw.rect[0], self.npw.rect[3] - self.npw.rect[1]

        # Wrap into args
        self.monitor = {
            'top': self.top + self.border * 27,
            'left': self.left,
            'width': self.w,
            'height': self.h - self.border * 27,
            'mon': self.monitor_number,
        }
    
    def update_bbox(self):
        self.npw = pwc.getWindowsWithTitle(self.window_name)[0]
        self.left,self.top = self.npw.rect[0], self.npw.rect[1]
        self.w,self.h = self.npw.rect[2] - self.npw.rect[0], self.npw.rect[3] - self.npw.rect[1]
        self.monitor = {
            'top': self.top + self.border * 27,
            'left': self.left,
            'width': self.w,
            'height': self.h - self.border * 27,
            'mon': self.monitor_number,
        }

    def get_screenshot(self):
        # self.update_bbox()
        with mss() as sct:
            img = np.asarray(sct.grab(self.monitor))
            img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            return img