import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

# Load the vid => change this for logic
cap = cv2.VideoCapture('vid.mp4')

# Skip to the 102nd frame
cap.set(cv2.CAP_PROP_POS_FRAMES, 101)  # Frame numbers start from 0

ret, frame = cap.read()
if not ret:
    print("Failed to grab frame")
    cap.release()
    cv2.destroyAllWindows()
else:
    cv2.imshow("frame", frame)
    cv2.waitKey(0)

    # Get manual input for the first ROI
    print("Enter coordinates for the first ROI:")
    # EDIT HERE FOR CHASNGING COORDINATES
    x1 = int(input("x1: "))
    y1 = int(input("y1: "))
    w1 = int(input("width1: "))
    h1 = int(input("height1: "))

    # Draw a rectangle around the first region of interest
    cv2.rectangle(frame, (x1, y1), (x1 + w1, y1 + h1), (0, 255, 0), 2)  # Green for first ROI
    cv2.imshow("frame", frame)
    cv2.waitKey(0)

    # Get manual input for the second ROI
    print("Enter coordinates for the second ROI:")
    # EDIT HERE FOR CHASNGING COORDINATES
    x2 = int(input("x2: "))
    y2 = int(input("y2: "))
    w2 = int(input("width2: "))
    h2 = int(input("height2: "))

    # Draw a rectangle around the second region of interest
    cv2.rectangle(frame, (x2, y2), (x2 + w2, y2 + h2), (0, 0, 255), 2)  # Red for second ROI
    cv2.imshow("frame", frame)
    cv2.waitKey(0)

    # Reset to the start of the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break if no more frames or error

        frame_count += 4

        # crop to the first selected ROI
        roi_frame = frame[y1:y1 + h1, x1:x1 + w1]

        # Convert to grayscale for easier color thresholding
        gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        # threshold for white color
        _, threshold_frame = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)

        # check if there is any white color in the frame's first ROI
        if np.any(threshold_frame == 255):
            # Crop to the second selected ROI and save
            roi_frame_save = frame[y2:y2 + h2, x2:x2 + w2]
            cv2.imwrite(f'frame_{frame_count}.jpg', roi_frame_save)

# # Release the video capture and close all windows
# saved_frames = sorted([f for f in os.listdir('.') if f.startswith('frame_')])

# # Iterate through the saved frames and compare each frame to the next frame
# i = 0
# while i < len(saved_frames) - 1:
#     frame1_filename = saved_frames[i]
#     frame2_filename = saved_frames[i + 1]

#     frame1 = cv2.imread(frame1_filename, cv2.IMREAD_GRAYSCALE)
#     frame2 = cv2.imread(frame2_filename, cv2.IMREAD_GRAYSCALE)

#     if frame1 is None or frame2 is None:
#         print(f"Failed to load {frame1_filename} or {frame2_filename}")
#         i += 1
#         continue  # Skip this pair of frames and move to the next

#     # Calculate the Structural Similarity Index (SSI) between two frames
#     ssi_index, _ = ssim(frame1, frame2, full=True)

#     # Define a threshold for similarity
#     threshold = 0.57

#     # If the SSI is above the threshold, delete the second frame in the pair
#     if ssi_index > threshold:
#         print(f"Deleting {frame2_filename} as it's similar to {frame1_filename}")
#         os.remove(frame2_filename)
#     else:
#         i += 1  # Move to the next frame if they are not similar

# # Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
