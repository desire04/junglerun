from gameObjects import Drawable
from utils.vector import vec
from . import TextEntry 

class AbstractMenu(Drawable):
    def __init__(self, background, fontName="default",
                 color=(255,255,255)):
        super().__init__((0,0), background)

        self.options = {}

        self.color = color
        self.font = fontName

    def addOption(self, key, text, position, center=None):
        self.options[key] = TextEntry(position, text, self.font, self.color)
        optionSize = self.options[key].getSize()

        if center != None:
            if center == "both":
                offset = optionSize // 2
            elif center == "horizontal":
                offset = vec(optionSize[0] // 2, 0)
            elif center == "vertical":
                offset = vec(0, optionSize[1] // 2)
            else:
                offset = vec(0,0)

            self.options[key].position -= offset

    def draw(self, surface):
        super().draw(surface)

        for item in self.options.values():
            item.draw(surface)

class EventMenu(AbstractMenu):
    def __init__(self, background, fontName="default", color=(255,255,255)):
        super().__init__(background, fontName, color)
        self.eventMap = {}

    def addOption(self, key, text, position, eventLambda, center=None):
        super().addOption(key, text, position, center)
        self.eventMap[key] = eventLambda

    def handleEvent(self, event):
        for key in self.eventMap.keys():
            function = self.eventMap[key]
            if function(event):
                return key
            
class DifficultyMenu(AbstractMenu):
    """Difficulty menu that sends difficulty information to the screen manager
    based on user input."""
    def __init__(self, background, fontName="default", color=(255,255,255)):
        super().__init__(background, fontName, color)
        self.difficultyMap = {}

    def addOption(self, key, text, position, difficultyLambda, center=None):
        super().addOption(key, text, position, center)
        self.difficultyMap[key] = difficultyLambda

    def handleEvent(self, event):
        for key in self.difficultyMap.keys():
            difficulty = self.difficultyMap[key]
            if difficulty(event):
                return key
            

class HomeMenu(AbstractMenu):
    """Homescreen menu that sends information to the screen manager
    based on user input."""
    def __init__(self, background, fontName="default8", color=(255,255,255)):
        super().__init__(background, fontName, color)
        self.homeMap = {}

    def addOption(self, key, text, position, homeLambda, center=None):
        super().addOption(key, text, position, center)
        self.homeMap[key] = homeLambda

    def handleEvent(self, event):
        for key in self.homeMap.keys():
            menu = self.homeMap[key]
            if menu(event):
                return key