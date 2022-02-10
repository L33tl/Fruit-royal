import random

import pygame
from pygame import sprite, Rect
from general_classes import Slice
from data.exceptions import BadLoadImage
from data.commands import load_image
from settings import WIDTH, HEIGHT, Y_GRAVITY, FPS, SIZE

fruit_types = ['a', 'b', 'c', 'l', 'r', 'w'] * 3 + ['g']


class Fruit(sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.init()
        self.x = random.randint(20, WIDTH - 20)
        self.y = random.randint(HEIGHT, HEIGHT + 200)

        self.fruit = random.choice(fruit_types)
        if self.fruit == 'g':
            self.points = 5
        else:
            self.points = 1
        self.image = self.load_fruit_image(0)
        self.rect = Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
        self.mask = pygame.mask.from_surface(self.image)
        self.throwing_force = -1000
        self.x_velocity = random.randrange(*(-3, 0) if self.x >= WIDTH / 2 else (0, 3))
        self.was_above = False

    def update(self):
        x = self.rect.x
        y = self.rect.y

        self.throwing_force += Y_GRAVITY
        y += self.throwing_force / FPS

        x += self.x_velocity

        self.rect.x = x
        self.rect.y = y
        if self.rect.y < HEIGHT - self.image.get_width():
            self.was_above = True

    def draw(self, screen):
        screen.blit(self.image, self.rect.size)

    def load_fruit_image(self, number):
        path = 'res/sprites/fruits'
        try:
            return load_image(f'{path}/{self.fruit}/{self.fruit}{number}.png')
        except BadLoadImage as bli:
            print(bli)

    def cut(self):
        self.kill()
        first_coords = (self.rect.x + 5, self.rect.y - random.choice(range(1, 3)))
        second_coords = (self.rect.x - 5, self.rect.y - random.choice(range(1, 3)))
        return Slice(first_coords, random.choice(range(1, 3)), random.choice(range(1, 3)), self.fruit, 1), Slice(
            second_coords, random.choice(range(-3, -1)), random.choice(range(1, 3)), self.fruit, 2)
