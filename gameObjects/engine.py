import pygame

from . import Drawable, Sonic

from utils import vec, RESOLUTION

class GameEngine(object):

    def __init__(self):       
        self.sonic = Sonic((0,403))
        self.size = vec(*RESOLUTION)
        self.background = Drawable((0,0), "JungleRunBackground.png")
        self.floor = pygame.Rect(0, 436, 500, 100)
        self.rock = Drawable((150, 405), "mountain_small.png", (0,0))
        #self.rock2 = Drawable((300, 400), "mountain_wide.png")
        #self.tree1 = Drawable((250, 400), "trees.png", (0,0))
        
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.sonic.draw(drawSurface)

        pygame.draw.rect(drawSurface, (205,135,65), self.floor)

        self.rock.draw(drawSurface)
        #self.rock2.draw(drawSurface)

        #self.tree1.draw(drawSurface)

            
    def handleEvent(self, event):
        self.sonic.handleEvent(event)
    
    def update(self, seconds):
        colliders = [self.floor]
        self.sonic.update(seconds, colliders)
        
        Drawable.updateOffset(self.sonic, self.size)
    

