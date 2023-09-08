import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2 as cv
import time
import pygame
from pygame.locals import *
import sys

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1280,720])
screen.fill([255,255,255])
cap = cv.VideoCapture(1)


BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

model_path="C:\\Users\\aksha\\Documents\\GitHub\\MotionControlledDinoGame\\gesture_recognizer.task"


val=""
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    global val
    if len(result.gestures)!=0:
        substring=str(result.gestures[0][0]).split(',')[3]
        val=substring[substring.index('=')+1:substring.index(')')]

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

print(cap.isOpened())

timestamp = 0
with GestureRecognizer.create_from_options(options) as recognizer:
  # The recognizer is initialized. Use it here.
    
    while cap.isOpened():
        
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        frame2 = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        frame2 = np.rot90(frame2)
        
        frame2 = pygame.surfarray.make_surface(frame2)
        frame2=pygame.transform.scale(frame2, (200, 200))
        screen.blit(frame2, (0,0))
        pygame.display.update()

        if not ret:
            print("Ignoring empty frame")
            break

        timestamp += 1
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        recognizer.recognize_async(mp_image, timestamp)
        print(val)
        #print(result_callback)

        for event in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_q]:
                cap.release()
                cv.destroyAllWindows()
                sys.exit(0)
