from langserve import RemoteRunnable
import argparse

from object_detection.run import read_scene
from bot.parser import RioOutputParser

parser = argparse.ArgumentParser(description='Capture and display a specified window.')
parser.add_argument('--window_name', type=str, help='The name of the window to capture.')
args = parser.parse_args()

RUNNABLE_URL = "http://localhost:8000"

'''
output format = "obj": [x, y, area, delta_x, delta_y, dist]
'''

def create_game_objects(res):
    objects = ""
    
    for obj in res.keys():
        coords = res[obj]
        for coord in coords:
            x, y, area, delta_x, delta_y, dist = coord
            print("obj: ", obj, "x: ", x, "y: ", y, "dist: ", dist, "delta_x: ", delta_x, "delta_y: ", delta_y, "area: ", area)
            objects += f"<{obj}, ({x}, {y}), {dist}>"
        
    return objects

def main():
    window_name = args.window_name or "BlueStacks App Player"
    res = read_scene(window_name)
    
    initiate_chain = RemoteRunnable(f"{RUNNABLE_URL}/initiate-chat/")
    
    game_objects = create_game_objects(res)

    chain_res = initiate_chain.invoke(input = {
        "list_of_instructions": "Shoot the fourthaq person in the scene",
        "current_game_objects": game_objects
    })
    
    actions = chain_res.split("<ACTIONS>")[-1]
    print(actions)
    
    parser = RioOutputParser(actions, window_title = window_name)
    parser.parse()
    
    
    # respond_chain = RemoteRunnable(f"${RUNNABLE_URL}/respond-chat/")
    
main()