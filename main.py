import csv

import pygame
from pygame.sprite import Group, Sprite

from general_classes import Button
from settings import *
from data.commands import *
from game import Game
from pygame.transform import scale


def setup_menu_screen(picture, result, combo):
    screen.fill((255, 255, 255))
    logo_image = load_image(f'res/images/{picture}.png')
    logo_image = pygame.transform.scale(logo_image, SIZE)
    screen.blit(logo_image, (0, 0))
    running = True
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)

    images = [load_image(f'res/images/{image}.png') for image in
              ['exit', 'classic', 'arcade', 'logo']]

    image = images[0]
    doubled_size = tuple(xy * 1.5 for xy in image.get_size())
    image = scale(image, doubled_size)

    button_exit = Button(10, HEIGHT - image.get_height(), image, destroy)

    image = scale(images[1], doubled_size)
    button_classic = Button(WIDTH / 3 - image.get_width() / 2, (HEIGHT - image.get_height()) / 2,
                            image, classic_game)

    image = scale(images[2], doubled_size)
    button_arcade = Button(2 * WIDTH / 3 - image.get_width() / 2, (HEIGHT - image.get_height()) / 2,
                           image, arcade_game)

    buttons_group = Group(button_exit, button_classic, button_arcade)

    logo = images[3]
    new_size = tuple(xy / 2 for xy in logo.get_size())
    logo = scale(logo, new_size)
    f1 = pygame.font.Font(f"res/fonts/main_font.ttf", 25)

    max_result = get_max_result()
    if result:
        max_result = max(result, get_max_result())
    max_result = f1.render(f'Max score: {max_result}', True, (182, 16, 201))
    screen.blit(max_result, (19 * WIDTH / 20 - max_result.get_width(), 16 * HEIGHT / 20))

    if result:
        write_result(result, combo)

        result = f1.render(f'Score: {result}', True, (136, 15, 82))
        screen.blit(result, (19 * WIDTH / 20 - result.get_width(), 15 * HEIGHT / 20))

        if combo > 1:
            combo = f1.render(f'The best combo: {combo}', True, (199, 125, 201))
            screen.blit(combo, (19 * WIDTH / 20 - combo.get_width(), 17 * HEIGHT / 20))

    return running, clock, buttons_group, logo


def get_max_result():
    max_result = 0
    try:
        with open('res/scores.csv', 'r', encoding='utf-8') as csv_file:
            try:
                data = list(csv.reader(csv_file, delimiter=';'))[1:]
                max_result = max(int(max(data, key=lambda x: int(x[1]))[1]), max_result)
            except (IndexError, ValueError):
                pass
    except KeyError:
        print('Bad score log')
    return max_result


def write_result(result, combo):
    try:
        with open('res/scores.csv', 'r', encoding='utf-8') as csv_file:
            try:
                data = list(csv.reader(csv_file, delimiter=';'))[1:]
                idx = int(data[-1][0])
            except IndexError:
                idx = 0

        with open('res/scores.csv', 'a', encoding='utf-8', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)
            writer.writerow([str(idx + 1), str(result), str(combo)])
    except KeyError:
        print('Bad score log')


def destroy():
    pygame.quit()


def start_screen(result=None, combo=0):
    running, clock, buttons_group, logo = setup_menu_screen("main_menu", result, combo)
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
        screen.blit(logo, ((WIDTH - logo.get_width()) / 2, HEIGHT / 20))
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
    try:
        if game_type:
            result, combo = game.base_game(screen)
        else:
            result, combo = game.arcade_game(screen)
    except TypeError:
        result, combo = None, 0
    start_screen(result, combo)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    try:
        start_screen()
    except pygame.error as e:
        print(e)
