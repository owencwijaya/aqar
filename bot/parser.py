
from enum import Enum
from ast import literal_eval 
import pydirectinput
import pygetwindow as gw
import keyboard as kb
import time
import threading

import win32api
import win32con

class Actions(Enum):
    DIRECTION = "DIRECTION"
    MOVE = "MOVE"
    ITEMS = "ITEMS"
    WEAPON = "WEAPON"
    NO_ACTION = "NO_ACTION"

KEY_MAP = {
    'w': 0x57,
    'a': 0x41,
    's': 0x53,
    'd': 0x44,
    'f': 0x46,
    'left': 0x25,
    'right': 0x27,
    'up': 0x26,
    'down': 0x28,
}

MOUSE_MAP = {
    'left_click': 0x0001,
    'release': 0x0002,
}

    
class RioOutputParser:
    llm_input = ""
    window_title = ""
    stop = False
    
    def __init__(self, llm_input: str, window_title = "BlueStacks App Player"):
        self.llm_input = llm_input
        self.window_title = window_title
        
    def sanitize(self, action: str):
        return action.replace("\t", "").lstrip()
    
    def is_valid(self, action: str):
        return len(action) > 0 and "description" not in action.lower()
    

    
    def focus_window(self):
        try:
            window = gw.getWindowsWithTitle(self.window_title)[0]
            if window:
                window.activate()
                win32api.Sleep(1000)
            else:
                print(f"No window found with title: {self.window_title}")
        except Exception as e:
            raise e
            
    def handle_direction(self, x: float, y: float):
        win32api.SetCursorPos((int(x), int(y)))
        print(f"DIRECTION | Moved mouse to direction ({x}, {y})")
    
    def handle_move(self, duration: float): 
        start_time = time.time()
        while time.time() - start_time < duration:
            win32api.keybd_event(KEY_MAP['w'], 0, 0, 0)  # 'w' key down
        win32api.keybd_event(KEY_MAP['w'], 0, 0x2, 0)  # 'w' key up
        print(f"MOVE | Moved forward for {duration} seconds")

    def handle_items(self, action: str):
        if (action == "PICK"):
            win32api.keybd_event(KEY_MAP['f'], 0, 0, 0)  # 'F' key down
            win32api.keybd_event(KEY_MAP['f'], 0, 0x2, 0)  # 'F' key up
        print(f"ITEMS | {action}")
        
    def handle_weapons(self, action: str):
        if (action == "SHOOT"):
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        print(f"WEAPONS | {action}")
        
    def listen_to_stop(self):
        while not self.stop:
            if (kb.is_pressed('pause')):
                self.stop = True
                break
            
        
    def parse(self):
        print("[INFO] Starting parsing...")
        stop_listener = threading.Thread(target = self.listen_to_stop)
        stop_listener.start()
        
        try:
            self.focus_window()
        except Exception as e:
            print(f"An error occurred: {e}")
            print(e)
            if ('success' in str(e)):
                print("[INFO] Window is already focused")
            else:
                self.stop = True
                return
        
        # # split lines between multiline input
        # actions = self.llm_input.splitlines()
        
        # # sanitize the inputs from tabs and whitespaces
        # actions = [self.sanitize(action) for action in actions]
        print(self.llm_input)
        actions = eval(self.llm_input)
        
        # include only valid actions
        # actions = [action for action in actions if self.is_valid(action)]
        
        # obtain action inside the brackets
        # actions = [action[action.index("<") + 1 : action.index(">")] for action in actions]
        
        if (len(actions) == 0):
            self.stop = True
            
        for i, action in enumerate(actions):
            if self.stop:
                print("[INFO] Stop signal received, finishing parsing...")
                break
            
            action_type, action_args = action[0], action [1]
            
            if action_type == Actions.DIRECTION.value:
                x, y = action_args
                self.handle_direction(x, y)
            elif action_type == Actions.MOVE.value:
                duration = float(action_args)
                self.handle_move(duration)
            elif action_type == Actions.ITEMS.value:
                action = action_args[0]
                self.handle_items(action)
            elif action_type == Actions.WEAPON.value:
                action = action_args[0]
                self.handle_weapons(action)
            else:
                print(f"Unknown action: {action_type}")
                
            if (i < len(actions) - 1):
                continue
            
            print("[INFO] Finishing parsing...")
            self.stop = True
            for _, value in KEY_MAP.items():
                win32api.keybd_event(value, 0, 0x2, 0)
        # win32api.mouse_event(MOUSE_MAP['release'], 0, 0, 0, 0)
# if __name__ == "__main__":
#     sample_input = """
#         2 <MOVE, 10>
#         Description: Go to that weapon
#         3 <ITEMS, PICK>
#         Description: Pick up that weapon
#         4 <WEAPON, SHOOT>
#         Description: Shoot
#         5 <NO_ACTION>
#         Description: End the system
#     """

#     parser = RioOutputParser(
#         llm_input = sample_input,
#         window_title = "BlueStacks App Player"
#     )
#     parser.parse()
