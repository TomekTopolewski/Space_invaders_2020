"""Player class"""

import math
import pygame

from missile import Missile

class Player(pygame.sprite.Sprite):
    """ Player class"""
    def __init__(self, velocity, hitpoints, icon):
        self.icon = icon
        self.position = [370, 480]
        self.velocity = velocity
        self.hitpoints = hitpoints
        self.reload_step = 10
        self.reload_time = 0
        self.is_reloading = False

    def is_collision(self, position_x, position_y):
        """Check if player collide with enemy"""
        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < 35:
            return True
        else:
            return False

    def move(self, screen, screen_params):
        """Move"""
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

    def shoot(self, player_missile, is_upgraded, missile_icon, missile_sound, missile_velocity, missile_range):
        "Shoot"
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            if not self.is_reloading:
                if is_upgraded:
                    player_missile.append(Missile(\
                                    missile_icon[0], missile_sound[0], missile_velocity, missile_range))
                else:
                    player_missile.append(Missile(\
                                    missile_icon[1], missile_sound[1], missile_velocity, missile_range))

                launch_x = (pygame.Surface.get_width(self.icon[0]) / 2) - \
                                        (pygame.Surface.get_width(player_missile[-1].icon) / 2)
                launch_y = (pygame.Surface.get_height(self.icon[0]) / 2) - \
                                        (pygame.Surface.get_height(player_missile[-1].icon) / 2)

                player_missile[-1].position[0] = self.position[0] + launch_x
                player_missile[-1].position[1] = self.position[1] - launch_y
                player_missile[-1].sound.play()
                player_missile[-1].state = True
                self.is_reloading = True

    def reload(self, time):
        """Reload"""
        self.reload_time += self.reload_step

        if self.reload_time >= time:
            self.is_reloading = False
            self.reload_time = 0
