"""File for missile class"""

import math
import pygame

class Missile(pygame.sprite.Sprite):
    """
    1. Icon     - image for an object
    2. Velocity - move in y-axis"""

    def __init__(self, icon, velocity):
        self.icon = icon
        self.position = [0, 0]
        self.velocity = velocity
        self.state = False
        self.range = 45

    def is_collision(self, position_x, position_y):
        """Check if missile hit the target
        1. PositionX - position on the x-axis where the object collides with a missile
        2. PositionY - position on the y-axis where the object collides with a missile"""

        hit_x = self.position[0] + (self.icon.get_width() / 2)

        distance = math.sqrt(math.pow(position_x - hit_x, 2) + \
                            (math.pow(position_y - self.position[1], 2)))

        if distance < self.range and self.state:
            return True
        else:
            return False

    def move(self, screen):
        """Move
        1. Screen - the surface where we will draw a missile"""

        if self.state:
            screen.blit(self.icon, (int(self.position[0]), int(self.position[1])))
            self.position[1] += self.velocity
