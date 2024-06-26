from gameObjects import Drawable
import pygame
import os

class TextEntry(Drawable):
    if not pygame.font.get_init():
        pygame.font.init()

    FONT_FOLDER = "fonts"
    DEFAULT_FONT = "PressStart2P.ttf"
    DEFAULT_SIZE = 16
    FONTS = {
        "default" : pygame.font.Font(os.path.join(FONT_FOLDER, 
                                    DEFAULT_FONT), DEFAULT_SIZE),
        "default8" : pygame.font.Font(os.path.join(FONT_FOLDER, 
                                    DEFAULT_FONT), 8)
    }

    def __init__(self, position, text, font="default", color=(255,255,255)):
        super().__init__(position, "")
        self.color = color
        self.font = font

        self.image = TextEntry.FONTS[self.font].render(text, False, self.color)

    def getFont(self):
        return TextEntry.FONTS[self.font]