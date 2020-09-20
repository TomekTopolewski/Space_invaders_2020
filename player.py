"""File for player class"""

import pygame

from objects import Object

class Player(pygame.sprite.Sprite):
    """1. vel  - move
    2. hitpoints - number of player's hitpoints
    3. icon - a list of three icons - center, left, right"""

    def __init__(self, vel, hitpoints, icon):
        self.icon = icon
        self.pos = [370, 480]
        self.vel = vel
        self.hitpoints = hitpoints
        self.reload = 1000
        self.time0 = -self.reload
        self.state = True

    def move(self, screen, display):
        """1. screen - the surface where we will draw an object
        2. display - width and height of the screen"""

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.pos[0] > self.vel:
            self.pos[0] -= self.vel
            screen.blit(self.icon[1], (self.pos))

            if keys[pygame.K_UP] and self.pos[1] > self.vel:
                self.pos[1] -= self.vel

            if keys[pygame.K_DOWN] and self.pos[1] < display[1] - \
                                        self.icon[0].get_height() - self.vel:
                self.pos[1] += self.vel

        elif keys[pygame.K_RIGHT] and self.pos[0] < display[0] - \
                                        self.icon[0].get_width() - self.vel:
            self.pos[0] += self.vel
            screen.blit(self.icon[2], (self.pos))

            if keys[pygame.K_UP] and self.pos[1] > self.vel:
                self.pos[1] -= self.vel

            if keys[pygame.K_DOWN] and self.pos[1] < display[1] - \
                                        self.icon[0].get_height() - self.vel:
                self.pos[1] += self.vel

        elif keys[pygame.K_UP] and self.pos[1] > self.vel:
            self.pos[1] -= self.vel
            screen.blit(self.icon[0], (self.pos))

        elif keys[pygame.K_DOWN] and self.pos[1] < display[1] - \
                                        self.icon[0].get_height() - self.vel:
            self.pos[1] += self.vel
            screen.blit(self.icon[0], (self.pos))

        else:
            screen.blit(self.icon[0], (self.pos))

    def shoot(self, player_missile, missile_icon, missile_sound):
        """1. player missile - list with player's missiles
        2. missile icon - list with missiles of icons
        3. missile sound - sound when a missile is launched"""

        time1 = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            if time1 - self.time0 > self.reload:
                player_missile.append(Object([missile_icon], [0, 0], -10, missile_sound))

                launch_x = (self.icon[0].get_width() / 2) - \
                    (player_missile[-1].icon[0].get_width() / 2)

                launch_y = (self.icon[0].get_height() / 2) - \
                    (player_missile[-1].icon[0].get_width() / 2)

                # Type 4 is used for check if enemy was destroyed by player's missile in enemy_envi
                player_missile[-1].type = 4
                player_missile[-1].pos[0] = self.pos[0] + launch_x
                player_missile[-1].pos[1] = self.pos[1] - launch_y
                player_missile[-1].sound.play()
                player_missile[-1].state = True
                self.time0 = pygame.time.get_ticks()
