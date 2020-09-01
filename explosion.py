"""File for explosion class"""

import pygame

class Explosion(pygame.sprite.Sprite):
    """Class for handling explosions"""
    def __init__(self, icon, sound):
        self.icon = icon
        self.sound = sound
        self.position = [0, 0]
        self.last = 0
        self.state = False

    def splash(self, screen, position_x, position_y):
        """Draw exlosion splash"""
        self.last = 10
        self.state = True
        self.position[0] = position_x
        self.position[1] = position_y
        self.sound.play()
        screen.blit(self.icon, (int(position_x), int(position_y)))

    def splash_last(self, screen, position_x, position_y):
        """Maintain explosion spalsh"""
        if self.last > 0:
            screen.blit(self.icon, (int(position_x), int(position_y)))
            self.last -= 1
        else:
            self.state = False
