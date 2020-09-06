"""File for explosion class"""

import pygame

class Explosion(pygame.sprite.Sprite):
    """Class for handling explosions
    1. Icon      - image of an explosion
    2. Sound     - sound when the missile hits a target"""

    def __init__(self, icon, sound):
        self.icon = icon
        self.sound = sound
        self.position = [0, 0]
        self.last = 0
        self.state = False

    def burst(self, screen, position_x, position_y):
        """Draw explosion (sound)
        1. Screen    - the surface where we will draw an explosion
        2. PositionX - position on the x-axis where the missile collides with an object
        3. PositionY - position on the y-axis where the missile collides with an object"""

        self.last = 10
        self.state = True
        self.position[0] = position_x
        self.position[1] = position_y
        self.sound.play()
        screen.blit(self.icon, (int(position_x), int(position_y)))

    def burst2(self, screen, position_x, position_y):
        """Draw explosion (no sound)
        1. Screen    - the surface where we will draw an explosion
        2. PositionX - position on the x-axis where the missile collides with an object
        3. PositionY - position on the y-axis where the missile collides with an object"""

        self.last = 10
        self.state = True
        self.position[0] = position_x
        self.position[1] = position_y
        screen.blit(self.icon, (int(position_x), int(position_y)))

    def burst_last(self, screen, position_x, position_y):
        """Maintain explosion
        1. Screen    - the surface where we will draw an explosion
        2. PositionX - position on the x-axis where the missile collides with an object
        3. PositionY - position on the y-axis where the missile collides with an object"""

        if self.last > 0:
            screen.blit(self.icon, (int(position_x), int(position_y)))
            self.last -= 1
        else:
            self.state = False
