from . import Drawable

class Background(Drawable):
    """This class handles the background's behavior"""
    def __init__(self, position):
        super().__init__(position, "JungleRunBackground3.png")

    def draw(self, drawSurface):
        super().draw(drawSurface)

    def update(self):
        """Update the background's position if the trackable object has moved
        beyond the image's width."""
        if Drawable.CAMERA_OFFSET[0] - self.position[0] >= 1600:
            self.position[0] += 1600

