from utils import vec, RESOLUTION
from . import Drawable

class Background(Drawable):
    #background's position
    def __init__(self, position):
        super().__init__(position, "JungleRunBackground3.png")

    def draw(self, drawSurface):
        super().draw(drawSurface)

    def update(self):
        if Drawable.CAMERA_OFFSET[0] - self.position[0] >= 1600:
            self.position[0] += 1600

    #ask her about it again. Right now, just set it to a very large number. 
