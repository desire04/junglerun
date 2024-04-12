import pygame

from . import Drawable, Sonic, Background, PowerUp, Tiger

from utils import vec, RESOLUTION, rectAdd

import random

class GameEngine(object):
    def __init__(self, level):
        self.loaded = False
        self.level = level
    
    def load(self):       
        if not self.loaded:
            self.sonic = Sonic((0,205))
            self.tiger = Tiger((-200, 170))
            self.size = vec(*RESOLUTION)
            self.background = Background((0,0))
            self.floor = pygame.Rect(0, 236, 100000000000000, 100)
            self.obstaclePositions = [200, 400, 600]
            if self.level == 0:
                self.rock1 = Drawable((self.obstaclePositions[0], 206), "mountain_small.png", (0,0))
                self.rock1.myRect = pygame.Rect(8, 25, 20, 5)
            elif self.level == 1:
                self.rock1 = Drawable((self.obstaclePositions[0], 206), "mountain_small.png", (0,0))
                self.rock1.myRect = pygame.Rect(8, 25, 20, 5)
                self.rock2 = Drawable((self.obstaclePositions[2], 206), "mountain_wide.png", (0,0))
                self.rock2.myRect = pygame.Rect(8, 25, 30, 5)
            elif self.level == 2:
                self.rock1 = Drawable((self.obstaclePositions[0], 206), "mountain_small.png", (0,0))
                self.rock1.myRect = pygame.Rect(8, 25, 20, 5)
                self.rock2 = Drawable((self.obstaclePositions[2], 206), "mountain_wide.png", (0,0))
                self.rock2.myRect = pygame.Rect(12, 25, 30, 5)
                self.tree1 = Drawable((self.obstaclePositions[1], 207), "trees.png", (0,0))
                self.tree1.myRect = pygame.Rect(8, 20, 12, 5)
            self.shield = PowerUp((100, 150), "bubbleshield.png", (0,0))
            self.shield.myRect = pygame.Rect(20, 20, 12, 5)
            self.shield.offset = vec(-12,-12)

            self.loaded = True
        
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.sonic.draw(drawSurface)
        self.tiger.draw(drawSurface)

        pygame.draw.rect(drawSurface, (205,135,65), self.floor)
        #pygame.draw.rect(drawSurface, (255,255,255), self.shield.getCollisionRect())
        #pygame.draw.rect(drawSurface, (255,255,255), self.rock2.myRect)
        #pygame.draw.rect(drawSurface, (255,255,255), self.tree1.myRect)
        if self.level == 0:
            if self.shield.isActive:
                self.shield.draw(drawSurface)
            self.rock1.draw(drawSurface)
        elif self.level == 1:
            self.rock1.draw(drawSurface)
            self.rock2.draw(drawSurface)
        elif self.level == 2:
            self.rock1.draw(drawSurface)
            self.rock2.draw(drawSurface)
            self.tree1.draw(drawSurface)
            
    def handleEvent(self, event):
        self.sonic.handleEvent(event)
        self.tiger.handleEvent(event)
    
    def update(self, seconds):
        if self.level == 0:
            tigerColliders = [self.sonic]
            colliders = [self.rock1, self.floor]
            """if self.tiger.doesCollide(self.sonic):
                if self.tiger.collisions == 0:
                    self.tiger.collisions += 1
                    if self.tiger.collisions == 1:
                        print(self.tiger.collisions)
                        self.tiger.velocity[0] *= 0.8
                        result = "tiger collided with sonic"
                        return result
            else:
                self.tiger.collisions = 0"""
            if self.shield.doesCollide(self.sonic): 
                self.shield.position = self.shield.offset + self.sonic.position
                self.shield.isAttached = True
                self.sonic.hasAShield = True
                colliders.append(self.shield)
        elif self.level == 1:
             colliders = [self.rock1.getCollisionRect(), self.rock2.getCollisionRect(), self.floor]
        elif self.level == 2:
             colliders = [self.rock1.getCollisionRect(), self.tree1.getCollisionRect(), self.rock2.getCollisionRect(), self.floor]
        result = self.sonic.update(seconds, colliders)
        #tigerResult = self.tiger.update(seconds, tigerColliders)
        self.shield.update()
        self.background.update()
        self.tiger.update(seconds, colliders=None)

        offsetAmount = Drawable.CAMERA_OFFSET[0] + RESOLUTION[0]
        #make it dependent on sonic's velocity
        if self.level == 0:
            if self.rock1.position[0] + self.rock1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock1.position[0] = random.randint(offsetAmount + 200, offsetAmount + 400)

        elif self.level == 1:
            if self.rock1.position[0] + self.rock1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock1.position[0] = random.randint(offsetAmount + 100, offsetAmount + 250)

            if self.rock2.position[0] + self.rock2.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock2.position[0] = random.randint(offsetAmount + 255, offsetAmount + 350)

        elif self.level == 2:
            if self.rock1.position[0] + self.rock1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock1.position[0] = random.randint(200, 400) + self.rock2.position[0]

            if self.tree1.position[0] + self.tree1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.tree1.position[0] = random.randint(200, 400) + self.rock1.position[0]

            if self.rock2.position[0] + self.rock2.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock2.position[0] = random.randint(200, 400) + self.tree1.position[0]

        Drawable.updateOffset(self.sonic, self.size)

        if self.tiger.doesCollide(self.sonic):
            self.tiger.collisions += 1
            if self.tiger.collisions == 1:
                self.tiger.velocity[0] *= 0.8
            return "tiger collided with sonic"
        else:
            self.tiger.collisions = 0

        if result == "sonic's speed reduced":
            self.sonic.collisions += 1
            if self.sonic.collisions == 1:
                self.sonic.velocity[0] *= 0.8
            return result
        else:
            self.sonic.collisions = 0
    

