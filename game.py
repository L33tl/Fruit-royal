import threading

import random
from datetime import datetime, timedelta
import pygame
from pygame import Rect
from pygame.sprite import Group
from data.commands import load_image
from settings import *
from fruit import Fruit
from general_classes import Blade
from bomb import Bomb
import random


class Game:
    def __init__(self):
        self.fruits_group = Group()
        self.bomb_group = Group()
        self.fruit_spawn_timer = threading.Event()
        self.blade = Blade()
        self.result = 0
        self.last_fruit = datetime.now()

    def base_game(self, screen):
        screen.fill((0, 0, 0))
        running = True
        clock = pygame.time.Clock()
        last_fruit = datetime.now()
        pygame.mouse.set_visible(False)
        mouse_pos = (0, 0)
        f1 = pygame.font.Font(None, 50)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.blade.is_cutting = True
                    if event.button == 3:
                        self.blade.is_rotating = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.blade.is_cutting = False
                    if event.button == 3:
                        self.blade.is_rotating = False
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
            screen.fill((0, 0, 0))
            score = f1.render(str(self.result), True,
                              (180, 0, 0))
            self.blade.rect.x, self.blade.rect.y = mouse_pos
            if not self.fruit_spawn_timer.is_set():
                threading.Timer(self.get_random_time(), self.spawn_fruits_group,
                                [self.fruit_spawn_timer]).start()
                self.fruit_spawn_timer.set()
            collision_res = self.check_collision()
            if collision_res is False:
                break
            self.bomb_group.update()
            self.bomb_group.draw(screen)
            self.fruits_group.update()
            self.fruits_group.draw(screen)
            self.blade.draw(screen, mouse_pos)
            screen.blit(score, (0, 0))
            clock.tick(FPS)
            pygame.display.flip()

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

    def check_collision(self):
        fruit: Fruit
        answer = 0
        for bomb in self.bomb_group:
            if pygame.sprite.collide_mask(self.blade, bomb) and self.blade.is_cutting:
                return False
        for fruit in self.fruits_group:
            if pygame.sprite.collide_mask(fruit, self.blade) and self.blade.is_cutting:
                if (datetime.now() - self.last_fruit).seconds <= 0.5:
                    self.result += 1
                self.result += 1
                fruit.cut()
                self.last_fruit = datetime.now()
                answer += 1
        return answer
