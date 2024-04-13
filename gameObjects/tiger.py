from FSMs import RunningFSM, AccelerationFSM
from . import MobileGravity
from pygame.locals import *


class Tiger(MobileGravity):
    """Tiger's main class."""
    def __init__(self, position):
        """Set tiger's animation frames and initialize the appropriate finite state machines."""
        super().__init__(position, "newtiger.png")
        
        self.framesPerSecond = 3
        self.nFrames = 1
        self.collisions = False
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
        "Send colliders to finite state machines to be updated"
        self.LR.update(seconds, colliders)
        super().update(seconds, colliders)

    def draw(self, drawSurface):
        super().draw(drawSurface)