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

    def movex(self, screen):
        """self, screen"""

        self.pos[1] += self.vel
        screen.blit(self.icon[0], (self.pos[0], self.pos[1]))

    def movexy(self, screen):
        """self, screen"""

        self.pos[0] -= self.vel
        self.pos[1] += self.vel
        screen.blit(self.icon[0], (self.pos[0], self.pos[1]))

    def open(self, player, is_upgraded, player_icon):
        """(fox boxes) self, player, is_upgraded, player_icon"""

        if self.type == 0:
            player.hitpoints += 1
        elif self.type == 1:
            player.icon = player_icon
            is_upgraded = True
        elif self.type == 3:
            player.vel += 1
        elif self.type == 2:
            if player.reload > 500:
                player.reload -= 50
        return is_upgraded

    def keep(self, screen):
        """(for debris) self, screen"""

        self.pos[1] += self.vel
        time1 = pygame.time.get_ticks()

        if time1 - self.time0 < 100:
            screen.blit(self.icon[0], (self.pos[0], self.pos[1]))

        elif time1 - self.time0 >= 100 and time1 - self.time0 < 200:
            screen.blit(self.icon[1], (self.pos[0], self.pos[1]))

        elif time1 - self.time0 >= 200 and time1 - self.time0 < 300:
            screen.blit(self.icon[2], (self.pos[0], self.pos[1]))

        elif time1 - self.time0 >= 300:
            self.state = False
