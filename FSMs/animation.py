from . import AbstractGameFSM
from utils import magnitude, EPSILON, SpriteManager
from statemachine import State

class AnimateFSM(AbstractGameFSM):
    def on_enter_state(self):
        """set the suitable animation frame"""
        state = self.current_state.id
        if self.obj.row != self.obj.rowList[state]:
            self.obj.nFrames = self.obj.nFramesList[state]
            self.obj.frame = 0
            self.obj.row = self.obj.rowList[state]
            self.obj.framesPerSecond = self.obj.framesPerSecondList[state]
            self.obj.animaionTimer = 0
            self.obj.image = SpriteManager.getInstance().getSprite(self.obj.imageName,
                                                                   (self.obj.frame, self.obj.row))
            
class RunningFSM(AnimateFSM):
    standing = State(initial=True)
    moving = State()
    falling = State()
    jumping = State()

    move = standing.to(moving)
    jump = moving.to(jumping) | falling.to.itself(internal=True)
    fall = jumping.to(falling) | moving.to(falling)
    land = falling.to(moving, cond="hasVelocity") | falling.to(standing, cond="noVelocity") \
           | jumping.to(moving, cond="hasVelocity") | jumping.to(standing, cond="noVelocity")
    stop = moving.to(standing)

    def updateState(self):
        """update animation based on current state and intended next state"""
        if self.isJumping() and self != "jumping":
            self.jump()
        elif self.isFalling() and self != "falling":
            self.fall()
        elif self.hasVelocity() and self not in ["moving", "falling", "jumping"]:
            self.move()
        elif self.isGrounded() and self not in ["standing", "moving"]:
            self.land()
        elif self.noVelocity() and self not in ["standing", "falling", "jumping"]:
            self.stop()

    def hasVelocity(self):
        """check if the object is moving"""
        return magnitude(self.obj.velocity) > EPSILON


    def isJumping(self):
        """check if the object is jumping"""
        return self.obj.velocity[1] < -EPSILON
    
    def isFalling(self):
        """check if the object is falling"""
        return self.obj.velocity[1] > EPSILON
    
    def isGrounded(self):
        """check if the object is on the ground"""
        return not self.isFalling() and not self.isJumping()
    
    def noVelocity(self):
        """check if the object is not moving"""
        return not self.hasVelocity()
    
