import pygame

from . import Drawable, Sonic, Background

from utils import vec, RESOLUTION

class GameEngine(object):

    def __init__(self):       
        self.sonic = Sonic((0,205))
        self.size = vec(*RESOLUTION)
        self.background = Background((0,0))
        self.floor = pygame.Rect(0, 236, 100000000000000, 100)
        self.rock = Drawable((70, 206), "mountain_small.png", (0,0))
        self.rock.myRect = pygame.Rect(78, 231, 20, 5)
        #self.rock2 = Drawable((230, 206), "mountain_small.png", (0,0))
        #self.tree1 = Drawable((250, 400), "trees.png", (0,0))
        
    
    def draw(self, drawSurface):        
        self.background.draw(drawSurface)
        
        self.sonic.draw(drawSurface)

        pygame.draw.rect(drawSurface, (205,135,65), self.floor)
        
        self.rock.draw(drawSurface)

        #for i in range(1, 2001, 200):
            #self.rock = Drawable((70+i, 206), "mountain_small.png", (0,0))
            #self.rock.draw(drawSurface)
        #self.rock2.draw(drawSurface)

        #self.tree1.draw(drawSurface)

            
    def handleEvent(self, event):
        self.sonic.handleEvent(event)
    
    def update(self, seconds):
        colliders = [self.rock.myRect, self.floor]
        result = self.sonic.update(seconds, colliders)
        self.background.update()
        
        
        Drawable.updateOffset(self.sonic, self.size)

        if result:
            return result
    

