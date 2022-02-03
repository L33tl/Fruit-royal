import pygame
from settings import *


class Game:
    def __init__(self):
        pass

    def base_game(self, screen):
        screen.fill((0, 0, 0))
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()
