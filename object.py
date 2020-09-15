"""File for object class"""

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
        self.last = 0
        self.icon = [random.choice(icon)]

    def move(self, screen):
        """Move and draw an object
        1. Screen    - the surface where we will draw a package"""

        self.position[1] += self.velocity
        screen.blit(self.icon[0], (self.position[0], self.position[1]))
