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
from Dinosaur import Dino
from Cloud import Cloud

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


# Initializing assets

track=pygame.image.load(os.path.join("Assets", "Track.png"))
cloud=pygame.image.load(os.path.join("Assets", "Cloud.png"))
smallCactus=[pygame.image.load(os.path.join("Assets", "SmallCactus1.png")),
             pygame.image.load(os.path.join("Assets", "SmallCactus2.png")),
             pygame.image.load(os.path.join("Assets", "SmallCactus3.png"))]
largeCactus=[pygame.image.load(os.path.join("Assets", "LargeCactus1.png")),
             pygame.image.load(os.path.join("Assets", "LargeCactus2.png")),
             pygame.image.load(os.path.join("Assets", "LargeCactus3.png"))]

bird=[pygame.image.load(os.path.join("Assets", "Bird1.png")), pygame.image.load(os.path.join("Assets", "Bird2.png"))]
currentGesture=""

# Initializing Obstacle superclass and bird and cactus objects that inherit from obstacle class

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

class Cactus(Obstacle):

    def __init__(self, cactus_type):
        self.cactus_type=cactus_type
        self.type=random.randint(0, 2)
        
        if self.cactus_type=='small':
            super().__init__(smallCactus, self.type)
            self.rect.y=325
        else:
            super().__init__(largeCactus, self.type)
            self.rect.y=300

def main() -> None:
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

    def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int) -> None:
        global currentGesture

        # Parsing through the text returned by model to obtain just the gesture

        if len(result.gestures)!=0:
            substring=str(result.gestures[0][0]).split(',')[3]
            currentGesture=substring[substring.index('=')+1:substring.index(')')]

    # Method to get the current score of the user and display it on screen

    def scoreSystem() -> None:
        global score, gameSpeed
        score+=1
        if score%100==0:
            gameSpeed+=1

        text=font.render("Score: " + str(score), True, (0, 0, 0))
        textRect=text.get_rect()
        textRect.center=(1000, 40)
        screen.blit(text, textRect)

    # Moves the track the dino is running on to feel like the dino is "running" even though it is standing still

    def background() -> None:
        global xposBg, yposBg

        imgWidth=track.get_width()
        screen.blit(track, (xposBg, yposBg))
        screen.blit(track, (xposBg+imgWidth, yposBg))

        if xposBg<=-imgWidth:
            screen.blit(track, (xposBg+imgWidth, yposBg))
            xposBg=0

        xposBg-=gameSpeed

    # Title screen method

    def welcomeScreen() -> None:
        global running
        running = True
        while running:
            screen.fill((255, 255, 255))
            title=pygame.font.Font('freesansbold.ttf', 50)
            smaller=pygame.font.Font('freesansbold.ttf', 40)

            text = title.render("Welcome to the Gesture-Controlled Dino Game!", False, (0, 0, 0))
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

    # Method for the second screen, allowing users to position their hands to be detected by the model

    def align() -> None:
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

    # Game over method to display high score status and ask user if they want to play again or quit

    def gameOver() -> None:
        
        screen.fill((255, 255, 255))

        gameOverFont=pygame.font.Font('freesansbold.ttf', 45)
        font = pygame.font.Font('freesansbold.ttf', 30)
        beat_high_score, high_score=getHighScore(score)

        if beat_high_score:
            beat_score_message=font.render("You Have a New High Score!", True, (0, 0, 0))
        else:
            beat_score_message=font.render(f"You Didn't Beat the Current High Score of {str(high_score)}", True, (0, 0, 0))
        beat_score_rect=beat_score_message.get_rect()
        beat_score_rect.center=(screenWidth //2, screenHeight //2 + 50)
        
        
        text = gameOverFont.render("Game Over!", False, (0, 0, 0))
        textRect=text.get_rect()
        textRect.center = (screenWidth // 2, screenHeight // 2 -150)
        
        scoreTot = font.render("Your Score: " + str(score), True, (0, 0, 0))
        scoreRect = scoreTot.get_rect()
        scoreRect.center = (screenWidth // 2, screenHeight // 2 +100)

        playAgain = font.render("Hit 'r' to play again or 'q' to quit!", True, (0, 0, 0))
        playAgainRect = playAgain.get_rect()
        playAgainRect.center = (screenWidth // 2, screenHeight // 2 + 200)

        screen.blit(text, textRect)
        screen.blit(beat_score_message,beat_score_rect)
        screen.blit(scoreTot, scoreRect)
        screen.blit(playAgain, playAgainRect)

        pygame.display.update()
        
        leave_screen=False

        while not leave_screen:

            if pygame.key.get_pressed()[pygame.K_r]:
                main()
                leave_screen=True

            for event in pygame.event.get():
                if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_q]:
                    pygame.quit()
                    leave_screen=True
                    sys.exit()

    # Method to read current high score from txt file and copare to current score                

    def getHighScore(score) -> (bool, int):

        if (os.path.exists("highscore.txt") == False):
            f = open("highscore.txt", "w")
            f.write(str(score))
            f.close()
            current_high_score=score

            return True, current_high_score
        
        else:
            f=open("highscore.txt", "r")
            current_high_score=f.read()
            
            f.close()

            if (score>int(current_high_score)):
                f2=open("highscore.txt", "w")
                f2.write(str(score))
                f2.close()

                return True, current_high_score
            
        return False, current_high_score

    # Main method responsible for playing the game            
    
    def startGame() -> None:
        global running         
        timestamp = 0

        options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_path=model_path),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=print_result)

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
                    
                    # Error handling

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
                            obstacles.append(Cactus("small"))
                        elif random.randint(0, 2)==1:
                            obstacles.append(Cactus("large"))
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

