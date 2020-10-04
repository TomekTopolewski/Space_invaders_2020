"""Enemy"""

import random
import pygame

from objects import Object

class Enemy(pygame.sprite.Sprite):
    """Enemy"""

    def __init__(self, scrn, icon, reload0):
        self.icon = icon
        self.pos = [random.randint(5, scrn[0] - 100), -10]
        self.vel = 1
        self.step = 0
        self.move_type = 0
        self.hitpoints = 2
        self.drop = 1
        self.cell = self.icon[0].get_width() / self.hitpoints
        self.reload = reload0
        self.state = True
        self.time0 = -reload0

    def boss(self):
        """self"""

        self.drop = 10
        self.hitpoints = 5
        self.cell = self.icon[0].get_width() / self.hitpoints

    def shoot(self, enemy_missile, missile_icon):
        """self, enemy_missile, missile_icon"""

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

    def draw_hp(self, scrn):
        """self, scrn"""

        surface = pygame.Surface((self.icon[0].get_width(), 4))
        pygame.draw.rect(surface, (255, 80, 80), (0, 0, self.icon[0].get_width(), 4))
        pygame.draw.rect(surface, (0, 255, 0), (0, 0, int(self.cell * self.hitpoints), 4))
        scrn.blit(surface, (self.pos[0], self.pos[1] - 5))

    def _forward(self, scrn):
        """self, scrn"""

        self.pos[1] += self.vel
        scrn.blit(self.icon[0], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_right_down(self, scrn):
        """self, scrn"""

        self._check_right(scrn[0])
        self.pos[0] += self.vel
        self.pos[1] += self.vel
        scrn[1].blit(self.icon[2], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_rigt_up(self, scrn):
        """self, scrn"""

        self._check_up()
        self._check_left()
        self.pos[0] -= self.vel
        self.pos[1] -= self.vel
        scrn.blit(self.icon[2], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_left_down(self, scrn):
        """self, scrn"""

        self._check_left()
        self.pos[0] -= self.vel
        self.pos[1] += self.vel
        scrn.blit(self.icon[1], (self.pos[0], self.pos[1]))
        self.step += 1

    def _diagonal_left_up(self, scrn):
        """self, scrn"""

        self._check_up()
        self._check_right(scrn[0])
        self.pos[0] += self.vel
        self.pos[1] -= self.vel
        scrn[1].blit(self.icon[1], (self.pos[0], self.pos[1]))
        self.step += 1

    def _right(self, scrn):
        """self, scrn"""

        self._check_right(scrn[0])
        self.pos[0] += self.vel
        scrn[1].blit(self.icon[2], (self.pos[0], self.pos[1]))
        self.step += 1

    def _left(self, scrn):
        """self, scrn"""

        self._check_left()
        self.pos[0] -= self.vel
        scrn.blit(self.icon[1], (self.pos[0], self.pos[1]))
        self.step += 1

    def _check_right(self, scrn):
        """self, scrn"""

        if self.pos[0] >= scrn[0] - self.icon[0].get_width():
            self.pos[0] -= self.vel
            self.step = 0
            self.move_type = random.randint(0, 4)

    def _check_left(self):
        """self"""
        if self.pos[0] <= 0:
            self.pos[0] += self.vel
            self.step = 0
            self.move_type = random.randint(0, 4)

    def _check_up(self):
        """self"""
        if self.pos[1] <= 0:
            self.pos[1] += self.vel
            self.step = 0
            self.move_type = random.randint(0, 4)

    def move(self, scrn):
        """self, scrn"""

        if self.step == 100:
            self.step = 0
            self.move_type = random.randint(0, 6)

        if self.move_type == 0:
            self._forward(scrn[1])
        elif self.move_type == 1:
            self._diagonal_right_down(scrn[:2])
        elif self.move_type == 2:
            self._diagonal_rigt_up(scrn[1])
        elif self.move_type == 3:
            self._diagonal_left_down(scrn[1])
        elif self.move_type == 4:
            self._diagonal_left_up(scrn[:2])
        elif self.move_type == 5:
            self._right(scrn[:2])
        elif self.move_type == 6:
            self._left(scrn[1])
