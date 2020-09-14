"""File for enemy class"""

import random
import pygame

from missile import Missile

class Enemy(pygame.sprite.Sprite):
    """Enemy class
    1. Screen_params - width and height used for creating enemies on the screen
    2. Enemy_icon    - list of three icons - center, left, right"""

    def __init__(self, screen_params, enemy_icon):
        self.icon = enemy_icon
        self.position = [random.randint(5, screen_params[0]- 100), -10]
        self.velocity = 2.5
        self.step = 0
        self.move_type = 0
        self.hitpoints = 2
        self.drop_rate = 1
        self.cell = self.icon[0].get_width() / self.hitpoints
        self.reload_step = 1
        self.reload_time = 0
        self.is_reloading = False

    def level(self, score_value, enemy_icon):
        """Progress mechanism
        1. Score_value - number of points that player earned
        2. Enemy_skin  - list with a lists of three icons - center, left, right"""

        if score_value > 10 and score_value <= 20:
            self.icon = enemy_icon[1]
        elif score_value > 20 and score_value <= 30:
            self.icon = enemy_icon[2]
        elif score_value > 30 and score_value <= 40:
            self.icon = enemy_icon[3]
        elif score_value > 40 and score_value <= 50:
            self.icon = enemy_icon[4]
        elif score_value > 50 and score_value <= 60:
            self.icon = enemy_icon[5]
        elif score_value > 60:
            self.icon = enemy_icon[random.randint(0, 5)]

    def boss(self):
        """Boss"""
        self.drop_rate = 10
        self.hitpoints = 5
        self.cell = self.icon[0].get_width() / self.hitpoints

    def shoot(self, enemy_missile, missile_icon, missile_velocity):
        """Shoot
        1. Enemy_missile    - list of enemy's missile
        2. Screen           - surface where we will draw a missile
        3. Missile_icon     - list with missiles of icons
        4. Missile_velocity - number of pixels on the y-axis a missile will fly in every loop step"""

        if not self.is_reloading and random.randint(0, 200) == 5:
            self.is_reloading = True
            enemy_missile.append(Missile(missile_icon, 0, missile_velocity, 2))

            launch_x = (self.icon[0].get_width() / 2) - \
                                        (enemy_missile[-1].icon[enemy_missile[-1].type].get_width() / 2)

            launch_y = (self.icon[0].get_height() / 2) - \
                                        (enemy_missile[-1].icon[enemy_missile[-1].type].get_height() / 2)

            enemy_missile[-1].position[0] = self.position[0] + launch_x
            enemy_missile[-1].position[1] = self.position[1] + launch_y
            enemy_missile[-1].state = True

    def draw_hp(self, screen):
        """Draw hitpoints bar
        1. Screen - surface where we will draw a health bar"""

        surface = pygame.Surface((self.icon[0].get_width(), 4))
        pygame.draw.rect(surface, (255, 80, 80), (0, 0, self.icon[0].get_width(), 4))
        pygame.draw.rect(surface, (0, 255, 0), (0, 0, int(self.cell * self.hitpoints), 4))
        screen.blit(surface, (self.position[0], self.position[1] - 5))

    def reload(self, time):
        """Reload
        1. Time - number used for calculating reload between shots"""

        self.reload_time += self.reload_step

        if self.reload_time >= time:
            self.is_reloading = False
            self.reload_time = 0

    def _forward(self, screen):
        """Fly forward
        1. Screen - surface where we will draw a ship"""

        if self.step % 2 == 0:
            self.position[1] += self.velocity
        screen.blit(self.icon[0], (self.position[0], self.position[1]))
        self.step += 1

    def _diagonal_right_down(self, screen, screen_params):
        r"""Fly like this \ down
        1. Screen        - surface where we will draw a ship
        2. Screen_params - width and height used for checking if the enemy won't leave the screen"""

        self._check_right(screen_params)
        if self.step % 2 == 0:
            self.position[0] += self.velocity
            self.position[1] += self.velocity
        screen.blit(self.icon[2], (self.position[0], self.position[1]))
        self.step += 1

    def _diagonal_rigt_up(self, screen):
        r"""Fly like this \ up
        1. Screen - surface where we will draw a ship"""

        self._check_up()
        self._check_left()
        if self.step % 2 == 0:
            self.position[0] -= self.velocity
            self.position[1] -= self.velocity
        screen.blit(self.icon[2], (self.position[0], self.position[1]))
        self.step += 1

    def _diagonal_left_down(self, screen):
        r"""Fly like this / down
        1. Screen - surface where we will draw a ship"""

        self._check_left()
        if self.step % 2 == 0:
            self.position[0] -= self.velocity
            self.position[1] += self.velocity
        screen.blit(self.icon[1], (self.position[0], self.position[1]))
        self.step += 1

    def _diagonal_left_up(self, screen, screen_params):
        r"""Fly like this / up
        1. Screen        - surface where we will draw a ship
        2. Screen_params - width and height used for checking if the enemy won't leave the screen"""

        self._check_up()
        self._check_right(screen_params)
        if self.step % 2 == 0:
            self.position[0] += self.velocity
            self.position[1] -= self.velocity
        screen.blit(self.icon[1], (self.position[0], self.position[1]))
        self.step += 1

    def _right(self, screen, screen_params):
        """Fly right
        1. Screen        - surface where we will draw a ship
        2. Screen_params - width and height used for checking if the enemy won't leave the screen"""

        self._check_right(screen_params)
        if self.step % 2 == 0:
            self.position[0] += self.velocity
        screen.blit(self.icon[2], (self.position[0], self.position[1]))
        self.step += 1

    def _left(self, screen):
        """Fly left
        1. Screen - surface where we will draw a ship"""

        self._check_left()
        if self.step % 2 == 0:
            self.position[0] -= self.velocity
        screen.blit(self.icon[1], (self.position[0], self.position[1]))
        self.step += 1

    def _check_right(self, screen_params):
        """Check right
        1. Screen        - surface where we will draw a ship
        2. Screen_params - width and height used for checking if the enemy won't leave the screen"""

        if self.position[0] >= screen_params[0] - self.icon[0].get_width():
            self.position[0] -= self.velocity
            self.step = 0
            self.move_type = random.randint(0, 4)

    def _check_left(self):
        """Check left"""
        if self.position[0] <= 0:
            self.position[0] += self.velocity
            self.step = 0
            self.move_type = random.randint(0, 4)

    def _check_up(self):
        """Check up"""
        if self.position[1] <= 0:
            self.position[1] += self.velocity
            self.step = 0
            self.move_type = random.randint(0, 4)

    def move(self, screen, screen_params):
        """Advanced move
        1. Screen        - surface where we will draw a ship
        2. Screen_params - width and height used for checking if the enemy won't leave the screen"""

        if self.step == 100:
            self.step = 0
            self.move_type = random.randint(0, 6)

        if self.move_type == 0:
            self._forward(screen)
        elif self.move_type == 1:
            self._diagonal_right_down(screen, screen_params)
        elif self.move_type == 2:
            self._diagonal_rigt_up(screen)
        elif self.move_type == 3:
            self._diagonal_left_down(screen)
        elif self.move_type == 4:
            self._diagonal_left_up(screen, screen_params)
        elif self.move_type == 5:
            self._right(screen, screen_params)
        elif self.move_type == 6:
            self._left(screen)
