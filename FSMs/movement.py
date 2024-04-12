from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION, rectAdd
from statemachine import State
from gameObjects import Drawable


class MovementFSM(AbstractGameFSM):
    
    def __init__(self, obj):
        super().__init__(obj)

    def update(self, seconds):
        super().update(seconds)
        #handle collisions here


class AccelerationFSM(MovementFSM):

    not_moving = State(initial=True)
    uniform_motion = State()
    positive = State()

    increase = not_moving.to(positive) | uniform_motion.to(positive)
    stop_increase = positive.to(uniform_motion) | uniform_motion.to.itself(internal=True)

    def __init__(self, obj, axis=0):
        self.axis = axis
        self.direction = vec(0,0)
        self.direction[self.axis] = 1
        self.accel = 3

        super().__init__(obj)

    def updateState(self):
        if self == "positive" and self.obj.position[0] % 1000 != 0:
            self.stop_increase()
        elif self.isNotAccelerating() and self.obj.position[0] % 1000 == 0:
            self.increase()

    def isAccelerating(self):
        return self.accel > 0
    
    def isNotAccelerating(self):
        return self.accel == 0
    
    def update(self, seconds=0, colliders=None):
        if self == "uniform_motion":
            self.accel = 0
        elif self == "positive":
            self.accel = 10
        self.obj.velocity += self.direction * self.accel * seconds
        self.obj.velocity[0] = min(self.obj.maxVelocity, self.obj.velocity[0])
        self.obj.UD.gravity = magnitude(self.obj.velocity) * 1.5
        if colliders:
            for item in colliders:
                if item.doesCollide(self.obj) and not self.obj.hasAShield:
                    return "sonic's speed reduced"
                else:
                    shield = colliders[len(colliders)-1]
                    shield.isAttached = False
                    self.obj.hasAShield = False
                    colliders.pop(len(colliders)-1)

        super().update(seconds)

class GravityFSM(MovementFSM):
    def __init__(self, obj):
        super().__init__(obj)
        self.jumpTimer = 0
        self.gravity = 150
        self.jumpSpeed = 100
        self.jumpCounter = 0
        self.maxjumps = 3
        #jump counter
        self.jumpTime = 0.1

    grounded = State(initial=True)
    jumping = State()
    falling = State()


    jump = grounded.to(jumping) | falling.to(jumping, cond="canJumpAgain") \
            | jumping.to.itself(cond="canJumpAgain") | jumping.to.itself(internal=True) |  falling.to.itself(internal=True) 
    fall = jumping.to(falling) | grounded.to(falling) 
    land = falling.to(grounded) | jumping.to(grounded)

    def updateState(self):
        if self.canFall() and self == "jumping":
            self.fall()
        #elif self.cannotFall() and self.canJumpAgain() and self == "moving":
            #self.jump()
    

    def canFall(self):
        return self.jumpTimer < 0
    
    def cannotFall(self):
        return self.jumpTimer > 0
    
    def canJumpAgain(self):
        return self.jumpCounter < self.maxjumps
    
    def on_enter_jumping(self):
        self.jumpCounter += 1
        self.jumpTimer = self.jumpTime

    def update(self, seconds=0, colliders=None):
        if self == "falling":
            self.obj.velocity[1] += self.gravity * seconds
            hitBox = rectAdd(self.obj.position, self.obj.image.get_rect())
            if colliders.colliderect(hitBox):
                    #get clip rect; subtract height of clip rect from y position of sonic
                if self.obj.position[1] < 236:
                    self.land()
                    self.jumpCounter = 0
            #check to see if i should transition to grounded
        elif self == "jumping":
            self.obj.velocity[1] = -self.jumpSpeed
            self.jumpTimer -= seconds
        else:
            self.obj.velocity[1] = 0
            self.jumpCounter = 0