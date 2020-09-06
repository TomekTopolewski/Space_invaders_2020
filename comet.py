"""File for comet class"""

import pygame

class Comet(pygame.sprite.Sprite):
    """Class for comet animation in game menu
    1. Icon          - image of an object
    2. Position      - list with x and y position"""

    def __init__(self, icon, position):
        self.position = position
        self.velocity = 5
        self.state = True
        self.icon = icon

    def move(self, screen):
        """Move and draw an object
        1. Screen    - the surface where we will draw a package"""

        self.position[0] -= self.velocity
        self.position[1] += self.velocity
        screen.blit(self.icon, (self.position[0], self.position[1]))
