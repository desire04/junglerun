from . import AbstractGameFSM
from statemachine import State


class ScreenManagerFSM(AbstractGameFSM):
    """Screen manager finite state machine that handles the different
    screen modes of the game."""
    homeMenu = State(initial=True)
    difficultyMenu = State()
    mainMenu = State()
    game     = State()
    paused   = State()
    gameOver = State()
    
    selectDifficulty = homeMenu.to(difficultyMenu)
    loadGame = difficultyMenu.to(mainMenu)
    pause = game.to(paused) | paused.to(game) | \
            mainMenu.to.itself(internal=True)
    
    startGame = mainMenu.to(game) 
    quitGame  = game.to(mainMenu) | \
                paused.to.itself(internal=True)
    
    restart = gameOver.to(mainMenu)
    
    endGame = game.to(gameOver) | gameOver.to.itself(internal=True)
    
    def isInGame(self):
        return self == "game" or self == "paused" or self == "gameOver"
    
    def on_enter_game(self):
        """load the game after the difficulty has been selected"""
        self.obj.game.load()
        self.obj.game.sonic.updateMovement()
    