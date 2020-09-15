"""File for debris class"""

import pygame

class Debris(pygame.sprite.Sprite):
    """
    1. Icon - image of an object"""

    def __init__(self, icon):
        self.position = [0, 0]
        self.velocity = 0.5
        self.state = True
        self.last = 0
        self.icon = icon

    def keep(self, screen):
        """Keep debris for four seconds
        1. Screen - the surface where we will draw a package"""

        self.position[1] += self.velocity
        if self.last < 60:
            self.last += 1
            screen.blit(self.icon[0], (self.position[0], self.position[1]))
        elif self.last >= 60 and self.last < 120:
            self.last += 1
            screen.blit(self.icon[1], (self.position[0], self.position[1]))
        elif self.last >= 120 and self.last < 180:
            self.last += 1
            screen.blit(self.icon[2], (self.position[0], self.position[1]))
        elif self.last >= 180:
            self.state = False
