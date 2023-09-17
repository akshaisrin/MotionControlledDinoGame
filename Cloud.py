import random
import pygame
from pygame.locals import *
import os

screenHeight=750
screenWidth=1200
gameSpeed=14
cloud=pygame.image.load(os.path.join("Assets", "Cloud.png"))

class Cloud:

    def __init__(self):
        self.x=screenWidth+random.randint(800, 1000)
        self.y=random.randint(50, 100)
        self.img=cloud
        self.width=self.img.get_width()
    
    def update(self) -> None:
        self.x-=gameSpeed

        if self.x<self.width:
            self.x=screenWidth+random.randint(2000, 2500)
            self.y=random.randint(50, 100)

    def draw(self, screen) -> None:
        screen.blit(self.img, (self.x, self.y))