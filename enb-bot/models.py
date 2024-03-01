import pyautogui
import keyboard as kb
import threading
import pydirectinput
import pygetwindow as gw
import json
import time
import os

from pynput import mouse, keyboard

PYNPUT_SPECIAL_CASE_MAP = {
    'alt_l': 'altleft',
    'alt_r': 'altright',
    'alt_gr': 'altright',
    'caps_lock': 'capslock',
    'ctrl_l': 'ctrlleft',
    'ctrl_r': 'ctrlright',
    'page_down': 'pagedown',
    'page_up': 'pageup',
    'shift_l': 'shiftleft',
    'shift_r': 'shiftright',
    'num_lock': 'numlock',
    'print_screen': 'printscreen',
    'scroll_lock': 'scrolllock',
}
    

class RecordPlayer():
    stop = False
    window_title = ""
    
    def __init__(self, window_title = "BlueStacks App Player"):
        self.window_title = window_title
    
    def convert_key_to_pyautogui(self, button):
        cleaned_key = button.replace('Key.', '')
        
        if (cleaned_key in PYNPUT_SPECIAL_CASE_MAP):
            return PYNPUT_SPECIAL_CASE_MAP[cleaned_key]
        
        return cleaned_key
    
    def listen_to_esc(self):
        while not self.stop:
            if (kb.is_pressed('pause')):
                self.stop = True
                break
            
    def focus_window(self):
        try:
            window = gw.getWindowsWithTitle(self.window_title)[0]
            if window:
                window.activate()
                pyautogui.sleep(1)
            else:
                print(f"No window found with title: {self.window_title}")
        except Exception as e:
            print(f"An error occurred: {e}")
                
    def play(self, filename):
        self.focus_window()
        pydirectinput.PAUSE = 0
        # pyautogui.PAUSE = 0
        stop_listener = threading.Thread(target = self.listen_to_esc)
        stop_listener.start()
        
        script_dir = os.path.dirname(__file__)
        filepath = os.path.join(script_dir, 'recordings', f'{filename}.json')
        beginning_time = time.time()
        with open(filepath, 'r') as input:
            events = json.load(input)
            
            for idx, event in enumerate(events):
                start_time = time.time()
                
                print(time.time() - beginning_time, idx)

                if event['button'] == 'Key.pause':
                    self.stop = True
                
                if self.stop:
                    break
                
                if event['type'] == 'keyDown':
                    key = self.convert_key_to_pyautogui(event['button'])
                    pyautogui.keyDown(key)
                    print(f'keyDown | {key}')
                elif event['type'] == 'keyUp':
                    key = self.convert_key_to_pyautogui(event['button'])
                    pyautogui.keyUp(key)
                    print(f'keyUp | {key}')
                elif event['type'] == 'click':
                    x, y = event['pos']
                    print(event['button'].split(".")[1])
                    pyautogui.click(x, y, duration = 0.25, button = event['button'].split(".")[1])
                    print(f'click | {x}, {y}')
                elif event['type'] == 'move':
                    x, y = event['pos']
                    pydirectinput.moveTo(x, y, duration = 0)
                    print(f'move | {x}, {y}')
                    
                
                if (event['type'] == 'move'):
                    continue
                    
                try:
                    next_event = events[idx + 1]
                except IndexError:
                    print('Reached end of recording!')
                    break
                
            
                elapsed_time = next_event['time'] - event['time']
                
                if (elapsed_time) < 0:
                    raise Exception('Wrong event ordering!')
                
                elapsed_time -= (time.time() - start_time)
                elapsed_time = max(elapsed_time, 0)
                time.sleep(elapsed_time)
                    
                


class EventType():
    KEY_DOWN = 'keyDown'
    KEY_UP = 'keyUp'
    CLICK = 'click'
    MOVE = 'move'
    
class InputRecorder():
    window_title = ""
    mouse_listener = None
    start_time = None
    pressed_keys = []
    input_events = []
    move_idx = 0
    recorded_move_idx = 0
    
    def __init__(self, window_title = "BlueStacks App Player"):
        self.window_title = window_title
        
    def is_window_active(self):
        try:
            return gw.getActiveWindowTitle() == self.window_title
        except Exception:
            return False
    
    '''
    append an event to the list of input events
    and log the event to the console
    '''
    def record_event(self, event_type, event_time, button, pos = None):

        
        self.input_events.append({
            'time': event_time,
            'type': event_type,
            'button': str(button),
            'pos': pos
        })
        
        if (event_type == EventType.CLICK):
            print(f'{event_type} | Clicked {button} on {pos} at {event_time}')
        elif (event_type == EventType.MOVE):
            print(f'{event_type} | Moved to {pos} at {event_time}')
        else:
            print(f'{event_type} | Pressed {button} at {event_time}')
            
    
    def elapsed_time(self):
        return time.time() - self.start_time
    
    '''
    listener function on keyboard press
    '''
    def keyboard_on_press(self, key):
        if (self.is_window_active() == False):
            print("Window is not active, skipping action...")
            return
        
        if key not in self.pressed_keys:
            self.pressed_keys.append(key)
            
        try:
            self.record_event(EventType.KEY_DOWN, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(EventType.KEY_DOWN, self.elapsed_time(), key)
            
    
    '''
    listener function on keyboard release
    - remove key from list of pressed keys
    - raise exception if pressed key is ESC
    '''
    def keyboard_on_release(self, key):
        if (self.is_window_active() == False):
            print("Window is not active, skipping action...")
            return
        
        try:
            self.pressed_keys.remove(key)
        except ValueError:
            print(f'ERROR | Key {key} not found in pressed keys!')      
            
        try:
            self.record_event(EventType.KEY_UP, self.elapsed_time(), key.char)
        except AttributeError:
            self.record_event(EventType.KEY_UP, self.elapsed_time(), key)
            
        
        if (key == keyboard.Key.pause):
            self.mouse_listener.stop()
            raise keyboard.Listener.StopException
        
    
    '''
    listener function on mouse click
    - simply adds a new event
    '''
    def mouse_on_click(self, x, y, button, pressed):
        if (self.is_window_active() == False):
            print("Window is not active, skipping action...")
            return
        
        if not pressed:
            self.record_event(EventType.CLICK, self.elapsed_time(), button, (x, y))
        
            
    def mouse_on_move(self, x, y):
        if (self.is_window_active() == False):
            print("Window is not active, skipping action...")
            return
        
        if (len(self.input_events) == 0):
            return
        
        self.record_event(EventType.MOVE, self.elapsed_time(), None, (x, y))

    '''
    function to start recording, starting mouse and keyboard listeners
    '''
    def start_recording(self):
        # init mouse listener before keyboard listener in the background,
        # so it wouldn't block the keyboard listener
        self.mouse_listener = mouse.Listener(
            on_click = self.mouse_on_click,
            on_move = self.mouse_on_move
        )
        
        self.mouse_listener.start()
        self.mouse_listener.wait()
        
        with keyboard.Listener(
            on_press = self.keyboard_on_press,
            on_release = self.keyboard_on_release
        ) as keyboard_listener:
            self.start_time = time.time()
            keyboard_listener.join()
        
    def save_recording(self, file_name):
        script_dir = os.path.dirname(__file__)
        filepath = os.path.join(
            script_dir, 'recordings', f'{file_name}.json'
        )
        
        with open(filepath, 'w') as output:
            json.dump(self.input_events, output, indent=4)
        