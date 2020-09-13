"""File for button class"""

import pygame

class Button():
    """Button class
    1. Position - position of a button
    2. Message  - displayed text
    3. Size     - size of a text
    4. Color    - color of a text"""

    def __init__(self, position, message, size, color, sound):
        self.message = message
        self.position = position
        self.color = color
        self.size = size
        self.render = 0
        self.status = False
        self.font = pygame.font.Font("data/fonts/space_age.ttf", self.size)
        self.sound = sound
        self.sound.set_volume(0.70)

    def draw(self, screen):
        """Draw
        1. Screen - surface where to draw a button"""

        self.render = self.font.render(self.message, True, self.color)
        screen.blit(self.render, (self.position[0], self.position[1]))

    def action(self, mouse, click):
        """Action
        1. Screen - surface where to draw a button"""

        if self.position[0] + self.render.get_width() > mouse[0] > self.position[0] and \
            self.position[1] + self.render.get_height() > mouse[1] > self.position[1]:
            self.color = (255, 255, 255)

            if click[0] == 1:
                self.status = True

        else:
            self.color = (125, 125, 125)
