from models import RecordPlayer

import sys
import time
def main():
    if len(sys.argv) != 2:
        print("Please provide the recording file name.")
        return


    print("Recording will play in 5 seconds. Please prepare.")
    time.sleep(5)
    print("Playing recording...")
    
    recording_name = sys.argv[1]
    player = RecordPlayer()
    player.play(recording_name)

if __name__ == "__main__":
    main()