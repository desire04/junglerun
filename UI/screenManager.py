from FSMs import ScreenManagerFSM
from . import TextEntry, EventMenu, DifficultyMenu, LevelManager, HomeMenu
from utils import vec, RESOLUTION, SoundManager
from gameObjects import Drawable
from pygame.locals import *

class ScreenManager(object):
    """The screen manager class that acts as the brain of the game. It sends
    and receives appropriate information to and from the game manager """
    def __init__(self):
        """Initialize the level manager and necessary information to be drawn
        on the screen."""
        self.level =  LevelManager()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        self.gameOverText = TextEntry(vec(0,0), "GAME OVER!")
        self.score = 0
        self.lives = Drawable((400,20), "sonicrings.png", (0,0))
        self.scoreText = TextEntry(vec(450,0), "Score: " + str(self.score))
        self.livesText = TextEntry(vec(450, 0), "Lives: ")
        self.mainScreenText = TextEntry(vec(450, 0), "JUNGLE RUN")
        self.screenSize = vec(*RESOLUTION)
        self.sm = SoundManager.getInstance()
        ch = self.sm.playBGM("Screen Saver.mp3")
        
        self.homeScreen = HomeMenu("JungleMainMenuBackground.png", fontName="default")
        self.homeScreen.addOption("display", "JUNGLE RUN", 
                                RESOLUTION // 2 - vec(0,50), 
                                lambda x: x.type == KEYDOWN and x.key == K_F1, 
                                center="both")
        self.homeScreen.addOption("enter", "Press Enter to select levels", 
                                RESOLUTION // 2 + vec(0,50),
                                lambda x: x.type == KEYDOWN and x.key == K_RETURN, 
                                center="both")
        
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
        """Draw things on the screen based on the screen manager's state."""
        if self.state.isInGame():
            self.game.draw(drawSurf)
            drawSurf.blit(self.scoreText.image, (300,0))
            drawSurf.blit(self.livesText.image, (300, 25))
            for i in range(self.livesCount):
                drawSurf.blit(self.lives.image, (400+(20*i), 18))

            if self.state == "paused":
                drawSurf.blit(self.pausedText.image, (200, 150))
            
            elif self.state == "gameOver":
                drawSurf.blit(self.gameOverText.image, (200, 150))
        elif self.state == "homeMenu":
            self.homeScreen.draw(drawSurf)
        elif self.state == "mainMenu":
            Drawable.CAMERA_OFFSET = vec(0,0)
            self.mainMenu.draw(drawSurf)
        elif self.state == "difficultyMenu":
            self.difficultyMenu.draw(drawSurf)


    def handleEvent(self, event):
        """Change the state of the game based on the event or 
        delegate the event to the game engine."""
        if self.state in ["game", "paused"]:
            if event.type == KEYDOWN and event.key == K_q:
                Drawable.CAMERA_OFFSET = vec(0,0)
                self.livesCount = self.maxLives
                self.score = 0
                self.game = self.level.levels[self.levelNum]
                self.game.loaded = False
                self.game.load()
                self.state.quitGame()
            elif event.type == KEYDOWN and event.key == K_p:
                self.state.pause()
            else:
                self.game.handleEvent(event)

        elif self.state == "homeMenu":
            choice = self.homeScreen.handleEvent(event)
            if choice == "enter":
                self.state.selectDifficulty()
    
        elif self.state == "mainMenu":
            choice = self.mainMenu.handleEvent(event)
            if choice == "start":
                self.state.startGame()
            elif choice == "exit":
                return "exit"
        
        elif self.state == "difficultyMenu":
            choice = self.difficultyMenu.handleEvent(event)
            if choice == "easy":
                self.levelNum = 0
                self.game = self.level.levels[0]
                self.livesCount = self.maxLives = 4
                self.state.loadGame()
            elif choice == "medium":
                self.levelNum = 1
                self.game = self.level.levels[1]
                self.livesCount = self.maxLives = 3
                self.state.loadGame()
            elif choice == "hard":
                self.levelNum = 2
                self.game = self.level.levels[2]
                self.livesCount = self.maxLives = 2
                self.state.loadGame()

        elif self.state == "gameOver":
            if event.type == KEYDOWN and event.key == K_r:
                Drawable.CAMERA_OFFSET = vec(0,0)
                self.livesCount = self.maxLives
                self.score = 0
                self.game = self.level.levels[self.levelNum]
                self.game.loaded = False
                self.game.load()
                self.state.restart()

            
    def update(self, seconds):
        """Update the state of the game based on time passed or
        results obtained from the game engine."""
        if self.state == "game":
            self.score += 1
            font = self.scoreText.getFont()
            self.scoreText.image = font.render("Score: " + str(self.score), True, self.scoreText.color)
            action = self.game.update(seconds)
            if action == "tiger collided with sonic":
                    self.livesCount -= 1
                    if self.livesCount == 0:
                        self.state.endGame()
            elif action == "add life if needed" and self.livesCount < self.maxLives:
                self.livesCount += 1

        elif self.state == "homeMenu":
            self.homeScreen.update(seconds)

        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)

        elif self.state == "difficultyMenu":
            self.difficultyMenu.update(seconds)