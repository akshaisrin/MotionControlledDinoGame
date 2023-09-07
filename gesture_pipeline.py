import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

model_path="C:\\Users\\aksha\\Documents\\GitHub\\MotionControlledDinoGame\\gesture_recognizer.task"

results=[]

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.IMAGE)

recognizer = vision.GestureRecognizer.create_from_options(options)
mp_image = mp.Image.create_from_file("C:\\Users\\aksha\\Documents\\GitHub\\MotionControlledDinoGame\\thumbs_up.jpg")

gesture_recognition_result = recognizer.recognize(mp_image)


top_gesture = str(gesture_recognition_result.gestures[0][0]).split(',')[3]
res=top_gesture[top_gesture.index('=')+1:top_gesture.index(')')]
hand_landmarks = gesture_recognition_result.hand_landmarks

print(res)


