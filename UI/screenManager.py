from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu
from utils import vec, RESOLUTION
from gameObjects.engine import GameEngine
from gameObjects import Drawable

from pygame.locals import *

class ScreenManager(object):

    def __init__(self):
        self.game = GameEngine()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        self.gameOverText = TextEntry(vec(0,0), "GAME OVER!")
        self.score = 0
        self.scoreText = TextEntry(vec(250+Drawable.CAMERA_OFFSET[0],0+Drawable.CAMERA_OFFSET[1]), "Score: " + str(self.score))
        self.screenSize = vec(*RESOLUTION)

        pausedTextSize = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - pausedTextSize
        self.pausedText.position = vec(*midpoint)

        gameOverTextSize = self.gameOverText.getSize()
        midpoint = RESOLUTION // 2 -  gameOverTextSize
        self.gameOverText.position = vec(*midpoint)
        

        self.mainMenu = EventMenu("JungleMainMenuBackground.png", fontName="default8")
        self.mainMenu.addOption("start", "Press S to start", 
                                RESOLUTION // 2 - vec(0,50), 
                                lambda x: x.type == KEYDOWN and x.key == K_s, 
                                center="both")
        self.mainMenu.addOption("exit", "Press Q to quit", 
                                RESOLUTION // 2 + vec(0,50),
                                lambda x: x.type == KEYDOWN and x.key == K_q, 
                                center="both")
        
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
            drawSurf.blit(self.scoreText.image, (200,0))

            if self.state == "paused":
                self.pausedText.draw(drawSurf)
            
            elif self.state == "gameOver":
                self.gameOverText.draw(drawSurf)

        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)


    def handleEvent(self, event):
        if self.state in ["game", "paused"]:
            if event.type == KEYDOWN and event.key == K_q:
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.game.handleEvent(event)

        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)

            if choice == "start":
                self.state.startGame()
            elif choice == "exit":
                return "exit"
            
    def update(self, seconds):
        #Drawable.updateOffset(self.gameOverText, self.screenSize)
        #Drawable.updateOffset(self.scoreText, self.screenSize)
        if self.state == "game":
            self.score += 1
            action = self.game.update(seconds)
            if action:
                self.state.endGame()
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)