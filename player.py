"""Player"""

import pygame

from objects import Object

class Player(pygame.sprite.Sprite):
    """Player"""

    def __init__(self, vel, hpoints, icon = None):
        self.icon = icon
        self.pos = [0, 0]
        self.vel = vel
        self.hpoints = hpoints
        self.reload = 1000
        self.time0 = -self.reload

    def move(self, scrn):
        """self, scrn"""

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.pos[0] > self.vel:
            self.pos[0] -= self.vel
            scrn[1].blit(self.icon[1], (self.pos))

            if keys[pygame.K_UP] and self.pos[1] > self.vel:
                self.pos[1] -= self.vel

            if keys[pygame.K_DOWN] and self.pos[1] < scrn[0][1] - \
                                        self.icon[0].get_height() - self.vel:
                self.pos[1] += self.vel

        elif keys[pygame.K_RIGHT] and self.pos[0] < scrn[0][0] - \
                                        self.icon[0].get_width() - self.vel:
            self.pos[0] += self.vel
            scrn[1].blit(self.icon[2], (self.pos))

            if keys[pygame.K_UP] and self.pos[1] > self.vel:
                self.pos[1] -= self.vel

            if keys[pygame.K_DOWN] and self.pos[1] < scrn[0][1] - \
                                        self.icon[0].get_height() - self.vel:
                self.pos[1] += self.vel

        elif keys[pygame.K_UP] and self.pos[1] > self.vel:
            self.pos[1] -= self.vel
            scrn[1].blit(self.icon[0], (self.pos))

        elif keys[pygame.K_DOWN] and self.pos[1] < scrn[0][1] - \
                                        self.icon[0].get_height() - self.vel:
            self.pos[1] += self.vel
            scrn[1].blit(self.icon[0], (self.pos))

        else:
            scrn[1].blit(self.icon[0], (self.pos))

    def shoot(self, player_missile, missile_icon, missile_sound):
        """self, player_missile, missile_icon, missile_sound"""

        time1 = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            if time1 - self.time0 > self.reload:
                player_missile.append(Object(missile_icon, [0, 0], -10, missile_sound))

                launch_x = (self.icon[0].get_width() / 2) - \
                    (player_missile[-1].icon[0].get_width() / 2)

                launch_y = (self.icon[0].get_height() / 2) - \
                    (player_missile[-1].icon[0].get_width() / 2)

                player_missile[-1].pos[0] = self.pos[0] + launch_x
                player_missile[-1].pos[1] = self.pos[1] - launch_y
                player_missile[-1].sound.play()
                self.time0 = pygame.time.get_ticks()
