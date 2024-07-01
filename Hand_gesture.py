import os
import cv2
import mediapipe as mp
import pyautogui
import pygetwindow as gw
import time
import absl.logging

# Suppress TensorFlow and Mediapipe logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
absl.logging.set_verbosity(absl.logging.ERROR)

# Function to calculate the distance between two points
def calculate_distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

# Function to activate the window of the document viewer
def activate_window(window_title):
    window = gw.getWindowsWithTitle(window_title)
    if window:
        window[0].activate()

# Set the title of the window to active
document_viewer_title = 'Hand Gesture.pdf'

# Initialize Mediapipe hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
ret = True

# Time variables to control zoom commands
last_zoom_time = time.time()
zoom_delay = 0.5  # 0.5 second delay

while ret:
    # Read each frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a mirror view
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to detect hands
    results = hands.process(frame_rgb)

    # If hands are detected
    if results.multi_hand_landmarks:
        for handslms in results.multi_hand_landmarks:
            thumb_tip = handslms.landmark[mpHands.HandLandmark.THUMB_TIP]
            index_tip = handslms.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
            middle_tip = handslms.landmark[mpHands.HandLandmark.MIDDLE_FINGER_TIP]

            thumb_coord = (int(thumb_tip.x * frame.shape[1]), int(thumb_tip.y * frame.shape[0]))
            index_coord = (int(index_tip.x * frame.shape[1]), int(index_tip.y * frame.shape[0]))
            middle_coord = (int(middle_tip.x * frame.shape[1]), int(middle_tip.y * frame.shape[0]))

            # Draw landmarks on the frame for thumb and index finger
            cv2.circle(frame, thumb_coord, 5, (0, 255, 0), -1)
            cv2.circle(frame, index_coord, 5, (0, 255, 0), -1)

            # Draw a line between thumb and index finger
            cv2.line(frame, thumb_coord, index_coord, (255, 0, 0), 2)

            # Draw the landmarks and connections of the whole hand
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Calculate the distance between thumb and index finger
            distance = calculate_distance(thumb_tip, index_tip)
            cv2.putText(frame, f'Distance: {distance:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

            # Activate the document viewer window
            activate_window(document_viewer_title)

            # Determine zoom in/out based on the distance with delay
            current_time = time.time()
            if current_time - last_zoom_time > zoom_delay:
                if distance < 0.25:
                    cv2.putText(frame, 'Zoom Out', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                    pyautogui.hotkey('ctrl', '-')  # Zoom Out
                    last_zoom_time = current_time
                elif distance > 0.25:  # Adjust the range for zooming in
                    cv2.putText(frame, 'Zoom In', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    pyautogui.hotkey('ctrl', '=')  # Zoom In
                    last_zoom_time = current_time

    # Display the frame
    cv2.imshow('Gesture Capture', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture and destroy all windows
cap.release()
cv2.destroyAllWindows()
