from FSMs import RunningFSM, AccelerationFSM
from utils import vec, RESOLUTION, rectAdd
from gameObjects import Drawable
from . import MobileGravity

from pygame.locals import *

import pygame
import numpy as np
from os.path import join

class Tiger(MobileGravity):
    def __init__(self, position):
        super().__init__(position, "newtiger.png")
        
        self.framesPerSecond = 3
        self.nFrames = 1
        self.collisions = 0
        self.hasCollided = False

        self.nFramesList = {
            "moving" : 3,
            "standing" : 1
        }

        self.rowList = {
            "moving" : 1,
            "standing" : 0
        }

        self.framesPerSecondList = {
            "moving" : 9,
            "standing" : 1
        }

        self.FSManimated = RunningFSM(self)
        self.LR = AccelerationFSM(self, axis=0)


    def handleEvent(self, event):
        super().handleEvent(event)

    def update(self, seconds, colliders=None):
        self.LR.update(seconds, colliders)

        super().update(seconds, colliders)

    def draw(self, drawSurface):
        super().draw(drawSurface)