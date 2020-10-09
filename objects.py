"""Object"""

import pygame

class Object(pygame.sprite.Sprite):
    """Object"""

    def __init__(self, icon, pos, vel = None, sound = None):
        self.pos = pos
        self.vel = vel
        self.icon = icon
        self.sound = sound
        self.type = 0
        self.hpoints = 1
        self.time0 = pygame.time.get_ticks()

    def movex(self, scrn):
        """self, scrn"""

        self.pos[1] += self.vel
        scrn.blit(self.icon[0], (self.pos[0], self.pos[1]))

    def open(self, player, obj_icons, adv_missile):
        """(for boxes) self, player"""

        if self.type == 0:
            if player.reload > 500:
                player.reload -= 50

        elif self.type == 1:
            player.vel += 1

        elif self.type == 2:
            player.hpoints += 1

        elif self.type == 3:
            player.icon = obj_icons[8]
            adv_missile = True

        return adv_missile
