"""File for text class"""

import pygame

class Text():
    """1. size - size of a text
    2. color - color of a text
    3. font_path - path to the font file"""

    def __init__(self, size, color, font_path):
        self.value = 0
        self.text = ""
        try:
            self.font = pygame.font.Font(font_path, size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, size)
        self.color = color

    def draw(self, screen, pos):
        """Draw text and numbers
        1. screen - the surface where we will draw a text
        2. pos - position on the x and y-axis"""

        line = self.font.render(str(self.text) + str(self.value), True, self.color)
        screen.blit(line, (pos[0], pos[1]))

    def draw_text(self, screen, pos):
        """Draw text
        1. screen - the surface where we will draw a text
        2. pos - position on the x and y-axis"""

        line = self.font.render(str(self.text), True, self.color)
        screen.blit(line, (pos[0], pos[1]))

    def draw_center(self, screen, pos):
        """Draw text center on the x-axis
        1. screen - the surface where we will draw a text
        2. pos - position on the y-axis"""

        line = self.font.render(str(self.text), True, self.color)
        centerx = (screen.get_width() / 2) - (line.get_width() / 2)
        screen.blit(line, (centerx, pos))
