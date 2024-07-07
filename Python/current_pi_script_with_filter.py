import time
import numpy as np
import cv2
from picamera2 import Picamera2
from datetime import datetime, timedelta
import os
import boto3

keys = {}
with open ("credentials.txt", "r") as f:
    lines = f.readlines()
    for line in lines:
        key = line.split("=")[0].strip()
        value = line.split("=")[1].strip()
        keys[key] = value

s3 = boto3.client('s3', 
                  region_name='ap-southeast-1',
                  aws_access_key_id=keys['AWS_ACCESS_KEY'],
                  aws_secret_access_key=keys['AWS_SECRET_ACCESS_KEY'])

def upload_to_s3(file_path, bucket_name):
    try:
        s3.upload_file(file_path, bucket_name, os.path.basename(file_path))
        print(f"Uploaded {file_path} to {bucket_name}")
    except Exception as e:
        print(f"Failed to upload {file_path}: {str(e)}")

# Set duration (in seconds) and interval (in seconds) for the timelapse
DURATION = 60*60*2 # in seconds
INTERVAL = 0.25 # 0.25 seconds
fps = 1/INTERVAL

def filter_frame(frame, x1, y1, w1, h1):
    # crop to the first selected ROI
    roi_frame = frame[y1:y1 + h1, x1:x1 + w1]

    # Convert to grayscale for easier color thresholding
    gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # threshold for white color
    _, threshold_frame = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)

    # check if there is any white color in the frame's first ROI
    if np.any(threshold_frame == 255):
        return True
    
    return False

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

        ### New Logic   
        frame = picamera2.capture_array()
        # Set ROI Values
        x1 = 1
        y1 = 1
        w1 = 1
        h1 = 1
        if filter_frame(frame, x1, y1, w1, h1):
            picamera2.capture_file(filename)
            upload_to_s3(filename, keys['AWS_BUCKET_NAME'])

        ### 

        
        frame_num += 1
        time.sleep(interval)
        time_elapsed = time.time() - start_time
    picamera2.stop()
    picamera2.close()
    

capture_timelapse(DURATION, INTERVAL)

time.sleep(2)
os.system("sudo shutdown now -h")
time.sleep(2)