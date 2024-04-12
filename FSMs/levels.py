from . import AbstractGameFSM
from statemachine import State

class LevelFSM(AbstractGameFSM):
    loading = State(initial=True)
    activeLevel = State()

    nextLevel = activeLevel.to(loading)
    loadLevel = loading.to(activeLevel, cond="isLoaded") | \
                loading.to.itself(internal=True)
    
    def __init__(self, obj, maxLevels):
        self.currentLevel = -1
        self.maxLevels = maxLevels
        super().__init__(obj)

    def isLoaded(self):
        return True
    
    def on_enter_loading(self):
        if self.currentLevel < self.maxLevels - 1:
            self.currentLevel += 1

