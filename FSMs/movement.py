from . import AbstractGameFSM
from utils import vec, magnitude, EPSILON, scale, RESOLUTION, rectAdd
from statemachine import State


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
    stop_increase = positive.to(uniform_motion)

    def __init__(self, obj, axis=0):
        self.axis = axis
        self.direction = vec(0,0)
        self.direction[self.axis] = 1
        self.accel = 100

        super().__init__(obj)

    def update(self, seconds=0):
        if self == "positive" or self == "uniform_motion":
            self.obj.velocity += self.direction * self.accel * seconds

        super().update(seconds)

class GravityFSM(MovementFSM):
    def __init__(self, obj):
        super().__init__(obj)
        self.jumpTimer = 0
        self.gravity = 200
        self.jumpSpeed = 65
        self.jumpTime = 0.1

    grounded = State(initial=True)
    jumping = State()
    falling = State()


    jump = grounded.to(jumping) | falling.to.itself(internal=True)
    fall = jumping.to(falling) | grounded.to(falling)
    land = falling.to(grounded) | jumping.to(grounded)

    def updateState(self):
        if self.canFall() and self == "jumping":
            self.fall()
        elif self.cannotFall() and self == "moving":
            self.jump()

    def canFall(self):
        return self.jumpTimer < 0
    
    def cannotFall(self):
        return self.jumpTimer > 0
    
    def on_enter_jumping(self):
        self.jumpTimer = self.jumpTime

    def update(self, seconds=0, colliders=None):
        if self == "falling":
            self.obj.velocity[1] += self.gravity * seconds
            hitBox = rectAdd(self.obj.position, self.obj.image.get_rect())
            for item in colliders:
                if item.colliderect(hitBox):
                    #get clip rect; subtract height of clip rect from y position of sonic
                    if self.obj.position[1] < 436:
                        self.land()
            #check to see if i should transition to grounded
        elif self == "jumping":
            self.obj.velocity[1] = -self.jumpSpeed
            self.jumpTimer -= seconds
        else:
            self.obj.velocity[1] = 0