import pygame
from pygame.locals import *
import os

duck=pygame.image.load(os.path.join("Assets", "DinoDuck.png"))
normal=pygame.image.load(os.path.join("Assets", "DinoStart.png"))

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

        self.img=self.normal_image
        self.dinoRectangle=self.img.get_rect()

        self.dinoRectangle.x=self.xPos
        self.dinoRectangle.y=self.yPos
        
        if test:
            self.dinoRectangle.x=self.xPosTest
            self.dinoRectangle.y=self.yPosTest

        self.jumpVel=self.jump_Vel
    

    def update(self, currentGesture, test=False) -> None:

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
        
    
    def normal(self, test=False) -> None:
        self.img=self.normal_image
        self.dinoRectangle=self.img.get_rect()
        if test:
            self.dinoRectangle.x=self.xPosTest
            self.dinoRectangle.y=self.yPosTest
        else:    
            self.dinoRectangle.x=self.xPos
            self.dinoRectangle.y=self.yPos

    def jump(self, test=False) -> None:
        self.img=self.normal_image
        if self.dinoJump:
            self.dinoRectangle.y-=self.jumpVel*4
            self.jumpVel-=0.8
        
        if self.jumpVel<-self.jump_Vel:
            self.dinoJump=False
            self.jumpVel=self.jump_Vel

    def duck(self, test=False) -> None:
        self.img=self.duck_image
        self.dinoRectangle=self.img.get_rect()

        if test:
            self.dinoRectangle.x=self.xPosTest
            self.dinoRectangle.y=self.yPosTest
            self.dinoRectangle.y=self.yPosDuckTest
        else:    
            self.dinoRectangle.x=self.xPos
            self.dinoRectangle.y=self.yPos
            self.dinoRectangle.y=self.yPosDuck
    
    def draw(self, screen) -> None:
        screen.blit(self.img, (self.dinoRectangle.x, self.dinoRectangle.y))
 