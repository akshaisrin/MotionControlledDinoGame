import os
import pygame
import random
import sys
from pygame import *

pygame.init()

screenHeight=600
screenWidth=1200
screen=pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Motion Controlled Dino Game")

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


    def __init__(self):

        self.duck_image=duck
        self.normal_image=normal

        self.dinoDuck=False
        self.dinoJump=False
        self.dinoNormal=True

        self.img=self.normal_image[0]
        self.dinoRectangle=self.img.get_rect()

        self.dinoRectangle.x=self.xPos
        self.dinoRectangle.y=self.yPos

        self.jumpVel=self.jump_Vel
    

    def update(self, userInput):
        if self.dinoDuck:
            self.duck()
        
        if self.dinoJump:
            self.jump()
        
        if self.dinoNormal:
            self.normal()
        
        if userInput[pygame.K_UP] and not self.dinoJump:
            self.dinoJump=True
            self.dinoDuck=False
            self.dinoNormal=False
        
        elif userInput[pygame.K_DOWN] and not self.dinoDuck:
            self.dinoJump=False
            self.dinoDuck=True
            self.dinoNormal=False
        
        elif not (self.dinoJump or userInput[pygame.K_DOWN]):
            self.dinoDuck=False
            self.dinoJump=False
            self.dinoNormal=True
        
    

    def normal(self):
        self.img=self.normal_image[0]
        self.dinoRectangle=self.img.get_rect()

        self.dinoRectangle.x=self.xPos
        self.dinoRectangle.y=self.yPos

    def jump(self):
        self.img=self.normal_image[0]
        if self.dinoJump:
            self.dinoRectangle.y-=self.jumpVel*4
            self.jumpVel-=0.8
        
        if self.jumpVel<-self.jump_Vel:
            self.dinoJump=False
            self.jumpVel=self.jump_Vel

    def duck(self):
        self.img=self.duck_image[0]
        self.dinoRectangle=self.img.get_rect()

        self.dinoRectangle.x=self.xPos
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

def main():
    global gameSpeed, xposBg, yposBg, score, obstacles

    running=True
    player=Dino()
    cloud=Cloud()
    xposBg=0
    yposBg=380
    score=0
    font=pygame.font.Font('freesansbold.ttf', 20)
    obstacles=[]


    clock=pygame.time.Clock()
    gameSpeed=14


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


    def gameOver():
        running = True
        while running:
            screen.fill((255, 255, 255))
            font = pygame.font.Font('freesansbold.ttf', 30)

            
            text = font.render("Game Over!", False, (0, 0, 0))
            textRect=text.get_rect()
            textRect.center = (screenWidth // 2, screenHeight // 2)

            scoreTot = font.render("Your Score: " + str(score), True, (0, 0, 0))
            scoreRect = scoreTot.get_rect()
            scoreRect.center = (screenWidth // 2, screenHeight // 2 + 50)
            screen.blit(text, textRect)
            screen.blit(scoreTot, scoreRect)
            
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    time.delay(1000)
                    pygame.quit()
                    sys.exit()

    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        screen.fill((255, 255, 255))
        userInput=pygame.key.get_pressed()


        player.draw(screen)
        player.update(userInput)

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
                time.delay(1500)
                gameOver()

        background()

        cloud.draw(screen)
        cloud.update()

        scoreSystem()

        clock.tick(30)
        pygame.display.update()


main()