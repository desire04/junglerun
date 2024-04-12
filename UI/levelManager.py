import pygame

from gameObjects.engine import GameEngine
from FSMs import LevelFSM

class LevelManager(object):
    def __init__(self, numLevels=2):
        self.levels = [GameEngine(x) for x in range(numLevels+1)]
        self.state = LevelFSM(self, numLevels)

    def update(self, seconds):
        if self.state == "activeLevel":
            self.levels[self.state.currentLevel].update(seconds)
        else:
            self.state.loadLevel()

    def handleEvent(self, event):
        if self.state == "activeLevel":
            self.levels[self.state.currentLevel].handleEvent(event)
            #change this condition later
            if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
                self.state.nextLevel()

    def draw(self, drawSurface):
        if self.state == "activeLevel":
            self.levels[self.state.currentLevel].draw(drawSurface)