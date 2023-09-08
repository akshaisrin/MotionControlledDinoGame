import pygame
from pygame.locals import *
import cv2
import numpy as np
import sys

camera = cv2.VideoCapture(0)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1280,720])


while True:

    ret, frame = camera.read()
    
    screen.fill([255,255,255])
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.rot90(frame)
    
    frame = pygame.surfarray.make_surface(frame)
    frame=pygame.transform.scale(frame, (200, 200))
    screen.blit(frame, (0,0))
    pygame.display.update()

    for event in pygame.event.get():
        if pygame.key.get_pressed()[pygame.K_q]:
            camera.release()
            cv2.destroyAllWindows()
            sys.exit(0)

