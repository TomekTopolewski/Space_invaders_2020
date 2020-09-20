"""File for enemy class"""

import random
import pygame

from objects import Object

class Enemy(pygame.sprite.Sprite):
    """1. display - width and height of the screen
    2. icon - list of three icons - center, left, right
    3. reload0 - reload time"""

    def __init__(self, display, icon, reload0):
        self.icon = icon
        self.pos = [random.randint(5, display[0] - 100), -10]
        self.vel = 1
        self.step = 0
        self.move_type = 0
        self.hitpoints = 2
        self.drop = 1
        self.cell = self.icon[0].get_width() / self.hitpoints
        self.reload = reload0
        self.state = True
        self.time0 = -reload0

    def level(self, score, icon):
        """1. score - number of points that player earned
        2. enemy icon - list with a lists of three icons - center, left, right"""

        if score > 10 and score <= 20:
            self.icon = icon[1]
        elif score > 20 and score <= 30:
            self.icon = icon[2]
        elif score > 30 and score <= 40:
            self.icon = icon[3]
        elif score > 40 and score <= 50:
            self.icon = icon[4]
        elif score > 50 and score <= 60:
            self.icon = icon[5]
        elif score > 60:
            self.icon = icon[random.randint(0, 5)]

    def boss(self):
        """Boss"""
        self.drop = 10
        self.hitpoints = 5
        self.cell = self.icon[0].get_width() / self.hitpoints

    def shoot(self, enemy_missile, missile_icon):
        """1. enemy_missile - list of enemy's missile
        2. missile_icon  - list with missiles of icons"""

        time1 = pygame.time.get_ticks()

        if time1 - self.time0 > self.reload:
            enemy_missile.append(Object([missile_icon], [0, 0], 4, False))

            launch_x = (self.icon[0].get_width() / 2) - \
                (enemy_missile[-1].icon[0].get_width() / 2)

            launch_y = (self.icon[0].get_height() / 2) - \
                (enemy_missile[-1].icon[0].get_height() / 2)

            enemy_missile[-1].pos[0] = self.pos[0] + launch_x
            enemy_missile[-1].pos[1] = self.pos[1] + launch_y
            enemy_missile[-1].state = True
            self.time0 = pygame.time.get_ticks()

    def draw_hp(self, display):
        """1. display - surface where we will draw a bar"""

        surface = pygame.Surface((self.icon[0].get_width(), 4))
        pygame.draw.rect(surface, (255, 80, 80), (0, 0, self.icon[0].get_width(), 4))
        pygame.draw.rect(surface, (0, 255, 0), (0, 0, int(self.cell * self.hitpoints), 4))
        display.blit(surface, (self.pos[0], self.pos[1] - 5))

    def _forward(self, display):
        """1. display - surface where we will move"""

        self.pos[1] += self.vel
        display.blit(self.icon[0], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_right_down(self, display):
        """1. display - surface and screen params"""

        self._check_right(display[0])
        self.pos[0] += self.vel
        self.pos[1] += self.vel
        display[1].blit(self.icon[2], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_rigt_up(self, display):
        """1. display - surface where we will move"""

        self._check_up()
        self._check_left()
        self.pos[0] -= self.vel
        self.pos[1] -= self.vel
        display.blit(self.icon[2], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_left_down(self, display):
        """1. display - surface where we will move"""

        self._check_left()
        self.pos[0] -= self.vel
        self.pos[1] += self.vel
        display.blit(self.icon[1], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_left_up(self, display):
        """1. display - surface and screen params"""

        self._check_up()
        self._check_right(display[0])
        self.pos[0] += self.vel
        self.pos[1] -= self.vel
        display[1].blit(self.icon[1], (self.pos[0], self.pos[1]))
        self.step += 1

    def _right(self, display):
        """1. display - surface and screen params"""

        self._check_right(display[0])
        self.pos[0] += self.vel
        display[1].blit(self.icon[2], (self.pos[0], self.pos[1]))
        self.step += 1

    def _left(self, display):
        """1. display - surface where we will move"""

        self._check_left()
        self.pos[0] -= self.vel
        display.blit(self.icon[1], (self.pos[0], self.pos[1]))
        self.step += 1

    def _check_right(self, display):
        """1. display - screen params"""

        if self.pos[0] >= display[0] - self.icon[0].get_width():
            self.pos[0] -= self.vel
            self.step = 0
            self.move_type = random.randint(0, 4)

    def _check_left(self):
        """Check left"""
        if self.pos[0] <= 0:
            self.pos[0] += self.vel
            self.step = 0
            self.move_type = random.randint(0, 4)

    def _check_up(self):
        """Check up"""
        if self.pos[1] <= 0:
            self.pos[1] += self.vel
            self.step = 0
            self.move_type = random.randint(0, 4)

    def move(self, display):
        """1. display - surface and screen params"""

        if self.step == 100:
            self.step = 0
            self.move_type = random.randint(0, 6)

        if self.move_type == 0:
            self._forward(display[1])
        elif self.move_type == 1:
            self._diagonal_right_down(display[:2])
        elif self.move_type == 2:
            self._diagonal_rigt_up(display[1])
        elif self.move_type == 3:
            self._diagonal_left_down(display[1])
        elif self.move_type == 4:
            self._diagonal_left_up(display[:2])
        elif self.move_type == 5:
            self._right(display[:2])
        elif self.move_type == 6:
            self._left(display[1])
