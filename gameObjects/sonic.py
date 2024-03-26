from FSMs import RunningFSM, GravityFSM, AccelerationFSM
from utils import vec, RESOLUTION, rectAdd
from gameObjects import Drawable
from . import MobileGravity

from pygame.locals import *

import pygame
import numpy as np
from os.path import join


class Sonic(MobileGravity):
    def __init__(self, position):
        super().__init__(position, "sonicmodified1.png")

        self.framesPerSecond = 3
        self.nFrames = 4

        self.nFramesList = {
            "moving" : 3, 
            "standing" : 3,
            "jumping" : 3,
            "falling" : 3,

        }

        self.rowList = {
            "moving" : 1,
            "standing" : 0,
            "jumping" : 2,
            "falling" : 3
        }

        self.framesPerSecondList = {
            "moving" : 6,
            "standing" : 6,
            "jumping" : 6,
            "falling" : 6
        }

        self.FSManimated = RunningFSM(self)
        self.LR = AccelerationFSM(self, axis=0)
        self.UD = GravityFSM(self)

    def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.UD.jump()
            elif event.key == K_RIGHT:
                self.LR.increase()
        elif event.type == pygame.KEYUP:
            if event.key == K_RIGHT:
                self.LR.stop_increase()

    def update(self, seconds, colliders):
        resultUD = self.UD.update(seconds, colliders)
        resultLR = self.LR.update(seconds, colliders[0])

        super().update(seconds, colliders)

        if resultUD:
            return resultUD
        if resultLR:
            return resultLR

    def draw(self, drawSurface):
        super().draw(drawSurface)
    
    def colliderect(self, other):
        sonicHitBox = rectAdd(self.position, self.image.get_rect())
        
        
    def updateMovement(self):
        pass