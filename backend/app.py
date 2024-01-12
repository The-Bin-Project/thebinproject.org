from flask import Flask, request, jsonify
import cv2
import numpy as np
import base64
from skimage.metrics import structural_similarity as ssim
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS
import uuid
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 600 * 1024 * 1024 #600 Mb Max Upload Size

@app.route('/video-upload', methods=['POST'])
def video_upload():
    print("Received video upload request")
    print(request.files)
    file_objects = request.files.getlist('video')
    
    if not file_objects:
        print("no video part")
        return jsonify({'error': 'No video file part'}), 400
    
    for  file in file_objects:
        if file.filename == '':
            print("no filename")
            continue
        
        unique_id = uuid.uuid4()
        custom_filename = f"vid_{unique_id}.mp4"
        save_path = os.path.join('video_saved', secure_filename(custom_filename))
        file.save(save_path)
    
    return jsonify({'message': 'ok'})



@app.route('/split-frames', methods=['POST'])
def split_frames():
    # Accessing the JSON data sent from the frontend
    data = request.json
    selectionDimensions = data['selectionDimensions']
    selectionDimensions2 = data['selectionDimensions2']

    # Load the video
    cap = cv2.VideoCapture('./video_saved/vid.mp4')

    # Get video frame dimensions
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

#     # Process the video
    split_images_white(selectionDimensions, selectionDimensions2, frame_width, frame_height)
#     cap.release()
    return jsonify({'message': 'ok'})

def split_images_white(selectionDimensions, selectionDimensions2, frame_width, frame_height):
    cap = cv2.VideoCapture('./video_saved/vid.mp4')

    # Process the video frames
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Reached the end of the video")
            break

        x1, y1, x2, y2 = scale_and_validate_roi(selectionDimensions, frame_width, frame_height)
        w1, h1 = x2 - x1, y2 - y1
        roi_frame = frame[y1:y1 + h1, x1:x1 + w1]

        x3, y3, x4, y4 = scale_and_validate_roi(selectionDimensions2, frame_width, frame_height)
        w2, h2 = x4 - x3, y4 - y3
        roi_frame_save = frame[y3:y3 + h2, x3:x3 + w2]


 
        # Convert to grayscale for easier color thresholding
        gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        # Threshold for white color
        _, threshold_frame = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)

        # Check if there is any white color in the frame's first ROI
        if np.any(threshold_frame == 255):
            # Crop to the second selected ROI and save
            roi_frame_save = frame[y3:y3 + h2, x3:x3 + w2]
            file_path = os.path.join("plates_captured", f'frame_{frame_count}.jpg')
            cv2.imwrite(file_path, roi_frame_save)   

        frame_count += 3

    CheckSimilarFrames()

def CheckSimilarFrames():

    print("Checking for similar frames")
    folder_path = "plates_captured"
    saved_frames = sorted([f for f in os.listdir('plates_captured') if f.startswith('frame_')])
    print(f"Found {len(saved_frames)} saved frames")
    print(saved_frames)
    i = 0
    while i < len(saved_frames) - 1:
        print(f"Checking frames {saved_frames[i]} and {saved_frames[i + 1]}")
        frame1_filename = saved_frames[i]
        frame2_filename = saved_frames[i + 1]
        full_frame1_path = os.path.join(folder_path, frame1_filename)
        full_frame2_path = os.path.join(folder_path, frame2_filename)
        print(full_frame1_path)

# Now read the images with the full paths
        frame1 = cv2.imread(full_frame1_path, cv2.IMREAD_GRAYSCALE)
        frame2 = cv2.imread(full_frame2_path, cv2.IMREAD_GRAYSCALE)
    

        if frame1 is None or frame2 is None:
            print("no")
            # print(f"Failed to load {frame1_filename} or {frame2_filename}")
            i += 1
            continue  # Skip this pair of frames and move to the next


        # Calculate the Structural Similarity Index (SSI) between two frames
        ssi_index, _ = ssim(frame1, frame2, full=True)

        # Define a threshold for similarity
        threshold = 0.55

        # If the SSI is above the threshold, delete the second frame in the pair
        if ssi_index > threshold:
            print(f"Deleting {frame2_filename} as it's similar to {frame1_filename}")
            os.remove(full_frame2_path)
        else:
            i += 1  # Move to the next frame if they are not similar


def scale_and_validate_roi(roi, frame_width, frame_height):
    # Example scaling and validation
    x1, y1, x2, y2 = roi
    x1, x2 = scale_coordinate(x1, x2, frame_width)
    y1, y2 = scale_coordinate(y1, y2, frame_height)
    return max(0, x1), max(0, y1), min(frame_width, x2), min(frame_height, y2)

def scale_coordinate(c1, c2, max_val):
    # Scale coordinates if necessary
    return int(c1), int(c2)

@app.route('/images/<filename>')
def get_image(filename):
    return send_from_directory('plates_captured', filename)

@app.route('/get-images', methods=['GET'])
def get_images():
    image_directory = 'plates_captured'
    images = [f for f in os.listdir(image_directory) if f.endswith('.jpg')]
    return jsonify({'images': images})



@app.route('/delete-image/<filename>', methods=['DELETE'])
def delete_image(filename):
    try:
        image_path = os.path.join('plates_captured', filename)
        if os.path.exists(image_path):
            os.remove(image_path)
            return jsonify({'message': 'Image deleted'}), 200
        else:
            return jsonify({'error': 'Image not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
