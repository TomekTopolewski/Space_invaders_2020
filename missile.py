"""File for missile class"""

import pygame

class Missile(pygame.sprite.Sprite):
    """
    1. Icon     - image for an object
    2. Velocity - move in y-axis"""

    def __init__(self, icon, velocity):
        self.icon = [icon]
        self.position = [0, 0]
        self.velocity = velocity
        self.state = False

    def move(self, screen):
        """Move
        1. Screen - the surface where we will draw a missile"""

        if self.state:
            screen.blit(self.icon[0], (int(self.position[0]), int(self.position[1])))
            self.position[1] += self.velocity
