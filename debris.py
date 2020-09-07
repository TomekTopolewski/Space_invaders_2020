"""File for debris class"""

import math
import random
import pygame

class Debris(pygame.sprite.Sprite):
    """Class for minor objects in game, like debris.
    1. Icon          - image of an object
    2. Screen_params - width and height used for creating objects on the screen"""

    def __init__(self, icon, screen_params):
        self.position = [random.randint(5, screen_params[0] - 50), -30]
        self.velocity = 0.5
        self.state = True
        self.range = 50
        self.last = 0
        self.icon = icon

    def keep(self, icon, screen):
        """Keep debris for four seconds
        1. Icon   - a list with three icons, fading slowly
        2. Screen - the surface where we will draw a package"""

        self.position[1] += self.velocity
        screen.blit(self.icon, (self.position[0], self.position[1]))

        if self.last < 60:
            self.last += 1
        elif self.last >= 60 and self.last < 120:
            self.last += 1
            self.icon = icon[1]
        elif self.last >= 120 and self.last < 180:
            self.last += 1
            self.icon = icon[2]
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
