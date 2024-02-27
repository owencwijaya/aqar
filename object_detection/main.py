import cv2 as cv
from time import time
import argparse
import os

from windowcapture import MacOSWindowCapture, WindowCapture
from vision import Vision
from hsvfilter import HsvFilter

os.chdir(os.path.dirname(os.path.abspath(__file__)))
SCENE_PATH, COMPONENT_PATH = 'scene', 'component'
RESULT_PATH = 'result'

parser = argparse.ArgumentParser(description='Capture and display a specified window.')
parser.add_argument('--window_name', type=str, help='The name of the window to capture.')
parser.add_argument('--monitor', type=int, default=1, help='Pick monitor to capture.')
parser.add_argument('--border', type=int, default=1, help='Existence of border')
args = parser.parse_args()

# Window Capture Class
wincap = MacOSWindowCapture(window_name=args.window_name)
# wincap = WindowCapture(window_name=args.window_name)

# Needle Target
vision_humanoid = Vision(f'{COMPONENT_PATH}/humanoid_1.jpg')
vision_humanoid.init_control_gui()
# HSV Filter
hsv_filter = HsvFilter(0, 180, 129, 15, 229, 243, 143, 0, 67, 0)

loop_time = time()
while True:
    # Capture the window
    screenshot = wincap.get_screenshot()

    # Preprocess image
    processed_image = vision_humanoid.apply_hsv_filter(screenshot, hsv_filter)

    # Get the points
    rectangles = vision_humanoid.find(screenshot, threshold=0.35, debug_mode='complete')
    points = vision_humanoid.get_click_points(rectangles)

    # draw the detection results onto the original image
    output_image = vision_humanoid.draw_rectangles(screenshot, rectangles)
    output_image = vision_humanoid.draw_crosshairs(output_image, points)

    # display the processed image
    cv.imshow('Processed', processed_image)
    cv.imshow('Matches', output_image)

    # Calculate the FPS
    print('FPS: {}'.format(1 / (time() - loop_time)))
    loop_time = time()


    # Exit
    if cv.waitKey(1) & 0xFF == ord('q'):
        cv.destroyAllWindows()
        break

print('Program exited.')