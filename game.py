import random

import pygame
from pygame.sprite import Group

from settings import *
from fruit import Fruit


class Game:
    def __init__(self):
        self.fruits_group = Group()

    def base_game(self, screen):
        screen.fill((0, 0, 0))
        running = True
        clock = pygame.time.Clock()

        self.spawn_fruits_group()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))
            self.fruits_group.update()
            self.fruits_group.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()

    def spawn_fruits_group(self):
        possible_amounts = (0, 1, 2, 3, 4, 5)
        weights = (1, 2, 3, 3, 2, 2)
        fruits_amount = random.choices(possible_amounts, weights=weights)[0]
        print(fruits_amount)
        for i in range(fruits_amount):
            fruit = Fruit()
            self.fruits_group.add(fruit)

        return fruits
