import time
from picamera2 import Picamera2
from datetime import datetime, timedelta
import os

# Set duration (in seconds) and interval (in seconds) for the timelapse
DURATION = 60*60*2 # in seconds
INTERVAL = 0.25 # 0.25 seconds
fps = 1/INTERVAL


# Function to capture timelapse
def capture_timelapse(duration, interval):
    picamera2 = Picamera2()

    camera_config = picamera2.create_still_configuration()
    camera_config["main"]["size"] = (2592, 1944)
    picamera2.configure(camera_config)
    
    picamera2.start()
    
    today = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder_path = f"/home/thebinproject/Desktop/{today}"
    os.makedirs(folder_path, exist_ok=True)
    
    start_time = time.time()
    time_elapsed = 0
    frame_num = 1
    while (time_elapsed) < duration:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"{folder_path}/image_{timestamp}_{frame_num}.jpg"
        picamera2.capture_file(filename)
        #print(f"Captured {filename}")
        frame_num += 1
        time.sleep(interval)
        time_elapsed = time.time() - start_time
    picamera2.stop()
    picamera2.close()
    

capture_timelapse(DURATION, INTERVAL)

time.sleep(2)
os.system("sudo shutdown now -h")
time.sleep(2)
