import pygame
from pygame import Rect
from data.commands import load_image
from settings import *


class Blade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('res/images/blade0.png')
        self.is_cutting = False
        self.x, self.y = 0, 0
        self.rect = Rect(self.x, self.y, *self.image.get_size())
        self.mask = pygame.mask.from_surface(self.image)
        self.is_rotating = False
        self.img_type = 0

    def draw(self, screen, mouse_pos):
        if self.is_cutting:
            self.img_type += 0.3
            self.image = load_image(f'res/images/blade{round(self.img_type) % 3}.png')
        screen.blit(self.image, (
            min(WIDTH - self.image.get_width(), mouse_pos[0]),
            min(HEIGHT - self.image.get_height(), mouse_pos[1])))


class Slice(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, fruit_type, side_type):
        super().__init__()
        self.image = load_image(f"res/sprites/fruits/{fruit_type}/{fruit_type}_slice{side_type}.png")
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = PART_GRAVITY
        self.fruit_type = fruit_type

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
        self.rect = Rect(self.x, self.y, *self.image.get_size())

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
    def __init__(self, x, y, image, on_click):
        super().__init__()
        self.x = x
        self.y = y
        self.image = image

        self.click = on_click

        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(self.x, self.y, *self.image.get_size())

    def click(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, self.rect.size)

    def get_rect(self):
        return self.rect


class Combo:
    def __init__(self, quan):
        self.frame = 0
        self.size = 50
        self.quan = quan

    def update(self):
        self.frame += 1
        if (self.frame // 10) % 2 == 0:
            self.size += 3
        else:
            self.size -= 3

    def draw(self, screen):
        if self.frame < 100:
            combo_text = pygame.font.Font(f"res/fonts/main_font.ttf", self.size)
            text = combo_text.render(f"{self.quan}x COMBO!", False, (255, 237, 0))
            text = pygame.transform.rotate(text, 45)
            screen.blit(text, (WIDTH - 300, 10))


class Spot(pygame.sprite.Sprite):
    def __init__(self, x, y, fruit_type):
        super().__init__()
        self.image = load_image(f"res/sprites/fruits/{fruit_type}/{fruit_type}2.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.alpha = 100

    def update(self):
        self.alpha -= 1
        self.image.set_alpha(self.alpha)
        if self.alpha == 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
