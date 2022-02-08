import pygame
from pygame import Rect
from data.commands import load_image


class Blade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('res/images/dsa.png')
        self.is_cutting = False
        self.x, self.y = 0, 0
        self.rect = Rect(self.x, self.y, *self.image.get_size())
        self.mask = pygame.mask.from_surface(self.image)
