"""Object"""

import pygame

class Object(pygame.sprite.Sprite):
    """Object"""

    def __init__(self, icon, pos, vel, sound):
        self.pos = pos
        self.vel = vel
        self.state = False
        self.icon = icon
        self.sound = sound
        self.type = 0
        self.hitpoints = 1
        self.time0 = pygame.time.get_ticks()

    def movex(self, scrn):
        """self, scrn"""

        self.pos[1] += self.vel
        scrn.blit(self.icon[0], (self.pos[0], self.pos[1]))

    def movexy(self, scrn):
        """self, scrn"""

        self.pos[0] -= self.vel
        self.pos[1] += self.vel
        scrn.blit(self.icon[0], (self.pos[0], self.pos[1]))

    def open(self, player):
        """(for boxes) self, player"""

        if self.type == 0:
            if player.reload > 500:
                player.reload -= 50

        elif self.type == 1:
            player.vel += 1

        elif self.type == 2:
            player.hitpoints += 1

    def keep(self, scrn):
        """(for debris) self, scrn"""

        self.pos[1] += self.vel
        time1 = pygame.time.get_ticks()

        if time1 - self.time0 < 100:
            scrn.blit(self.icon[0], (self.pos[0], self.pos[1]))

        elif time1 - self.time0 >= 100 and time1 - self.time0 < 200:
            scrn.blit(self.icon[1], (self.pos[0], self.pos[1]))

        elif time1 - self.time0 >= 200 and time1 - self.time0 < 300:
            scrn.blit(self.icon[2], (self.pos[0], self.pos[1]))

        elif time1 - self.time0 >= 300:
            self.state = False
