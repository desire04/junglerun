import pygame
from FSMs import RunningFSM, GravityFSM, AccelerationFSM
from utils import rectAdd
from . import MobileGravity
from pygame.locals import *





class Sonic(MobileGravity):
    """Sonic's main class."""
    def __init__(self, position):
        """Initialize sonic's animation frames and the appropriate 
        finite state machines."""
        super().__init__(position, "sonicmodified1.png")

        self.framesPerSecond = 3
        self.nFrames = 4
        self.hasAShield = False
        self.collisions = False
        

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
        """Handle jumping based on user input"""
        if event.type == pygame.KEYDOWN:
            if event.key == K_UP:
                self.UD.jump()


    def update(self, seconds, colliders):
        """Send colliders to the finite state machines."""
        if len(colliders) == 2:
            resultUD = self.UD.update(seconds, colliders[1])
            resultLR = self.LR.update(seconds, [colliders[0]])
        elif len(colliders) == 3:
            resultUD = self.UD.update(seconds, colliders[2])
            resultLR = self.LR.update(seconds, [colliders[0], colliders[1]])
        elif len(colliders) == 4:
            resultUD = self.UD.update(seconds, colliders[3])
            resultLR = self.LR.update(seconds, [colliders[0], colliders[1], colliders[2]])

        super().update(seconds, colliders)

        if resultUD:
            return resultUD
        if resultLR:
            return resultLR

    def draw(self, drawSurface):
        super().draw(drawSurface)
    
    def colliderect(self):
        sonicHitBox = rectAdd(self.position, self.image.get_rect())
        
        
    def updateMovement(self):
        pass