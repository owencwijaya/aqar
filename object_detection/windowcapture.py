from mss import mss
import numpy as np
import pywinctl as pwc


class MacOSWindowCapture:
    def __init__(self, window_name, monitor_number=1, border=1):
        # Get mandatory attributes
        # Including window, monitor ID, name
        self.npw = pwc.getWindowsWithTitle(window_name)
        self.monitor_number = monitor_number
        self.window_name = window_name
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
            'top': self.top + border * 27,
            'left': self.left,
            'width': self.w,
            'height': self.h - border * 27,
            'mon': self.monitor_number,
        }

    def get_screenshot(self):
        with mss() as sct:
            img = np.asarray(sct.grab(self.monitor))
            return img


class Win32WindowCapture:
    def __init__(self) -> None:
        pass
