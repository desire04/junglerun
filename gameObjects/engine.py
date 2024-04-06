import pygame

from . import Drawable, Sonic, Background, Rock

from utils import vec, RESOLUTION

import random

class GameEngine(object):

    def __init__(self):       
        self.sonic = Sonic((0,205))
        self.size = vec(*RESOLUTION)
        self.background = Background((0,0))
        self.floor = pygame.Rect(0, 236, 100000000000000, 100)
        self.obstaclePositions = [200, 400, 600]
        self.rock1 = Drawable((self.obstaclePositions[0], 206), "mountain_small.png", (0,0))
        self.rock1.myRect = pygame.Rect(8, 25, 20, 5)
        self.rock2 = Drawable((self.obstaclePositions[2], 206), "mountain_wide.png", (0,0))
        self.rock2.myRect = pygame.Rect(8, 25, 20, 5)
        self.tree1 = Drawable((self.obstaclePositions[1], 207), "trees.png", (0,0))
        self.tree1.myRect = pygame.Rect(8, 17, 20, 5)
        
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.sonic.draw(drawSurface)

        pygame.draw.rect(drawSurface, (205,135,65), self.floor)
        #pygame.draw.rect(drawSurface, (255,255,255), self.rock2.myRect)
        
        self.rock1.draw(drawSurface)
        self.rock2.draw(drawSurface)
        self.tree1.draw(drawSurface)

            
    def handleEvent(self, event):
        self.sonic.handleEvent(event)
    
    def update(self, seconds):
        colliders = [self.rock1.getCollisionRect(), self.tree1.getCollisionRect(), self.rock2.getCollisionRect(), self.floor]
        result = self.sonic.update(seconds, colliders)
        self.background.update()

        offsetAmount = Drawable.CAMERA_OFFSET[0] + RESOLUTION[0]
        if self.rock1.position[0] + self.rock1.myRect.width < Drawable.CAMERA_OFFSET[0]:
            self.rock1.position[0] = random.randint(offsetAmount + 200, offsetAmount + 400)
        
        if self.tree1.position[0] + self.tree1.myRect.width < Drawable.CAMERA_OFFSET[0]:
            self.tree1.position[0] = random.randint(offsetAmount + 150, offsetAmount + 450)

        Drawable.updateOffset(self.sonic, self.size)

        if result:
            return result
    

