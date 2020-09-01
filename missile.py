"""Missile class"""

import math
import pygame

class Missile(pygame.sprite.Sprite):
    """Missile class"""
    def __init__(self, icon, sound, velocity, mrange):
        self.icon = icon
        self.sound = sound
        self.position = [0, 0]
        self.velocity = velocity
        self.state = False
        self.range = mrange

    def is_collision(self, position_x, position_y):
        """Check if missile hit the target"""
        hit_x = self.position[0] + (pygame.Surface.get_width(self.icon) / 2)

        distance = math.sqrt(math.pow(position_x - hit_x, 2) + \
                            (math.pow(position_y - self.position[1], 2)))

        if distance < self.range and self.state:
            return True
        else:
            return False

    def move(self, screen):
        """Move"""
        if self.state:
            screen.blit(self.icon, (int(self.position[0]), int(self.position[1])))
            self.position[1] += self.velocity
