from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
import ffmpeg
from pymongo import MongoClient
import shutil
import tempfile
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

app.config['MAX_CONTENT_LENGTH'] = 2000 * 1024 * 1024 #600 Mb Max Upload Size
# results = db["results"]
openai_key = os.getenv('OPENAI_KEY')
openai_client = OpenAI(api_key=openai_key)

# try:

mongo_uri = os.getenv('MONGO_URI')
# mongo_client = MongoClient(mongo_uri)
mongo_client = MongoClient(mongo_uri, tls=True, tlsAllowInvalidCertificates=True)
db = mongo_client["main"]
users = db["users"]
print("Connected to MongoDB cluster successfully.")

# except pymongo.errors.ConnectionFailure as e:
#     print(f"Connection failed: {e}")

def getMenu(username):
    user = users.find_one({"name": username})
    print("user", user)
    if user and 'menu' in user:
        return user['menu']
    else:
        return {
            'Monday': '',
            'Tuesday': '',
            'Wednesday': '',
            'Thursday': '',
            'Friday': ''
        }
    
@app.route('/fetch-menu', methods=['POST'])
def fetch_menu():
    username = request.json.get('username')
    menu = getMenu(username)
    return jsonify({'menu': menu})


@app.route('/update-menu', methods=['POST'])
def update_menu():
    menu = request.json.get('menu')
    username = request.json.get('username')
    print(menu, username)

    # Update the document, or insert if it doesn't exist
    result = users.update_one({"name": username}, {"$set": {"menu": menu}}, upsert=True)
    print("Matched count:", result.matched_count)
    print("Modified count:", result.modified_count)
    print("Upserted ID:", result.upserted_id)
    # test = users.find_one({"name": username})  
    # print(test)
    return jsonify({'message': 'ok'})


@app.route('/check-login', methods=['POST'])
def check_login():
    try:
        print("Received login request")
        # Extract credentials from request
        username = request.json.get('username')
        password = request.json.get('password')
        print(username, password)
        # Connect to your database and user collection
        # Find user in database
        # Check if user exists and password matches
        print("A")
        print(users)
        user = users.find_one({"name": username, "password": password})
        print("B")
        # print(user)
        
        if user:
            return jsonify({'message': 'ok'})
        else:
            return jsonify({'message': 'no'}), 401
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': 'error'}), 500



@app.route('/convert-mp4', methods=['POST'])
#write a function to conver an incoming video to mp4 format and send it back
def check_and_convert_mp4():
    if 'video' not in request.files:
        return "No file part", 400
    
    file = request.files['video']
    if file.filename == '':
        return "No selected file", 400

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            input_path = temp_file.name

        file.save(input_path)

        output_path = input_path + '_converted.mp4'
        ffmpeg.input(input_path).output(output_path).run()

        return send_file(output_path, as_attachment=True, mimetype='video/mp4')

    except Exception as e:
        return str(e), 500

    finally:
        os.remove(input_path)
        os.remove(output_path)
    
@app.route('/video-upload', methods=['POST'])
def video_upload():
    try:
        print("Received video upload request")
        # print(request.files)
        selection1 = request.form.get('selection1')
        selection2 = request.form.get('selection2')
        selection_dimensions = json.loads(selection1)
        selection_dimensions2 = json.loads(selection2)
        
        split_images_white_data = [selection_dimensions['x1'], selection_dimensions['y1'], selection_dimensions['x2'], selection_dimensions['y2']]
        split_images_white2_data = [selection_dimensions2['x1'], selection_dimensions2['y1'], selection_dimensions2['x2'], selection_dimensions2['y2']]

        print(selection1, selection2)
        file_objects = request.files.getlist('video')
        
        if not file_objects:
            print("no video part")
            return jsonify({'error': 'No video file part'}), 400
        
        # Create the 'video_saved' folder if it doesn't exist
        if not os.path.exists('video_saved'):
            os.makedirs('video_saved')
        
        for file in file_objects:
            if file.filename == '':
                print("no filename")
                continue
            
            custom_filename = "vid.mp4"
            save_path = os.path.join('video_saved', secure_filename(custom_filename))
            file.save(save_path)
        
        split_images_white(split_images_white_data, split_images_white2_data)
        deleteVideo()
        # split frames logic here
        return jsonify({'message': 'ok'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': str(e)}), 500


#write a funciton to delete all videos in the video_saved folder
def deleteVideo():
	folder = './video_saved'
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		try:
			if os.path.isfile(file_path) or os.path.islink(file_path):
				print("deleting")
				os.unlink(file_path)
		except Exception as e:
			print('Failed to delete %s. Reason: %s' % (file_path, e))
def split_images_white(selectionDimensions, selectionDimensions2):
    print ("CALLED split_images_white")

    cap = cv2.VideoCapture('./video_saved/vid.mp4')
    frame_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    # Create a subfolder with a unique name inside the plates_captured folder
    # create plates_captured folder if it doesn't exist
    if not os.path.exists('plates_captured'):
        os.makedirs('plates_captured')
        print ("MAKING plates_captured dir")
        
    subfolder_name = os.path.join('plates_captured', str(uuid.uuid4()))
    os.mkdir(subfolder_name)

    print ("Creating subfolder")

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

        print ("CHECKING np.any")
        # Check if there is any white color in the frame's first ROI
        if np.any(threshold_frame == 255):
            print ("np.any returned True")
            # Crop to the second selected ROI and save
            roi_frame_save = frame[y3:y3 + h2, x3:x3 + w2]
            # add roi_frame_save to the subfolder created
            file_path = os.path.join(subfolder_name, f'frame_{frame_count}.jpg')
            cv2.imwrite(file_path, roi_frame_save)
            print(f"Saved frame {frame_count}")

        frame_count += 3

    CheckSimilarFrames(subfolder_name)

def CheckSimilarFrames(folder_path):
    print("Checking for similar frames")
    
    # folder_path = "plates_captured"
    saved_frames = sorted([f for f in os.listdir(folder_path) if f.startswith('frame_')])
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
        threshold = 0.5

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




def get_images(directory):
    images = []

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.jpg'):
                images.append(os.path.join(root, file))

    return jsonify({'images': images})

@app.route('/get-all-images', methods=['GET'])  # Changed endpoint name
def get_all_images():
    image_directory = 'plates_captured'
    return get_images(image_directory)

@app.route('/images/<path:filename>')
def get_image(filename):
    base_directory = 'plates_captured'
    full_path = os.path.join(base_directory, filename)
    #delete the first 15 characters of full_path
    full_path = full_path[16:]
    print(f"Full Path: {full_path}")  # Add this debugging output
    directory, filename = os.path.split(full_path)  # Split the full path into directory and filename
    return send_from_directory(directory, filename)  # Use send_from_directory with directory and filename
   

    # Get the filename without the directory path
    # filename_without_directory = os.path.basename(filename)
    # print(f"Filename without directory: {filename_without_directory}")
    return send_from_directory(full_path)



@app.route("/generate_report", methods=['POST'])
def generate_report():
    data = request.get_json()  # Get data posted as JSON
    username = data['schoolName']
    groupName = data['groupName']
    user_document = users.find_one({"name": username})
    results_flattened = []
    if 'results' in user_document:
    	for result in user_document['results']:
            if groupName in result:
                results_flattened = result[groupName]
                break

    # num_of_plates is the number of files in plates_captured
    num_of_plates = len([f for f in os.listdir('plates_captured') if f.endswith('.jpg')])
    with open ('report_prompt.txt', 'r') as f:
        prompt = f.read()
        prompt = prompt.replace("<<NUM_OF_PLATES>>", str(num_of_plates))
        prompt = prompt.replace("<<RESULTS_FLATTENED>>", json.dumps(results_flattened, indent=4))

    print ("PROMPT:")
    print (prompt)

    response = openai_client.chat.completions.create(
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
    #update users with a JSON of {groupname: report} in a new feild(upsert =true) called reports
    report = {groupName: report}
    users.update_one({"name": username}, {"$push": {"reports": report}},upsert=True)
    return jsonify({ 'status': 'SUCCESS', 'message': 'Successfully generated report', 'report': report })
    

@app.route('/delete-image', methods=['POST'])
def delete_image():
    try:
        data = request.json
        filename = data['imageName']
        print(filename)
        image_path = os.path.join(filename)
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

def analyze_image(images, question, is_url): 
    request_content = [{ "type": "text", "text": question }]

    for image in images:
        if is_url: 
            request_content.append({ "type": "image_url", "image_url": { "url": image }})
        else: 
            request_content.append({ "type": "image_url", "image_url": { "url": image }})

    response = openai_client.chat.completions.create(
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

@app.route('/classify_plates', methods=['POST'])
def classify_plates():
    username = request.json.get('schoolName')
    groupName = request.json.get('groupName')

    base_folder = "plates_captured"
    total_results = []

    with open('vision_prompt.txt', 'r') as f:
        prompt = f.read()
        menu = users.find_one({"name": username})['menu']
        prompt = prompt.replace("<<SCHOOL_MENU>>", str(menu))

    for subdir, dirs, files in os.walk(base_folder):
        images_base64 = open_images_base64(subdir)
        images_base64_split = [images_base64[i:i + 5] for i in range(0, len(images_base64), 5)]
        
        for index, batch in enumerate(images_base64_split): 
            print("PROCESSING BATCH " + str(index + 1) + " IN FOLDER " + subdir)

            result = analyze_image(batch, prompt, False)

            first_line = result.split('\n')[0]
            if first_line != '{':
                result = "\n".join(result.split('\n')[1:-1])

            print(result)

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
            
    update_data = {groupName: results_flattened}
    update = {"$push": {"results": update_data}}
    users.update_one({"name": username}, update)
    test = users.find_one({"name": username})
    print(test)
	# delete plates_captured folder
    shutil.rmtree('plates_captured')
    os.mkdir('plates_captured')
            
    return jsonify({ 'status': 'SUCCESS', 'message': 'ok', 'results': total_results, 'results_flattened': results_flattened })

    



@app.route('/get-groups', methods=['POST'])
def get_groups():
    username = request.json.get('schoolName')
    print(username)
    data = users.find_one({"name": username})
    group_names = [list(group.keys())[0] for group in data['results']]
    print(group_names)
    return jsonify({'groups': group_names})


@app.route('/get-results', methods=['POST'])
def get_results():
    data = request.get_json()
    school_name = data['schoolName']
    group_name = data['groupName']
    print("INFO",school_name, group_name)
    data = users.find_one({"name": school_name})
    print(data)
    # return jsonify({'results': "hi"})
    results = [list(group.values())[0] for group in data['results'] if list(group.keys())[0] == group_name][0]
    print(results)
    return jsonify({'results': results})


if __name__ == '__main__':
    app.run(debug=False, port=3001)
