import pygame

from utils import vec, RESOLUTION
from . import Drawable
import random

class Rock(Drawable):
    #give it an empty string for now 
    def __init__(self, position=vec(70,206), fileName="mountain_small.png", offset=(0,0)):
        super().__init__(position, fileName, offset)
        self.collideRect = pygame.Rect(8, 25, 20, 5)
        self.obstacleDistance = 200

    def draw(self, drawSurface):
        super().draw(drawSurface)

    def update(self):
        #rock position + width < Camera offset
        offsetAmount = Drawable.CAMERA_OFFSET[0] + RESOLUTION[0]
        if self.position[0] < offsetAmount:
            self.position[0] = random.randint(offsetAmount + 150, offsetAmount + 450)

    def getCollisionRect(self):
        return self.collideRect

    #ask her about it again. Right now, just set it to a very large number. 
