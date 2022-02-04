import threading

import random

import pygame
from pygame.sprite import Group

from settings import *
from fruit import Fruit


class Game:
    def __init__(self):
        self.fruits_group = Group()
        self.fruit_spawn_timer = threading.Event()

    def base_game(self, screen):
        screen.fill((0, 0, 0))
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((0, 0, 0))

            if not self.fruit_spawn_timer.is_set():
                threading.Timer(self.get_random_time(), self.spawn_fruits_group,
                                [self.fruit_spawn_timer]).start()
                self.fruit_spawn_timer.set()

            self.fruits_group.update()
            self.fruits_group.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()

    def spawn_fruits_group(self, args=None, kwargs=None):
        possible_amounts = (0, 1, 2, 3, 4, 5)
        weights = (1, 2, 3, 3, 2, 2)
        fruits_amount = random.choices(possible_amounts, weights=weights)[0]
        for i in range(fruits_amount):
            fruit = Fruit()
            self.fruits_group.add(fruit)
        self.fruit_spawn_timer.clear()
        return fruits

    def get_random_time(self):
        return random.randrange(2, 3)
