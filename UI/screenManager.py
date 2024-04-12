from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu, DifficultyMenu, LevelManager
from utils import vec, RESOLUTION
from gameObjects.engine import GameEngine
from gameObjects import Drawable

from pygame.locals import *

class ScreenManager(object):

    def __init__(self):
        self.level =  LevelManager() #level manager here 
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        self.gameOverText = TextEntry(vec(0,0), "GAME OVER!")
        self.score = 0
        self.lives = Drawable((400,20), "sonicrings.png", (0,0))
        self.scoreText = TextEntry(vec(450,0), "Score: " + str(self.score))
        self.livesText = TextEntry(vec(450, 0), "Lives: ")
        self.screenSize = vec(*RESOLUTION)

        pausedTextSize = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - pausedTextSize
        self.pausedText.position = vec(*midpoint)

        gameOverTextSize = self.gameOverText.getSize()
        midpoint = RESOLUTION // 2 -  gameOverTextSize
        self.gameOverText.position = vec(*midpoint)
        

        self.mainMenu = EventMenu("JungleRunBackground.png", fontName="default8")
        self.mainMenu.addOption("start", "Press S to start", 
                                RESOLUTION // 2 - vec(0,50), 
                                lambda x: x.type == KEYDOWN and x.key == K_s, 
                                center="both")
        self.mainMenu.addOption("exit", "Press Q to quit", 
                                RESOLUTION // 2 + vec(0,50),
                                lambda x: x.type == KEYDOWN and x.key == K_q, 
                                center="both")
        
        self.difficultyMenu = DifficultyMenu("JungleMainMenuBackground.png", fontName="default8")
        self.difficultyMenu.addOption("easy", "Press E for easy", 
                                      RESOLUTION // 2 - vec(0,50), 
                                      lambda x: x.type == KEYDOWN and x.key == K_e, 
                                      center="both")
        self.difficultyMenu.addOption("medium", "Press M for medium", 
                                        RESOLUTION // 2, 
                                        lambda x: x.type == KEYDOWN and x.key == K_m, 
                                        center="both")
        self.difficultyMenu.addOption("hard", "Press H for hard", 
                                      RESOLUTION // 2 + vec(0,50), 
                                      lambda x: x.type == KEYDOWN and x.key == K_h, 
                                      center="both")
        
    def draw(self, drawSurf):
        if self.state.isInGame():
            self.game.draw(drawSurf)
            drawSurf.blit(self.scoreText.image, (300,0))
            drawSurf.blit(self.livesText.image, (300, 25))
            if self.game.level == 0:
                for i in range(self.livesCount):
                    drawSurf.blit(self.lives.image, (400+(20*i), 18))

            if self.state == "paused":
                self.pausedText.draw(drawSurf)
            
            elif self.state == "gameOver":
                drawSurf.blit(self.gameOverText.image, (200, 150))

        elif self.state == "mainMenu":
            self.mainMenu.draw(drawSurf)
        
        elif self.state == "difficultyMenu":
            self.difficultyMenu.draw(drawSurf)


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
        elif self.state == "difficultyMenu":
            choice = self.difficultyMenu.handleEvent(event)
            if choice == "easy":
                self.game = self.level.levels[0]
                self.livesCount = 3
                self.state.loadGame()
            elif choice == "medium":
                self.game = self.level.levels[1]
                self.livesCount = 2
                self.state.loadGame()
            elif choice == "hard":
                self.game = self.level.levels[2]
                self.livesCount = 2
                self.state.loadGame()
        elif self.state == "gameOver":
            if event.type == KEYDOWN and event.key == K_r:
                self.state.restart()
                Drawable.CAMERA_OFFSET = vec(0,0)
                #reset everything
                #self.game = GameEngine()
            
    def update(self, seconds):
        if self.state == "game":
            self.score += 1
            font = self.scoreText.getFont()
            self.scoreText.image = font.render("Score: " + str(self.score), True, self.scoreText.color)
            action = self.game.update(seconds)
            if action == "tiger collided with sonic":
                    self.livesCount -= 1
                    if self.livesCount == 0:
                        self.state.endGame()
        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
        elif self.state == "difficultyMenu":
            self.difficultyMenu.update(seconds)