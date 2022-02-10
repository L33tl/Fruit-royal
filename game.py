import threading

from datetime import datetime
import pygame
from pygame.sprite import Group
from pygame import time

from data.commands import load_image
from settings import *
from fruit import Fruit
from general_classes import Blade, Cross, Combo, Spot
from bomb import Bomb
import random


class Game:
    def __init__(self):
        self.fruits_group = Group()
        self.bomb_group = Group()
        self.slices_group = Group()
        self.particle_group = Group()
        self.fruit_spawn_timer = threading.Event()
        self.result = 0
        self.missed_fruits = 0
        self.last_fruit = datetime.now()
        self.current_combo = 0
        self.blade = Blade()
        self.last_fruit = datetime.now()
        self.mouse_moving = False
        self.game_type = None

        self.crosses = Group(Cross((20, 50)), Cross((80, 50)), Cross((140, 50)))

    def base_game(self, screen):
        self.game_type = 1
        screen.fill((0, 0, 0))
        back_image = pygame.transform.scale(load_image(f'res/images/game_background.png'), SIZE)
        running = True
        clock = time.Clock()
        pygame.mouse.set_visible(False)
        mouse_pos = (0, 0)
        score_text = pygame.font.Font(f"res/fonts/main_font.ttf", 50)
        combo = None
        best_combo = 0

        while running:
            screen.fill((0, 0, 0))
            screen.blit(back_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.blade.is_cutting = True
                    if event.button == 3:
                        self.blade.is_rotating = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.blade.is_cutting = False
                    if event.button == 3:
                        self.blade.is_rotating = False
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    self.mouse_moving = True
                else:
                    self.mouse_moving = False

            # if self.added_points:
            #     self.render_added_points(screen)

            score = score_text.render(str(self.result), True, (180, 0, 0))
            self.blade.rect.x, self.blade.rect.y = mouse_pos
            if not self.fruit_spawn_timer.is_set():
                threading.Timer(self.get_random_time(), self.spawn_fruits_group,
                                [self.fruit_spawn_timer]).start()
                self.fruit_spawn_timer.set()

            collision_res = self.check_collision()
            if collision_res is False:
                return self.result, best_combo

            if collision_res and self.current_combo > 1:
                combo = Combo(self.current_combo)
            if combo:
                combo.update()
                combo.draw(screen)
            self.particle_group.update()
            self.particle_group.draw(screen)
            self.crosses.update()
            self.crosses.draw(screen)
            self.bomb_group.update()
            self.bomb_group.draw(screen)
            self.fruits_group.update()
            self.fruits_group.draw(screen)
            self.slices_group.update()
            self.slices_group.draw(screen)
            self.blade.draw(screen, mouse_pos)
            screen.blit(score, (10, 0))
            clock.tick(FPS)
            pygame.display.flip()

            best_combo = max(best_combo, self.current_combo)

    def arcade_game(self, screen):
        self.game_type = 0
        # бомбы - -10pts
        # упавшее говно хер с ним
        # таймер 60s

        screen.fill((0, 0, 0))
        back_image = pygame.transform.scale(load_image(f'res/images/game_background.png'), SIZE)
        running = True
        clock = time.Clock()
        last_fruit = datetime.now()
        pygame.mouse.set_visible(False)
        mouse_pos = (0, 0)
        score_text = pygame.font.Font(f"res/fonts/main_font.ttf", 50)
        combo = None
        best_combo = 0
        start_ticks = time.get_ticks()
        duration = 40

        while running:
            screen.fill((0, 0, 0))
            screen.blit(back_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.blade.is_cutting = True
                    if event.button == 3:
                        self.blade.is_rotating = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.blade.is_cutting = False
                    if event.button == 3:
                        self.blade.is_rotating = False
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    self.mouse_moving = True
                else:
                    self.mouse_moving = False

            # if self.added_points:
            #     self.render_added_points(screen)

            score = score_text.render(str(self.result), True, (180, 0, 0))
            self.blade.rect.x, self.blade.rect.y = mouse_pos
            if not self.fruit_spawn_timer.is_set():
                threading.Timer(self.get_random_time(), self.spawn_fruits_group,
                                [self.fruit_spawn_timer]).start()
                self.fruit_spawn_timer.set()

            collision_res = self.check_collision()
            if collision_res is False:
                self.result = max(self.result - 20, 0)

            if collision_res and self.current_combo > 1:
                combo = Combo(self.current_combo)
            if combo:
                combo.update()
                combo.draw(screen)
            self.particle_group.update()
            self.particle_group.draw(screen)
            self.bomb_group.update()
            self.bomb_group.draw(screen)
            self.fruits_group.update()
            self.fruits_group.draw(screen)
            self.slices_group.update()
            self.slices_group.draw(screen)
            self.blade.draw(screen, mouse_pos)

            best_combo = max(best_combo, self.current_combo)

            timer = duration - (time.get_ticks() - start_ticks) / 1000

            if timer <= 0:
                return self.result, best_combo

            f2 = pygame.font.Font(f"res/fonts/main_font.ttf", 50)
            timer = f2.render(str(round(timer)), True, (0, 180, 0))
            screen.blit(timer, (WIDTH / 2, 0))

            screen.blit(score, (10, 0))
            clock.tick(FPS)
            pygame.display.flip()

    def spawn_fruits_group(self, args=None, kwargs=None):
        possible_amounts = (0, 1, 2, 3, 4, 5)
        weights = (1, 2, 3, 3, 2, 2)
        fruits_amount = random.choices(possible_amounts, weights=weights)[0]
        wants_bomb = random.randint(1, 4)
        for i in range(fruits_amount):
            fruit = Fruit()
            self.fruits_group.add(fruit)
        if wants_bomb == 1:
            bomb = Bomb()
            self.bomb_group.add(bomb)
        self.fruit_spawn_timer.clear()
        return fruits

    @staticmethod
    def get_random_time():
        return random.randrange(2, 3)

    def check_collision(self):
        fruit: Fruit
        bomb: Bomb
        answer = 0
        acceleration_need_to_cut = 50
        for bomb in self.bomb_group:
            if not self.mouse_moving and bomb.throwing_force <= acceleration_need_to_cut:
                break

            if pygame.sprite.collide_mask(self.blade,
                                          bomb) and self.blade.is_cutting and not bomb.exploded():
                bomb.set_exploded()
                return False
        for fruit in self.fruits_group:
            if not self.mouse_moving and fruit.throwing_force <= acceleration_need_to_cut:
                return 0

            if pygame.sprite.collide_mask(fruit, self.blade) and self.blade.is_cutting:
                if (datetime.now() - self.last_fruit).seconds <= 0.3:
                    self.result += 1
                    self.current_combo += 1
                else:
                    self.current_combo = 1
                self.result += 1
                first, second = fruit.cut()
                self.slices_group.add(first, second)
                self.last_fruit = datetime.now()
                answer += 1
                spot = Spot(first.rect.x, first.rect.y, first.fruit_type)
                self.particle_group.add(spot)
            if fruit.rect.y > HEIGHT and fruit.was_above:
                if self.game_type:
                    cross: Cross
                    for cross in self.crosses:
                        if not cross.on_animation:
                            cross.start_animation()
                            break
                    else:
                        return False

                self.missed_fruits += 1
                fruit.kill()
        return answer

    # def render_added_points(self, screen):
    #     f2 = pygame.font.Font(None, 50)
    #     score = f2.render(f'+{str(self.added_points)}', True, (0, self.added_points_tint, 0))
    #     score.blit(screen, (10, 0))
    #
    #     self.added_points_tint -= 10
    #     self.result += self.added_points
