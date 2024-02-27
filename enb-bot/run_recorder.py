from models import InputRecorder
import sys
import time
def main():
    if len(sys.argv) != 2:
        print("Please provide the recording file name.")
        return

    recording_name = sys.argv[1]
    
    print("Recording will start in 5 seconds. Please prepare.")
    time.sleep(5)
    print("Starting recording, press 'Pause' to stop recording.")
    
    recorder = InputRecorder()
    recorder.start_recording()
    recorder.save_recording(recording_name)

if __name__ == "__main__":
    main()