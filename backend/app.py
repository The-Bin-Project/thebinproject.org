from flask import Flask, request, jsonify
import cv2
import numpy as np
from pymongo import MongoClient
from skimage.metrics import structural_similarity as ssim
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS
import uuid
import os
from flask import send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import base64
from openai import OpenAI
import json

load_dotenv()
app = Flask(__name__)
CORS(app)

app.config['MAX_CONTENT_LENGTH'] = 600 * 1024 * 1024 #600 Mb Max Upload Size
mongo_uri = os.getenv('MONGO_URI')
mongo_client = MongoClient(mongo_uri)
db = mongo_client.main
users = db.users

@app.route('/check-login', methods=['POST'])
def check_login():
    # Extract credentials from request
    username = request.json.get('username')
    password = request.json.get('password')
    print(username,password)
    # Connect to your database and user collection
    # Find user in database
    # Check if user exists and password matches
    user = users.find_one({'name': username})
    print(user)
    if user and user['password'] == password:
        return jsonify({'message': 'Login successful'})                      
    else:
        return jsonify({'message': 'no'}), 401


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

def open_file (file_path):
    with open(file_path, 'rb') as image_file:
        base64_encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        # add data:image/jpeg;base64,
        base64_encoded_image = "data:image/jpeg;base64," + base64_encoded_image
        return base64_encoded_image

def open_images_base64(folder_path): 
    # go through all images in the folder and return a list of base64 encoded images
    images = []
    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)
        if os.path.isfile(image_path) and image_path.endswith('.jpg'):
            images.append(open_file(image_path))
    return images

client = OpenAI()

def analyze_image(images, question, is_url): 
    request_content = [{ "type": "text", "text": question }]

    for image in images:
        if is_url: 
            request_content.append({ "type": "image_url", "image_url": { "url": image }})
        else: 
            request_content.append({ "type": "image_url", "image_url": { "url": image }})

    response = client.chat.completions.create(
        model="gpt-4-vision-preview", 
        messages=[
            {
                "role": "user", 
                "content": request_content
            }
        ],
        max_tokens=1000,
    )

    return response.choices[0].message.content

@app.route('/test', methods=['GET'])
def test():
    results = [
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.15
			},
			{
				"name": "Chicken or Vegettable Fired Rice with Egg",
				"quantity": 0.05
			},
			{
				"name": "Beans Paruppu Usili",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.25
			},
			{
				"name": "Fish 65",
				"quantity": 0.1
			},
			{
				"name": "Beans Paruppu Usili",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.6
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.2
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.15
			},
			{
				"name": "Chicken or Vegettable Fired Rice with Egg",
				"quantity": 0.05
			},
			{
				"name": "Beans Paruppu Usili",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.7
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Sticky Asian Fish",
				"quantity": 0.1
			},
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Pizza",
				"quantity": 0.2
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.1
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Pasta",
				"quantity": 0.15
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Vegetable",
				"quantity": 0.08
			},
			{
				"name": "EMPTY",
				"quantity": 0.92
			}
		],
		[
			{
				"name": "Chicken Noodles Soup",
				"quantity": 0.07
			},
			{
				"name": "EMPTY",
				"quantity": 0.93
			}
		],
		[
			{
				"name": "Vegetable",
				"quantity": 0.1
			},
			{
				"name": "Chicken Noodles Soup",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.95
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.15
			},
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.2
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.25
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.95
			}
		],
		[
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Naan",
				"quantity": 0.05
			},
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Pizza",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.95
			}
		],
		[
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.05
			},
			{
				"name": "Pasta",
				"quantity": 0.15
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Pasta",
				"quantity": 0.15
			},
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Pasta",
				"quantity": 0.2
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "Pasta",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.05
			},
			{
				"name": "Pasta",
				"quantity": 0.15
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.1
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1.0
			}
		],
		[
			{
				"name": "Fish 65",
				"quantity": 0.05
			},
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.4
			},
			{
				"name": "Chefs Salad",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.5
			}
		],
		[
			{
				"name": "Pasta",
				"quantity": 0.2
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.15
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Brown Rice",
				"quantity": 0.1
			},
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.25
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.25
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Naan",
				"quantity": 0.1
			},
			{
				"name": "Butter Chicken",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.15
			},
			{
				"name": "Chicken",
				"quantity": 0.05
			},
			{
				"name": "Beans Paruppu Usili",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.1
			},
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.9
			},
			{
				"name": "EMPTY",
				"quantity": 0.1
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.2
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.1
			},
			{
				"name": "Fried Noodles",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.6
			}
		],
		[
			{
				"name": "Steamed Mixed Rice",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.15
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Lemon Rice",
				"quantity": 0.05
			},
			{
				"name": "Chefs Salad",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Chefs Salad",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.9
			}
		],
		[
			{
				"name": "Chefs Salad",
				"quantity": 0.1
			},
			{
				"name": "Chicken or Vegettable Fired Rice with Egg",
				"quantity": 0.1
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Chefs Salad",
				"quantity": 0.15
			},
			{
				"name": "Butter Chicken",
				"quantity": 0.05
			},
			{
				"name": "Naan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.75
			}
		],
		[
			{
				"name": "Pasta",
				"quantity": 0.15
			},
			{
				"name": "Chefs Salad",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.02
			},
			{
				"name": "Vegetable",
				"quantity": 0.03
			},
			{
				"name": "EMPTY",
				"quantity": 0.95
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Vegetable",
				"quantity": 0.02
			},
			{
				"name": "EMPTY",
				"quantity": 0.93
			}
		],
		[
			{
				"name": "Chicken Noodles Soup",
				"quantity": 0.06
			},
			{
				"name": "EMPTY",
				"quantity": 0.94
			}
		],
		[
			{
				"name": "Lemon Rice",
				"quantity": 0.1
			},
			{
				"name": "Vegetable",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.15
			},
			{
				"name": "Garlic Roasted Vegetable",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.8
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.05
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.07
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.08
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.08
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.05
			},
			{
				"name": "EMPTY",
				"quantity": 0.87
			}
		],
		[
			{
				"name": "EMPTY",
				"quantity": 1
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.06
			},
			{
				"name": "Stir fry Baby Kailan",
				"quantity": 0.1
			},
			{
				"name": "EMPTY",
				"quantity": 0.84
			}
		],
		[
			{
				"name": "Fried Noodles",
				"quantity": 0.15
			},
			{
				"name": "EMPTY",
				"quantity": 0.85
			}
		]
    ]

    results_flattened = [item for sublist in results for item in sublist]
    # add together all quantities for each dish with the same name
    results_dict = {}
    for result in results_flattened:
        name = result['name']
        if name in results_dict:
            results_dict[name] += result['quantity']
        else:
            results_dict[name] = result['quantity']

    results_flattened = []
    for name, quantity in results_dict.items():
        results_flattened.append({ 'name': name, 'quantity': round(quantity, 4) })

    # order descending by quantity
    results_flattened = sorted(results_flattened, key=lambda k: k['quantity'], reverse=True)

    # for each item in results_flattened, add a percentage by finding the sum of all quantities across all foods and dividing by that
    total_quantity = sum([result['quantity'] for result in results_flattened])
    for result in results_flattened:
        result['percentage'] = round(result['quantity'] / total_quantity, 4)

    # now, calculate another percentage but discluding the quantity from the category named "EMPTY"
    total_quantity = sum([result['quantity'] for result in results_flattened if result['name'] != 'EMPTY'])
    for result in results_flattened:
        if result['name'] != 'EMPTY':
            result['percentage_without_empty'] = round(result['quantity'] / total_quantity, 4)
        else:
            result['percentage_without_empty'] = 0

    # Change the name "EMPTY" to "Clean Plate"
    for result in results_flattened:
        if result['name'] == 'EMPTY':
            result['name'] = 'Clean Plate'

    return jsonify({ 'status': 'SUCCESS', 'message': 'Successfully classified plates', 'results_flattened': results_flattened })

@app.route('/classify_plates', methods=['GET'])
def classify_plates():
    images_base64 = open_images_base64("plates_captured")
    images_base64_split = [images_base64[i:i + 5] for i in range(0, len(images_base64), 5)]

    num_of_plates = len(images_base64)

    # print length of each batch
    for batch in images_base64_split: 
        print(len(batch))

    with open ('vision_prompt.txt', 'r') as f:
        prompt = f.read()
    
    total_results = []

    # MAX_COUNT=1
    for index, batch in enumerate(images_base64_split): 
        # if index >= MAX_COUNT: 
        #     break

        print ("PROCESSING BATCH " + str(index + 1))

        result = analyze_image(batch, prompt, False)

        first_line = result.split('\n')[0]
        if first_line != '{':
            result = "\n".join(result.split('\n')[1:-1])

        print (result)

        result_json = json.loads(result)

        plates = result_json['plates']

        for plate in plates: 
            total_results.append(plate)

    results_flattened = [item for sublist in total_results for item in sublist]
    # add together all quantities for each dish with the same name
    results_dict = {}
    for result in results_flattened:
        name = result['name']
        if name in results_dict:
            results_dict[name] += result['quantity']
        else:
            results_dict[name] = result['quantity']

    results_flattened = []
    for name, quantity in results_dict.items():
        results_flattened.append({ 'name': name, 'quantity': round(quantity, 4) })

    # order descending by quantity
    results_flattened = sorted(results_flattened, key=lambda k: k['quantity'], reverse=True)

    # for each item in results_flattened, add a percentage by finding the sum of all quantities across all foods and dividing by that
    total_quantity = sum([result['quantity'] for result in results_flattened])
    for result in results_flattened:
        result['percentage'] = round(result['quantity'] / total_quantity, 4)

    # now, calculate another percentage but discluding the quantity from the category named "EMPTY"
    total_quantity = sum([result['quantity'] for result in results_flattened if result['name'] != 'EMPTY'])
    for result in results_flattened:
        if result['name'] != 'EMPTY':
            result['percentage_without_empty'] = round(result['quantity'] / total_quantity, 4)
        else:
            result['percentage_without_empty'] = 0

    # Change the name "EMPTY" to "Clean Plate"
    for result in results_flattened:
        if result['name'] == 'EMPTY':
            result['name'] = 'Clean Plate'

    return jsonify({ 'status': 'SUCCESS', 'message': 'Successfully classified plates', 'results': total_results, 'results_flattened': results_flattened, 'num_of_plates': num_of_plates })

# TAKES results_flattened and num_of_plates
@app.route("/generate_report", methods=['POST'])
def generate_report():
    data = request.get_json()  # Get data posted as JSON
    results_flattened = data['results_flattened']
    num_of_plates = data['num_of_plates']

    with open ('report_prompt.txt', 'r') as f:
        prompt = f.read()
        prompt = prompt.replace("<<NUM_OF_PLATES>>", str(num_of_plates))
        prompt = prompt.replace("<<RESULTS_FLATTENED>>", json.dumps(results_flattened, indent=4))

    print ("PROMPT:")
    print (prompt)

    response = client.chat.completions.create(
        model="gpt-4-1106-preview", 
        messages=[
            {
                "role": "user", 
                "content": prompt
            }
        ],
        max_tokens=2000,
    )

    report = response.choices[0].message.content
    
    print (report)

    return jsonify({ 'status': 'SUCCESS', 'message': 'Successfully generated report', 'report': report })
    

if __name__ == '__main__':
    app.run(debug=True, port=3002)
