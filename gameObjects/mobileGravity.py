from . import Mobile
from FSMs import GravityFSM, AccelerationFSM

class MobileGravity(Mobile):
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.UD = GravityFSM(self)
        self.LR = AccelerationFSM(self)

    def update(self, seconds, colliders):
        self.UD.updateState()
        self.LR.updateState()

        super().update(seconds, colliders)

        #Handle collision with each item in colliders