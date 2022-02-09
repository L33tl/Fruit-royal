import pygame
from pygame import Rect
from data.commands import load_image
from settings import *


class Blade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('res/images/dsa.png')
        self.is_cutting = False
        self.x, self.y = 0, 0
        self.rect = Rect(self.x, self.y, *self.image.get_size())
        self.mask = pygame.mask.from_surface(self.image)
        self.is_rotating = False
        self.angle = 0

    def draw(self, screen, mouse_pos):
        if self.is_rotating:
            self.image, self.rect = self.rot_center(self.image, self.rect, 1)
        screen.blit(self.image, (
            min(WIDTH - self.image.get_width(), mouse_pos[0]),
            min(HEIGHT - self.image.get_height(), mouse_pos[1])))

    def rot_center(self, image, rect, angle):
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = rot_image.get_rect(center=rect.center)
        return rot_image, rot_rect
