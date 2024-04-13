import pygame, random
from . import Drawable, Sonic, Background, PowerUp, Tiger
from utils import vec, RESOLUTION, SoundManager

class GameEngine(object):
    """This class acts as the engine of the game and is the center 
    of the game's operation."""
    def __init__(self, level):
        self.loaded = False
        self.level = level
        self.sm = SoundManager.getInstance()
    
    def load(self): 
        """Load the game objects. The number of obstacles loaded depends on the 
        chosen difficulty level."""      
        if not self.loaded:
            self.sonic = Sonic((0,205))
            self.tiger = Tiger((-200, 170))
            self.size = vec(*RESOLUTION)
            self.background = Background((0,0))
            self.floor = pygame.Rect(0, 236, 100000000000000, 100)
            self.obstaclePositions = [200, 400, 600]
            self.rock1 = Drawable((self.obstaclePositions[0], 206), "mountain_small.png", (0,0))
            self.rock1.myRect = pygame.Rect(8, 25, 20, 5)
            if self.level == 1 or self.level == 2:
                self.rock2 = Drawable((self.obstaclePositions[2], 206), "mountain_wide.png", (0,0))
                self.rock2.myRect = pygame.Rect(8, 25, 30, 5)
                if self.level == 2:
                    self.tree1 = Drawable((self.obstaclePositions[1], 207), "trees.png", (0,0))
                    self.tree1.myRect = pygame.Rect(8, 20, 12, 5)
            self.shield = PowerUp((2000, 150), "bubbleshield.png", (0,0))
            self.shield.myRect = pygame.Rect(20, 20, 12, 5)
            self.shield.offset = vec(-12,-12)
            self.shieldOutline = pygame.Rect(400, 50, 100, 10)
            self.shieldIcon = Drawable((400, 50), "shields.png", (0,0))

            self.life = PowerUp((3000, 150), "sonicrings.png", (0,0))

            ch = self.sm.playBGM("Hot Pursuit.mp3")

            self.loaded = True
        
    def draw(self, drawSurface):
        """draw the loaded objects onto the screen. Some objects are drawn only if 
        certain conditions are met."""        
        self.background.draw(drawSurface)
        self.sonic.draw(drawSurface)
        self.tiger.draw(drawSurface)

        pygame.draw.rect(drawSurface, (205,135,65), self.floor)

        if self.sonic.hasAShield:
            drawSurface.blit(self.shieldIcon.image, (382, 40))
            pygame.draw.rect(drawSurface, (0,0,0), self.shieldOutline)
            pygame.draw.rect(drawSurface, (255,255,255), self.shieldIndicator)
    
        self.rock1.draw(drawSurface)
        if self.level == 1 or self.level == 2:
            self.rock2.draw(drawSurface)
            if self.level == 1:
                self.life.isActive = False
            if self.level == 2:
                self.tree1.draw(drawSurface)
            if self.life.isActive:
                self.life.draw(drawSurface)
            if self.shield.isActive:
                self.shield.draw(drawSurface)
            
    def handleEvent(self, event):
        """Pass event to the object's classes to handle"""
        self.sonic.handleEvent(event)
        self.tiger.handleEvent(event)
    
    def update(self, seconds):
        """Update the conditions of the game world based on detected collisions.
        Does too much heavy lifting. Better design practice would be to delegate 
        some collisions to other classes to be handled."""
        if self.level == 0:
            colliders = [self.rock1, self.floor]
        elif self.level == 1:
             colliders = [self.rock1, self.rock2, self.floor]
        elif self.level == 2:
             colliders = [self.rock1, self.tree1, self.rock2, self.floor]
    
        result = self.sonic.update(seconds, colliders)
        self.shield.update()
        self.background.update()
        self.tiger.update(seconds, colliders=None)

        offsetAmount = Drawable.CAMERA_OFFSET[0] + RESOLUTION[0]
        
        #update obstacles' positions to regenerate to the right of the screen when their position
        #is to the left of the screen.
        if self.level == 0:
            if self.rock1.position[0] + self.rock1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock1.position[0] = random.randint(offsetAmount + 50, offsetAmount + 200)

        elif self.level == 1:
            if self.rock1.position[0] + self.rock1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock1.position[0] = random.randint(offsetAmount + 100, offsetAmount + 250)

            if self.rock2.position[0] + self.rock2.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock2.position[0] = random.randint(offsetAmount + 350, offsetAmount + 500)

        elif self.level == 2:
            if self.rock1.position[0] + self.rock1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock1.position[0] = random.randint(100, 200) + self.rock2.position[0]

            if self.tree1.position[0] + self.tree1.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.tree1.position[0] = random.randint(150, 300) + self.rock1.position[0]

            if self.rock2.position[0] + self.rock2.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.rock2.position[0] = random.randint(200, 400) + self.tree1.position[0]

        Drawable.updateOffset(self.sonic, self.size)

        #update sonic and the shield when sonic has the shield
        if self.shield.doesCollide(self.sonic): 
            self.shieldIndicator = pygame.Rect(400, 53, 20*self.shield.timer, 5)
            self.shield.position = self.shield.offset + self.sonic.position
            self.sonic.hasAShield = True
            self.shield.timer -= seconds

            if self.shield.timer <= 0:
                self.shield.isActive = False

            
            if not self.shield.isActive:
                self.sonic.hasAShield = False
                if self.level == 1:
                    self.shield.position = vec(offsetAmount+10000+self.sonic.velocity[0], 150)
                elif self.level == 2:
                    self.shield.position = vec(offsetAmount+15000+self.sonic.velocity[0], 120)
                self.shield.resetTimer()
                self.shield.isActive = True
        #update the shield's position if sonic misses it and it is no longer visible
        else:
            if self.shield.position[0] + self.shield.myRect.width < Drawable.CAMERA_OFFSET[0]:
                if self.level == 1:
                    self.shield.position = vec(offsetAmount+5000, 150)
                elif self.level == 2:
                    self.shield.position = vec(offsetAmount+7500, 120)
            
        #update sonic and the life ring when sonic has the ring by passing information to the screen 
        #manager. 
        if self.life.doesCollide(self.sonic):
            self.life.isActive = False
            if not self.life.isActive or (self.life.position[0] + self.life.myRect.width) < Drawable.CAMERA_OFFSET[0]:
                self.life.position = vec(offsetAmount+15000+self.sonic.velocity[0], 150)
                self.life.isActive = True
            return "add life if needed"
        else:
            if self.life.position[0] + self.life.myRect.width < Drawable.CAMERA_OFFSET[0]:
                self.life.position = vec(offsetAmount+15000+self.sonic.velocity[0], 150)

        #update the tiger's velocity when it collides with sonic and send relevant information
        #to the screen manager. 
        if self.tiger.doesCollide(self.sonic):
            if not self.tiger.collisions:
                ch = self.sm.playSFX("Lion-roar-sound-effect.wav")
                self.tiger.collisions = True
                self.tiger.velocity[0] = self.sonic.velocity[0] * 0.8
                if not self.sonic.hasAShield:
                    return "tiger collided with sonic"
        else:
            self.tiger.collisions = False
        #update sonic's velocity when it collides with an obstacle and send relevant information to the
        #screen manager. 
        if result == "sonic's speed reduced":
            if not self.sonic.collisions:
                ch = self.sm.playSFX("Cell-phone-vibration-sound-effect.wav")
                self.sonic.collisions = True
                self.sonic.velocity[0] *= 0.8
                return result
        else:
            self.sonic.collisions = False
    

