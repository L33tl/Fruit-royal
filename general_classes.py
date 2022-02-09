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
            self.image, self.rect = self.rot_center(self.image, 1, mouse_pos)
        screen.blit(self.image, (
            min(WIDTH - self.image.get_width(), mouse_pos[0]),
            min(HEIGHT - self.image.get_height(), mouse_pos[1])))

    def rot_center(self, image_ex, angle, coords):
        rotated_image = pygame.transform.rotate(image_ex, angle)
        new_rect = rotated_image.get_rect(center=image_ex.get_rect(center=coords).center)
        return rotated_image, new_rect


class Slice(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, fruit_type, side_type):
        super().__init__()
        self.image = load_image(f"res/sprites/fruits/{fruit_type}/{fruit_type}_slice{side_type}.png")
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = PART_GRAVITY

    def update(self):
        self.velocity[1] += self.gravity / FPS
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.y > HEIGHT:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))