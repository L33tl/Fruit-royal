import pygame
from settings import *
from data.commands import *
from game import Game


def setup_menu_screen(picture):
    screen.fill((255, 255, 255))
    logo_image = load_image(f'res/images/{picture}.png')
    logo_image = pygame.transform.scale(logo_image, SIZE)
    screen.blit(logo_image, (0, 0))
    running = True
    clock = pygame.time.Clock()
    return running, clock


def start_screen():
    running, clock = setup_menu_screen("logo")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_game()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def finish_screen():
    running, clock = setup_menu_screen('logo')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return main_game()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


def menu():
    pass


def main_game():
    game = Game()
    game.base_game(screen)
    finish_screen()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    start_screen()
