import threading

import random

import pygame
from pygame import Rect
from pygame.sprite import Group
from data.commands import load_image
from settings import *
from fruit import Fruit
from bomb import Bomb
import random


class Game:
    def __init__(self):
        self.fruits_group = Group()
        self.bomb_group = Group()
        self.fruit_spawn_timer = threading.Event()

    def base_game(self, screen):
        screen.fill((0, 0, 0))
        running = True
        clock = pygame.time.Clock()
        wait_for = 0
        is_cutting = False
        pygame.mouse.set_visible(False)
        mouse_sprite = pygame.sprite.Sprite()
        mouse_sprite.image = load_image('res/images/dsa.png')
        mouse_sprite.rect = mouse_sprite.image.get_rect()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        is_cutting = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        is_cutting = False
            screen.fill((0, 0, 0))
            if pygame.mouse.get_focused():
                mouse_sprite.rect.x, mouse_sprite.rect.y = pygame.mouse.get_pos()
            if not self.fruit_spawn_timer.is_set():
                threading.Timer(self.get_random_time(), self.spawn_fruits_group,
                                [self.fruit_spawn_timer]).start()
                self.fruit_spawn_timer.set()
            self.bomb_group.update()
            self.bomb_group.draw(screen)
            self.fruits_group.update()
            self.fruits_group.draw(screen)
            clock.tick(FPS)
            pygame.display.flip()
        pygame.quit()

    def spawn_fruits_group(self, args=None, kwargs=None):
        possible_amounts = (0, 1, 2, 3, 4, 5)
        weights = (1, 2, 3, 3, 2, 2)
        fruits_amount = random.choices(possible_amounts, weights=weights)[0]
        wants_bomb = random.randint(1, 4)
        for i in range(fruits_amount):
            fruit = Fruit()
            self.fruits_group.add(fruit)
        if wants_bomb == 1:
            bomb = Bomb()
            self.bomb_group.add(bomb)
        self.fruit_spawn_timer.clear()
        return fruits

    def get_random_time(self):
        return random.randrange(2, 3)


    def update(self):
        pass
