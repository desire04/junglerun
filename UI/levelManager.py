from gameObjects.engine import GameEngine

class LevelManager(object):
    def __init__(self, numLevels=2):
        """Level manager that sets the appropriate game engine based on user input."""
        self.levels = [GameEngine(x) for x in range(numLevels+1)]
