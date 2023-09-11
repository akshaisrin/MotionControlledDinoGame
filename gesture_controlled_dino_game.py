import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2 as cv
import time
import pygame
from pygame.locals import *
import sys
import os
import random

pygame.init()

screenHeight=750
screenWidth=1200
screen=pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Motion Controlled Dino Game")

cap = cv.VideoCapture(0)

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

model_path="C:\\Users\\aksha\\Documents\\GitHub\\MotionControlledDinoGame\\gesture_recognizer.task"

duck=[pygame.image.load(os.path.join("Assets", "DinoDuck.png"))]
normal=[pygame.image.load(os.path.join("Assets", "DinoStart.png"))]
track=pygame.image.load(os.path.join("Assets", "Track.png"))
cloud=pygame.image.load(os.path.join("Assets", "Cloud.png"))
smallCactus=[pygame.image.load(os.path.join("Assets", "SmallCactus1.png")),
             pygame.image.load(os.path.join("Assets", "SmallCactus2.png")),
             pygame.image.load(os.path.join("Assets", "SmallCactus3.png"))]
largeCactus=[pygame.image.load(os.path.join("Assets", "LargeCactus1.png")),
             pygame.image.load(os.path.join("Assets", "LargeCactus2.png")),
             pygame.image.load(os.path.join("Assets", "LargeCactus3.png"))]

bird=[pygame.image.load(os.path.join("Assets", "Bird1.png")), pygame.image.load(os.path.join("Assets", "Bird2.png"))]


class Dino:
    
    xPos=80
    yPos=310
    yPosDuck=340
    jump_Vel=8.5

    xPosTest=500
    yPosTest=360
    yPosDuckTest=390

    def __init__(self, test=False):

        self.duck_image=duck
        self.normal_image=normal

        self.dinoDuck=False
        self.dinoJump=False
        self.dinoNormal=True

        self.img=self.normal_image[0]
        self.dinoRectangle=self.img.get_rect()

        self.dinoRectangle.x=self.xPos
        self.dinoRectangle.y=self.yPos
        
        if test:
            self.dinoRectangle.x=self.xPosTest
            self.dinoRectangle.y=self.yPosTest

        self.jumpVel=self.jump_Vel
    

    def update(self, currentGesture, test=False):

        if self.dinoDuck:
            self.duck(test)
        
        if self.dinoJump:
            self.jump(test)
        
        if self.dinoNormal:
            self.normal(test)
        
        if currentGesture=="'Thumb_Up'" and not self.dinoJump:
            self.dinoJump=True
            self.dinoDuck=False
            self.dinoNormal=False
            currentGesture=""
        
        elif currentGesture=="'Thumb_Down'" and not self.dinoDuck:
            self.dinoJump=False
            self.dinoDuck=True
            self.dinoNormal=False
            currentGesture=""
        
        elif not (self.dinoJump or currentGesture=="'Thumb_Down'"):
            self.dinoDuck=False
            self.dinoJump=False
            self.dinoNormal=True
        
    

    def normal(self, test=False):
        self.img=self.normal_image[0]
        self.dinoRectangle=self.img.get_rect()
        if test:
            self.dinoRectangle.x=self.xPosTest
            self.dinoRectangle.y=self.yPosTest
        else:    
            self.dinoRectangle.x=self.xPos
            self.dinoRectangle.y=self.yPos

    def jump(self, test=False):
        self.img=self.normal_image[0]
        if self.dinoJump:
            self.dinoRectangle.y-=self.jumpVel*4
            self.jumpVel-=0.8
        
        if self.jumpVel<-self.jump_Vel:
            self.dinoJump=False
            self.jumpVel=self.jump_Vel

    def duck(self, test=False):
        self.img=self.duck_image[0]
        self.dinoRectangle=self.img.get_rect()

        if test:
            self.dinoRectangle.x=self.xPosTest
            self.dinoRectangle.y=self.yPosTest
            self.dinoRectangle.y=self.yPosDuckTest
        else:    
            self.dinoRectangle.x=self.xPos
            self.dinoRectangle.y=self.yPos
            self.dinoRectangle.y=self.yPosDuck
    
    def draw(self, screen):
        screen.blit(self.img, (self.dinoRectangle.x, self.dinoRectangle.y))
 
class Cloud:

    def __init__(self):
        self.x=screenWidth+random.randint(800, 1000)
        self.y=random.randint(50, 100)
        self.img=cloud
        self.width=self.img.get_width()
    
    def update(self):
        self.x-=gameSpeed

        if self.x<self.width:
            self.x=screenWidth+random.randint(2000, 2500)
            self.y=random.randint(50, 100)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

class Obstacle:

    def __init__(self, img, type):
        self.img=img
        self.type=type
        self.rect=(self.img[self.type]).get_rect()
        self.rect.x=screenWidth

    def update(self):
        self.rect.x-=gameSpeed
        if self.rect.x < self.rect.width:
            obstacles.pop()

    def draw(self, screen):
        screen.blit(self.img[self.type], self.rect)

class SmallCactus(Obstacle):
    
    def __init__(self, img):
        self.type=random.randint(0, 2)
        super().__init__(img, self.type)
        self.rect.y=325

class LargeCactus(Obstacle):
    
    def __init__(self, img):
        self.type=random.randint(0, 2)
        super().__init__(img, self.type)
        self.rect.y=300

class Bird(Obstacle):
    def __init__(self, img):
        self.type=0
        super().__init__(img, self.type)
        self.rect.y=250
        self.index=0
    
    def draw(self, screen):
        if self.index>=9:
            self.index=0
        screen.blit(self.img[self.index//5], self.rect)
        self.index+=1


currentGesture=""
def main():
    global gameSpeed, xposBg, yposBg, score, obstacles, currentGesture
    
    player=Dino()
    testPlayer=Dino(True)

    cloud=Cloud()
    xposBg=0
    yposBg=380
    score=0
    font=pygame.font.Font('freesansbold.ttf', 20)
    obstacles=[]

    clock=pygame.time.Clock()
    gameSpeed=14

    def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        global currentGesture
        if len(result.gestures)!=0:
            substring=str(result.gestures[0][0]).split(',')[3]
            currentGesture=substring[substring.index('=')+1:substring.index(')')]

    def scoreSystem():
        global score, gameSpeed
        score+=1
        if score%100==0:
            gameSpeed+=1

        text=font.render("Score: " + str(score), True, (0, 0, 0))
        textRect=text.get_rect()
        textRect.center=(1000, 40)
        screen.blit(text, textRect)

    def background():
        global xposBg, yposBg

        imgWidth=track.get_width()
        screen.blit(track, (xposBg, yposBg))
        screen.blit(track, (xposBg+imgWidth, yposBg))

        if xposBg<=-imgWidth:
            screen.blit(track, (xposBg+imgWidth, yposBg))
            xposBg=0

        xposBg-=gameSpeed

    def welcomeScreen():
        global running
        running = True
        while running:
            screen.fill((255, 255, 255))
            title=pygame.font.Font('freesansbold.ttf', 50)
            smaller=pygame.font.Font('freesansbold.ttf', 40)

            text = title.render("Welcome to the Gesture-Powered Dino Game!", False, (0, 0, 0))
            textRect=text.get_rect()
            textRect.center = (screenWidth // 2, screenHeight // 2 -150)

            text2=smaller.render("Hit 's' to start playing!", False, (0, 0, 0))
            text2Rect=text2.get_rect()
            text2Rect.center = (screenWidth // 2, screenHeight // 2 -50)

            screen.blit(text, textRect)
            screen.blit(text2, text2Rect)
            
            pygame.display.update()
            if pygame.key.get_pressed()[pygame.K_s]:
                align()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def align():
        running=True
        xposBg=00
        yposBg=410
        timestamp = 0

        options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)

        while running:
            
            
            with GestureRecognizer.create_from_options(options) as recognizer:

                while cap.isOpened():
                    if pygame.key.get_pressed()[pygame.K_g]:
                        startGame()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    
                    screen.fill((255, 255, 255))
                    smaller=pygame.font.Font('freesansbold.ttf', 25)

                    text = smaller.render("In this game, you will control the dino using various hand gestures.", False, (0, 0, 0))
                    textRect=text.get_rect()
                    textRect.center = (screenWidth // 2 +50, screenHeight // 2 -350)

                    text2 = smaller.render("Use a thumbs up to jump, thumbs down to duck, and sideways fist otherwise.", False, (0, 0, 0))
                    text2Rect=text2.get_rect()
                    text2Rect.center = (screenWidth // 2 +70, screenHeight // 2 -300)

                    text3 = smaller.render("Try it out for yourself, then hit 'g' to start the game!", False, (0, 0, 0))
                    text3Rect=text3.get_rect()
                    text3Rect.center = (screenWidth // 2 +70, screenHeight // 2 -250)

                    
                    screen.blit(text, textRect)
                    screen.blit(text2, text2Rect)
                    screen.blit(text3, text3Rect)

                    ret, frame = cap.read()
            
                    frame2 = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                    frame2 = np.rot90(frame2)
                    
                    frame2 = pygame.surfarray.make_surface(frame2)
                    frame2=pygame.transform.scale(frame2, (200, 200))
                    screen.blit(frame2, (0,0))
                    

                    if not ret:
                        print("Ignoring empty frame")
                        break

                    timestamp += 1
                    
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

                    recognizer.recognize_async(mp_image, timestamp)

                 
                    testPlayer.draw(screen)
                    testPlayer.update(currentGesture, True)
                    screen.blit(track, (xposBg, yposBg))

                    pygame.display.update()
    def gameOver():
        running = True
        while running:
            screen.fill((255, 255, 255))
            gameOverFont=pygame.font.Font('freesansbold.ttf', 45)
            font = pygame.font.Font('freesansbold.ttf', 30)

            
            text = gameOverFont.render("Game Over!", False, (0, 0, 0))
            textRect=text.get_rect()
            textRect.center = (screenWidth // 2, screenHeight // 2 -50)

            scoreTot = font.render("Your Score: " + str(score), True, (0, 0, 0))
            scoreRect = scoreTot.get_rect()
            scoreRect.center = (screenWidth // 2, screenHeight // 2 +50)

            playAgain = font.render("Hit 'r' to play again or 'q' to quit!", True, (0, 0, 0))
            playAgainRect = playAgain.get_rect()
            playAgainRect.center = (screenWidth // 2, screenHeight // 2 + 150)


            screen.blit(text, textRect)
            screen.blit(scoreTot, scoreRect)
            screen.blit(playAgain, playAgainRect)
            
            pygame.display.update()

            if pygame.key.get_pressed()[pygame.K_r]:
                main()   
            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                    running = False
                    pygame.quit()
                    sys.exit()

    def startGame():
        global running         
        timestamp = 0

        options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)

        print(cap.isOpened())

        while running:
            with GestureRecognizer.create_from_options(options) as recognizer:
            
                while cap.isOpened():

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                    
                    screen.fill((255, 255, 255))

                    ret, frame = cap.read()
            
                    frame2 = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
                    frame2 = np.rot90(frame2)
                    
                    frame2 = pygame.surfarray.make_surface(frame2)
                    frame2=pygame.transform.scale(frame2, (200, 200))
                    screen.blit(frame2, (0,0))
                    

                    if not ret:
                        print("Ignoring empty frame")
                        break

                    timestamp += 1
                    
                    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

                    recognizer.recognize_async(mp_image, timestamp)

                    player.draw(screen)
                    player.update(currentGesture)

                    if len(obstacles)==0:
                        if random.randint(0, 2)==0:
                            obstacles.append(SmallCactus(smallCactus))
                        elif random.randint(0, 2)==1:
                            obstacles.append(LargeCactus(largeCactus))
                        elif random.randint(0, 2)==2:
                            obstacles.append(Bird(bird))

                    for obstacle in obstacles:
                        obstacle.draw(screen)
                        obstacle.update()

                        if player.dinoRectangle.colliderect(obstacle.rect):
                            time.sleep(1.2)
                            gameOver()
                            
                            sys.exit()

                    background()

                    cloud.draw(screen)
                    cloud.update()

                    scoreSystem()

                    clock.tick(30)
                    pygame.display.update()

    welcomeScreen()

main()

