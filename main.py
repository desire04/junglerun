
import pygame
from UI import ScreenManager
from utils import RESOLUTION, UPSCALED

def main():
    pygame.init()

    screen = pygame.display.set_mode(list(map(int, UPSCALED)))
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))

    gameEngine = ScreenManager()

    RUNNING = True
    
    while RUNNING:
        gameEngine.draw(drawSurface)

        pygame.transform.scale(drawSurface, list(map(int, UPSCALED)), screen)

        pygame.display.flip()

        gameClock = pygame.time.Clock()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                RUNNING = False
            else:
                result = gameEngine.handleEvent(event)

                if result == "exit":
                    RUNNING = False

        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000
        gameEngine.update(seconds)

    pygame.quit()

if __name__ == '__main__':
    main()