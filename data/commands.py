import os
import pygame
from pygame import Surface
from data.exceptions import *


def load_image(name, colorkey=None) -> Surface:
    if not os.path.isfile(name):
        raise BadLoadImage(f"Файл с изображением {name} не найден")
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        try:
            image = image.convert_alpha()
            pass
        except pygame.error as e:
            print(e)
    return image
