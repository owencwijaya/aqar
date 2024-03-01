
from enum import Enum
from ast import literal_eval 
import pyautogui
import pydirectinput
import pygetwindow as gw
import keyboard as kb
import time
import threading

class Actions(Enum):
    DIRECTION = "DIRECTION"
    MOVE = "MOVE"
    ITEMS = "ITEMS"
    WEAPON = "WEAPON"
    NO_ACTION = "NO_ACTION"
    
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
                pyautogui.sleep(1)
            else:
                print(f"No window found with title: {self.window_title}")
        except Exception as e:
            raise e
            
    def handle_direction(self, x: float, y: float):
        pyautogui.move(x, y)
        print(f"DIRECTION | Moved mouse to direction ({x}, {y})")
    
    def handle_move(self, duration: int): 
        start_time = time.time()
        while time.time() - start_time < duration:
            pyautogui.keyDown('w')
        pyautogui.keyUp('w')
        print(f"MOVE | Moved forwards for {duration} seconds")

    def handle_items(self, action: str):
        if (action == "PICK"):
            pyautogui.keyDown('F')
            pyautogui.keyUp('F')
        print(f"ITEMS | {action}")
        
    def handle_weapons(self, action: str):
        if (action == "SHOOT"):
            pyautogui.click(button = 'left', clicks = 10, interval = 0.25)
        print(f"WEAPONS | {action}")
        
    def listen_to_stop(self):
        while not self.stop:
            if (kb.is_pressed('pause')):
                self.stop = True
                break
            
        
    def parse(self):
        stop_listener = threading.Thread(target = self.listen_to_stop)
        stop_listener.start()

        try:
            self.focus_window()
        except Exception as e:
            print(f"An error occurred: {e}")
            return
        
        # split lines between multiline input
        actions = self.llm_input.splitlines()
        
        # sanitize the inputs from tabs and whitespaces
        actions = [self.sanitize(action) for action in actions]
        
        # include only valid actions
        actions = [action for action in actions if self.is_valid(action)]
        
        # obtain action inside the brackets
        actions = [action[action.index("<") + 1 : action.index(">")] for action in actions]
        
        for action in actions:
            if self.stop:
                print("[INFO] Stop signal received, finishing parsing...")
                break
            
            action_type, *action_args = action.split(", ", 1)
            
            if action_type == Actions.DIRECTION.value:
                x, y = literal_eval(action_args[0]) 
                self.handle_direction(x, y)
            elif action_type == Actions.MOVE.value:
                duration = int(action_args[0])
                self.handle_move(duration)
            elif action_type == Actions.ITEMS.value:
                action = action_args[0]
                self.handle_items(action)
            elif action_type == Actions.WEAPON.value:
                action = action_args[0]
                self.handle_weapons(action)
            elif action_type == Actions.NO_ACTION.value:
                print("[INFO] NO_ACTION received, finishing parsing...")
                break
            else:
                print(f"Unknown action: {action_type}")
        
if __name__ == "__main__":
    sample_input = """
        1 <DIRECTION, (0.3, 0.2)>
        Description: Look for any weapon laying in the ground
        2 <MOVE, 10>
        Description: Go to that weapon
        3 <ITEMS, PICK>
        Description: Pick up that weapon
        4 <WEAPON, SHOOT>
        Description: Shoot
        5 <NO_ACTION>
        Description: End the system
    """

    parser = RioOutputParser(
        llm_input = sample_input,
        window_title = "Gameloop(64beta)"
    )
    parser.parse()
    