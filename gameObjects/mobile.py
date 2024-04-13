from . import Animated
from utils import vec, magnitude, scale

class Mobile(Animated):
    """This class serves as the framework for the behaviors of mobile objects
    i.e sonic and tiger."""
    def __init__(self, position, fileName=""):
        super().__init__(position, fileName)
        self.velocity = vec(50,0)
        self.acceleration = 3
        self.maxVelocity = 500
    
    def update(self, seconds, colliders):
        """Update the object's position based on its velocity"""
        super().update(seconds, colliders)
        if magnitude(self.velocity) > self.maxVelocity:
            self.velocity = scale(self.velocity, self.maxVelocity)
        self.position += self.velocity * seconds