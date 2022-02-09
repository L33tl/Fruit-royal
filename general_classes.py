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

class Cross(pygame.sprite.Sprite):
    def __init__(self, cords):
        super().__init__()
        self.x, self.y = cords

        self.images = [load_image(f'res/sprites/cross/x_0{i}.png') for i in range(1, 10)]
        doubled_size = tuple(xy * 2 for xy in self.images[0].get_size())
        self.images = [pygame.transform.scale(image, doubled_size) for image in self.images]

        self.image = self.images[0]
        self.rect = pygame.rect.Rect(self.x, self.y, *self.image.get_size())

        self.on_animation = False
        self.sprite = 0
        self.last_sprite = 9

    def animation(self):
        if self.sprite < self.last_sprite - 1:
            self.sprite += 0.2
            self.image = self.images[round(self.sprite)]

    def update(self):
        if self.on_animation:
            self.animation()

    def draw(self, screen):
        screen.blit(self.image, self.rect.size)

    def start_animation(self):
        self.on_animation = True


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pass
