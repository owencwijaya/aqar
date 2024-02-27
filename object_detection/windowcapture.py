from mss import mss
import numpy as np
import pywinctl as pwc
import pygetwindow as gw
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
            raise Exception('Window not found: {}'.format(window_name))
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


class WindowCapture:
    def __init__(self, window_name) -> None:
        self.npw = None
        try:
            self.npw = gw.getActiveWindows(window_name)[0]
        except IndexError:
            print(f"Window with title '{window_name}' not found.")
        self.bbox = {
            'top': self.npw.top, 
            'left': self.npw.left, 
            'width': self.npw.width, 
            'height': self.npw.height
        }
    
    def update_bbox(self):
        self.npw = gw.getWindowsWithTitle(self.npw.title)[0]
        self.bbox = {
            'top': self.npw.top, 
            'left': self.npw.left, 
            'width': self.npw.width, 
            'height': self.npw.height
        }
    
    def get_screenshot(self):
        self.update_bbox()
        with mss() as sct:
            img = np.array(sct.grab(self.bbox))
            img = cv.cvtColor(img, cv.COLOR_BGRA2BGR)
            return img
