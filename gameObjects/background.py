from utils import vec, RESOLUTION
from . import Drawable

class Background(Drawable):
    def __init__(self, position):
        super().__init__(position, "JungleRunBackground3.png")

    def draw(self, drawSurface):
        super().draw(drawSurface)

    def update(self, sonic):
        if sonic.position[0] > 0 and (sonic.position[0] - RESOLUTION[0]) % RESOLUTION[0] == 0:
            sonic.position[0] += RESOLUTION[0]

    
