import cv2
import numpy as np
import os
from skimage.metrics import structural_similarity as ssim

def select_roi(event, x, y, flags, param):
    global refPt, cropping, frame, roi_selected

    if event == cv2.EVENT_LBUTTONDOWN:
        if not roi_selected:  # If first ROI is not selected yet
            refPt = [(x, y)]
            cropping = True

    elif event == cv2.EVENT_LBUTTONUP:
        if not roi_selected:
            refPt.append((x, y))
            cropping = False

            # draw a rectangle around the first region of interest
            cv2.rectangle(frame, refPt[0], refPt[1], (0, 255, 0), 2)  # Green for first ROI
            cv2.imshow("frame", frame)

# Initialize variables
cropping = False
refPt = []
roi_selected = False

# Load the video
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
    cv2.setMouseCallback("frame", select_roi)

    # First ROI selection
    while not roi_selected:
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            frame = frame.copy()

        elif key == ord("c"):
            roi_selected = True

    # Update the coordinates for the first ROI
    y1, h1, w1, x1 = refPt[0][1], refPt[1][1] - refPt[0][1], refPt[1][0] - refPt[0][0], refPt[0][0]

    # Second ROI selection
    refPt = []  # Reset refPt for second ROI
    roi_selected = False
    cv2.setMouseCallback("frame", select_roi)
    while not roi_selected:
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            frame = frame.copy()

        elif key == ord("c"):
            roi_selected = True

    # Update the coordinates for the second ROI
    y2, h2, w2, x2 = refPt[0][1], refPt[1][1] - refPt[0][1], refPt[1][0] - refPt[0][0], refPt[0][0]

    # Reset to the start of the video
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break if no more frames or error

        frame_count += 4

        # Crop to the first selected ROI
        roi_frame = frame[y1:y1+h1, x1:x1+w1]

        # Convert to grayscale for easier color thresholding
        gray_frame = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

        # Threshold for white color
        _, threshold_frame = cv2.threshold(gray_frame, 240, 255, cv2.THRESH_BINARY)

        # Check if there is any white color in the frame's first ROI
        if np.any(threshold_frame == 255):
            # Crop to the second selected ROI and save
            roi_frame_save = frame[y2:y2+h2, x2:x2+w2]
            cv2.imwrite(f'frame_{frame_count}.jpg', roi_frame_save)

# Release the video capture and close all windows

# Remaining code for processing saved frames...

# Release the video capture and close all windows
saved_frames = sorted([f for f in os.listdir('.') if f.startswith('frame_')])

# Iterate through the saved frames and compare each frame to the next frame
i = 0
while i < len(saved_frames) - 1:
    frame1_filename = saved_frames[i]
    frame2_filename = saved_frames[i + 1]

    frame1 = cv2.imread(frame1_filename, cv2.IMREAD_GRAYSCALE)
    frame2 = cv2.imread(frame2_filename, cv2.IMREAD_GRAYSCALE)

    if frame1 is None or frame2 is None:
        print(f"Failed to load {frame1_filename} or {frame2_filename}")
        i += 1
        continue  # Skip this pair of frames and move to the next

    # Calculate the Structural Similarity Index (SSI) between two frames
    ssi_index, _ = ssim(frame1, frame2, full=True)

    # Define a threshold for similarity
    threshold = 0.57

    # If the SSI is above the threshold, delete the second frame in the pair
    if ssi_index > threshold:
        print(f"Deleting {frame2_filename} as it's similar to {frame1_filename}")
        os.remove(frame2_filename)
    else:
        i += 1  # Move to the next frame if they are not similar


# Close the video capture

cap.release()
cv2.destroyAllWindows()

