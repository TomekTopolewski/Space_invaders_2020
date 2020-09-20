"""File for button class"""

import pygame

class Button():
    """1. pos - position of a button
    2. msg - displayed text
    3. size - size of a text
    4. color - color of a text
    5. sound - sound when clicked"""

    def __init__(self, pos, msg, size, color, sound):
        self.msg = msg
        self.pos = pos
        self.color = color
        self.size = size
        self.line = 0
        self.status = False
        self.sound = sound

        try:
            self.font = pygame.font.Font("data/fonts/space_age.ttf", self.size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, size)

    def render(self):
        """Draw text onto surface"""

        self.line = self.font.render(self.msg, True, self.color)

    def draw(self, screen):
        """1. screen - surface where to draw a button"""

        screen.blit(self.line, (self.pos))

    def inside(self, mouse):
        """1. mouse - mouse position"""

        return bool(self.pos[0] + self.line.get_width() > mouse[0] > self.pos[0] and \
            self.pos[1] + self.line.get_height() > mouse[1] > self.pos[1])
