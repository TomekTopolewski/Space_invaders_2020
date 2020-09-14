"""File for object class"""

import math
import random
import pygame

class Object(pygame.sprite.Sprite):
    """
    1. Icon          - image of an object
    2. Screen_params - width and height used for creating objects on the screen"""

    def __init__(self, icon, screen_params):
        self.position = [random.randint(5, screen_params[0] - 50), -30]
        self.velocity = 0.5
        self.state = True
        self.range = 50
        self.last = 0
        self.icon = random.choice(icon)

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

    def move(self, screen):
        """Move and draw an object
        1. Screen    - the surface where we will draw a package"""

        self.position[1] += self.velocity
        screen.blit(self.icon, (self.position[0], self.position[1]))
