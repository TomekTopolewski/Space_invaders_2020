"""File for player class"""

import math
import pygame

from missile import Missile

class Player(pygame.sprite.Sprite):
    """ Player class
    1. Velocity  - number of pixels on both axis that a player will move in every loop step
    2. Hitpoints - number of player's hitpoints
    3. Icon      - a list of three icons - center, left, right"""

    def __init__(self, velocity, hitpoints, icon):
        self.icon = icon
        self.position = [370, 480]
        self.velocity = velocity
        self.hitpoints = hitpoints
        self.reload_step = 10
        self.reload_time = 0
        self.is_reloading = False

    def is_collision(self, position_x, position_y):
        """Check if player collide with enemy
        1. PositionX - position on the x-axis where the player collides with an enemy
        2. PositionY - position on the y-axis where the player collides with an enemy"""

        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < 35:
            return True
        else:
            return False

    def move(self, screen, screen_params):
        """Move
        1. Screen        - the surface where we will draw a player ship
        2. Screen_params - width and height used for checking if the player
                           won't leave the screen"""

        keys = pygame.key.get_pressed()
        # I'm not proud of it, but it works.
        # I hope that I will find another way to control the player's move.
        if keys[pygame.K_LEFT] and self.position[0] > self.velocity:
            self.position[0] -= self.velocity
            screen.blit(self.icon[1], (self.position[0], self.position[1]))

            if keys[pygame.K_UP] and self.position[1] > self.velocity:
                self.position[1] -= self.velocity

            if keys[pygame.K_DOWN] and self.position[1] < screen_params[1] - \
                                        pygame.Surface.get_height(self.icon[0]) - self.velocity:
                self.position[1] += self.velocity

        elif keys[pygame.K_RIGHT] and self.position[0] < screen_params[0] - \
                                        pygame.Surface.get_width(self.icon[0]) - self.velocity:
            self.position[0] += self.velocity
            screen.blit(self.icon[2], (self.position[0], self.position[1]))

            if keys[pygame.K_UP] and self.position[1] > self.velocity:
                self.position[1] -= self.velocity

            if keys[pygame.K_DOWN] and self.position[1] < screen_params[1] - \
                                        pygame.Surface.get_height(self.icon[0]) - self.velocity:
                self.position[1] += self.velocity

        elif keys[pygame.K_UP] and self.position[1] > self.velocity:
            self.position[1] -= self.velocity
            screen.blit(self.icon[0], (self.position[0], self.position[1]))

        elif keys[pygame.K_DOWN] and self.position[1] < screen_params[1] - \
                                        pygame.Surface.get_height(self.icon[0]) - self.velocity:
            self.position[1] += self.velocity
            screen.blit(self.icon[0], (self.position[0], self.position[1]))
        else:
            screen.blit(self.icon[0], (self.position[0], self.position[1]))

    def shoot(self, player_missile, is_upgraded, missile_icon, \
        missile_sound, missile_velocity, missile_range):
        """Shoot
        1. Player_missile   - list with player's missiles
        2. Is_upgraded      - flag used for determining which missile icon to use
        3. Missile_icon     - list with missiles of icons
        4. Missile_sound    - sound when a missile starts
        5. Missile_velocity - number of pixels on the y-axis a missile will fly in every loop step
        6. Missile_range    - number used for deciding if a missile hit the target
                              (a missile and an object are close to each other)"""

        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            if not self.is_reloading:
                if is_upgraded:
                    player_missile.append(Missile(\
                            missile_icon[0], missile_sound[1], missile_velocity, missile_range))
                else:
                    player_missile.append(Missile(\
                            missile_icon[1], missile_sound[0], missile_velocity, missile_range))

                launch_x = (pygame.Surface.get_width(self.icon[0]) / 2) - \
                                        (pygame.Surface.get_width(player_missile[-1].icon) / 2)
                launch_y = (pygame.Surface.get_height(self.icon[0]) / 2) - \
                                        (pygame.Surface.get_height(player_missile[-1].icon) / 2)

                player_missile[-1].position[0] = self.position[0] + launch_x
                player_missile[-1].position[1] = self.position[1] - launch_y
                player_missile[-1].sound.set_volume(0.20)
                player_missile[-1].sound.play()
                player_missile[-1].state = True
                self.is_reloading = True

    def reload(self, time):
        """Reload
        1. Time - number used for calculating reload between shots"""

        self.reload_time += self.reload_step

        if self.reload_time >= time:
            self.is_reloading = False
            self.reload_time = 0
