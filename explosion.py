"""File for explosion class"""

import pygame

class Explosion(pygame.sprite.Sprite):
    """
    1. Icon  - image of an explosion
    2. Sound - sound when an object explode"""

    def __init__(self, icon, sound):
        self.icon = icon
        self.sound = sound
        self.position = [0, 0]
        self.last = 0
        self.state = False
        self.sound.set_volume(0.25)

    def burst(self, screen, position):
        """Draw explosion (sound)
        1. Screen   - the surface where we will draw an explosion
        2. Position - position on the x and y-axis where the explosion will appear"""

        self.last = 10
        self.state = True
        self.position[0] = position[0]
        self.position[1] = position[1]
        self.sound.play()
        screen.blit(self.icon, (self.position[0], self.position[1]))

    def burst2(self, screen, position):
        """Draw explosion (no sound)
        1. Screen   - the surface where we will draw an explosion
        2. Position - position on the x and y-axis where the explosion will appear"""

        self.last = 10
        self.state = True
        self.position[0] = position[0]
        self.position[1] = position[1]
        screen.blit(self.icon, (self.position[0], self.position[1]))

    def burst_last(self, screen):
        """Keep burst on the screen
        1. Screen    - the surface where we will draw an explosion"""

        if self.last > 0:
            screen.blit(self.icon, (self.position[0], self.position[1]))
            self.last -= 1
        else:
            self.state = False
