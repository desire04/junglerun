import pygame

from utils import vec, RESOLUTION
from . import Drawable
import random

class PowerUp(Drawable):
    #give it an empty string for now 
    def __init__(self, position=vec(100,150), fileName="mountain_small.png", offset=(0,0)):
        super().__init__(position, fileName, offset)
        self.isCollided = False
        self.isActive = True
        self.isAttached = False

    def draw(self, drawSurface):
        super().draw(drawSurface)

    
    def update(self):
        """if not self.isAttached:
            offsetAmount = Drawable.CAMERA_OFFSET[0] + RESOLUTION[0]
            self.position[0] = random.randint(offsetAmount + 500, offsetAmount + 1500)"""
        pass


    #ask her about it again. Right now, just set it to a very large number. 
