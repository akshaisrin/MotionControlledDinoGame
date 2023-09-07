import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2 as cv
import time

cap = cv.VideoCapture(0)


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

model_path="C:\\Users\\aksha\\Documents\\GitHub\\MotionControlledDinoGame\\gesture_recognizer.task"

def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if len(result.gestures)!=0:
        substring=str(result.gestures[0][0]).split(',')[3]
        print(substring[substring.index('=')+1:substring.index(')')])
    
    #print('gesture recognition result: '.format(result))

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

print(cap.isOpened())

timestamp = 0
count=0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    
    while cap.isOpened():
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        count+=1
        cv.imshow('live video', frame)

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        # Send live image data to perform gesture recognition
        # The results are accessible via the `result_callback` provided in
        # the `GestureRecognizerOptions` object.
        # The gesture recognizer must be created with the live stream mode.
        recognizer.recognize_async(mp_image, timestamp)
       
        if cv.waitKey(1) == ord('q'):
            break


cap.release()
cv.destroyAllWindows()