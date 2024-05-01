import argparse
import os
from object_detection.windowcapture import MacOSWindowCapture
from time import time
from collections import defaultdict 
from ultralytics import YOLO

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"


parser = argparse.ArgumentParser(description='Capture and display a specified window.')
parser.add_argument('--window_name', type=str, help='The name of the window to capture.')
parser.add_argument('--monitor', type=int, default=1, help='Pick monitor to capture.')
parser.add_argument('--border', type=int, default=1, help='Existence of border')
args = parser.parse_args()

def detect_scene(wincap, model):
    d = {0: 'bench', 1: 'bush', 2: 'car', 3: 'door', 4: 'person', 5: 'target'}
    
    screenshot = wincap.get_screenshot()
    objs = model(screenshot, save=False)[0]
    res = defaultdict(list)
    
    print(wincap.left, wincap.top, wincap.w, wincap.h)
    
    res['player'] = [[wincap.w / 2, wincap.h / 2, 0, 0, 0, 0]]

    for obj in objs:
        x,y,w,h = obj.boxes.xywh[0]
        c_x, c_y = float(x + w/2), float(y + h/2)
        area = float(w*h)
        delta_x, delta_y = float(c_x - wincap.w//2), float(c_y - wincap.h//2)
        dist = float((delta_x**2 + delta_y**2)**0.5)

        cls = int(obj.boxes.cls[0])

        res[d[cls]].append([c_x, c_y, area, delta_x, delta_y, dist])
        

    return res


def read_scene(window_name: str = "BlueStacks App Player"):
    model = YOLO('object_detection/yolov8-25.pt')
    wincap = MacOSWindowCapture(window_name=window_name)
    return detect_scene(wincap, model)

# read_scene()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Capture and display a specified window.')
    parser.add_argument('--window_name', type=str, help='The name of the window to capture.')
    parser.add_argument('--monitor', type=int, default=1, help='Pick monitor to capture.')
    parser.add_argument('--border', type=int, default=1, help='Existence of border')
    args = parser.parse_args()

    model = YOLO('yolov8-25.pt')
    wincap = MacOSWindowCapture(window_name=args.window_name)

    loop_time = time()
    while True:

        screenshot = wincap.get_screenshot()
        scene = detect_scene(screenshot, model)

        print(scene)
        print('FPS {}'.format(1 / (time() - loop_time)))

        loop_time = time()

