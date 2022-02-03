import pygame
from settings import *
from data.commands import *
from game import Game

pygame.init()
screen = pygame.display.set_mode(SIZE)


def start_screen():
    screen.fill((0, 0, 0))
    logo_image = load_image('res/images/logo.png')
    screen.blit(logo_image, (0, 0))
    running = True
    clock = pygame.time.Clock()
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



if __name__ == '__main__':
    start_screen()
