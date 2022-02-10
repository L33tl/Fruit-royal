import pygame
from pygame.sprite import Group, Sprite

from general_classes import Button
from settings import *
from data.commands import *
from game import Game
from pygame.transform import scale


def setup_menu_screen(picture):
    screen.fill((255, 255, 255))
    logo_image = load_image(f'res/images/{picture}.png')
    logo_image = pygame.transform.scale(logo_image, SIZE)
    screen.blit(logo_image, (0, 0))
    running = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)

    btn_images = [load_image(f'res/images/{image}.png') for image in ['exit', 'classic', 'arcade']]

    image = btn_images[0]
    doubled_size = tuple(xy * 1.5 for xy in image.get_size())
    image = scale(image, doubled_size)

    button_exit = Button(10, HEIGHT - image.get_height(), image, destroy)

    image = scale(btn_images[1], doubled_size)
    button_classic = Button(WIDTH / 3 - image.get_width() / 2, (HEIGHT - image.get_height()) / 2,
                            image, classic_game)

    image = scale(btn_images[2], doubled_size)
    button_arcade = Button(2 * WIDTH / 3 - image.get_width() / 2, (HEIGHT - image.get_height()) / 2,
                           image, arcade_game)

    buttons_group = Group(button_exit, button_classic, button_arcade)
    return running, clock, buttons_group


def destroy():
    pygame.quit()


def start_screen():
    running, clock, buttons_group = setup_menu_screen("main_menu")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                button: Button
                for button in buttons_group:
                    if button.get_rect().collidepoint(x, y):
                        button.click()
                        break

        buttons_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


# def finish_screen():
#     running, clock, buttons_group = setup_menu_screen('main_menu')
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 x, y = event.pos
#                 button: Button
#                 for button in buttons_group:
#                     if button.get_rect().collidepoint(x, y):
#                         button.click()
#                         break
#         buttons_group.draw(screen)
#         pygame.display.flip()
#         clock.tick(FPS)
#
#     pygame.quit()


def menu():
    pass


def classic_game():
    main_game(1)


def arcade_game():
    main_game(0)


def main_game(game_type):
    game = Game()
    if game_type:
        game.base_game(screen)
    else:
        pass
    start_screen()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    try:
        start_screen()
    except pygame.error as e:
        print(e)
