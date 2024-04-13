from . import Mobile
from FSMs import GravityFSM, AccelerationFSM

class MobileGravity(Mobile):
    """This class provides a framework that handles the behaviors of objects
    that move with gravity."""
    def __init__(self, position, fileName=""):
        """Initialize the appropriate finite state machines"""
        super().__init__(position, fileName)
        self.UD = GravityFSM(self)
        self.LR = AccelerationFSM(self)

    def update(self, seconds, colliders):
        """Delegate collision handling to the finite state machine"""
        self.UD.updateState()
        self.LR.updateState()

        super().update(seconds, colliders)
