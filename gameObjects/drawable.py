import pygame
from utils import SpriteManager, SCALE, RESOLUTION, vec

class Drawable(object):
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        for i in range(2):
            offset[i] = int(max(0,offset[i]))
        offset[1] = 0                            
        cls.CAMERA_OFFSET = offset
        
        

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None):
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
            self.myRect = self.image.get_rect()
       
        self.position  = vec(*position)
        self.imageName = fileName
        
    
    def draw(self, drawSurface):
        drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
            
    def getSize(self):
        return vec(*self.image.get_size())
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
    
    
    def getCollisionRect(self):
        newRect = pygame.Rect(self.myRect)
        newRect.left = int(self.position[0]+newRect.left)
        newRect.top = int(self.position[1]+newRect.top)
        return newRect

    def doesCollide(self, other):
        return self.getCollisionRect().colliderect(other.getCollisionRect())   
    
    def doesCollideList(self, others):
        rects = [r.getCollisionRect() for r in others]
        return self.getCollisionRect().collidelist(rects)   