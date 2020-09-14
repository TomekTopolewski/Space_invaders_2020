"""File for debris class"""

import math
import pygame

class Debris(pygame.sprite.Sprite):
    """
    1. Icon - image of an object"""

    def __init__(self, icon):
        self.position = [0, 0]
        self.velocity = 0.5
        self.state = True
        self.range = 50
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

    def is_collision(self, position_x, position_y):
        """Check if an object collides with this object
        1. PositionX - position on the x-axis where this object collides with an object
        2. PositionY - position on the y-axis where this object collides with an object"""

        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False
