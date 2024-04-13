from utils import vec
from . import Drawable


class PowerUp(Drawable):
    """This class provides a framework for the behaviors of
    powerups i.e shields and life rings."""
    def __init__(self, position=vec(2000,150), fileName="", offset=(0,0)):
        super().__init__(position, fileName, offset)
        self.isCollided = False
        self.isActive = True
        self.timer = 5

    def draw(self, drawSurface):
        super().draw(drawSurface)
    
    def update(self):
        pass

    def resetTimer(self):
        self.timer = 5
 
