# Hand-Gesture
Control the zoom in/out using your thumb and index finger.
Ever wished to control a document  by just using your index finger and thumb in the air? In this post, I have a project that has the capability to enable you to zoom in/out of the document. A virtual drawing tool (Computer vision project) that allows you to move your hands in the air using hand gestures, thanks to the powerful combination of OpenCV and MediaPipe.

🔧 Tools and Libraries Used:

Python3, opencv , mediapipe, pyautogui, pygetwindow, absl-py, 

OpenCV: This open-source library is essential for real-time computer vision tasks. It helped me capture and process video frames from the webcam seamlessly.

MediaPipe: Developed by Google, MediaPipe is a fantastic framework for building multimodal machine learning pipelines. In this project, I used MediaPipe for hand tracking, enabling accurate and real-time recognition of hand landmarks.

How It Works:

Capture Video: Using OpenCV, the script captures live video feed from the webcam.
Process Frames: Each frame is processed using MediaPipe to detect and track hand landmarks.
Draw Landmarks: The detected hand landmarks are drawn on the video frames.
The distance between the funger tip and the thumb tip is calculated, the distance is used to control the zoom in/out of the document.
I am also using Adobe Acrobat Document viewer.
Algorithm
Start reading the frames and convert the captured frames to HSV colour space.(Easy for colour detection)

Adjust the values of the mediapipe utilization to detect one hand only.

Detect the landmarks by passing the RGB frame to the mediapipe hand detector.

Detect the landmarks, calculates the distance between the thumb tip and the finger tip, uses the distance to control the zooming.

Finally, draw the line connecting the thumb tip and the funger tip, i.e controlling the zooming effect.

I commented this part since I am using the default Camera(One camera) #cv2.imshow('Gesture Capture', frame)![Hands](https://github.com/Stud58/Hand-Gesture/assets/118792996/e17686f1-985b-4e15-8304-7432d81df673)





