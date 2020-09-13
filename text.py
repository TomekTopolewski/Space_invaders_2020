"""File for text class"""

import pygame

class Text():
    """Text class
    1. Size      - size of a text
    2. Color     - color of a text
    3. Font_path - path to the font file"""

    def __init__(self, size, color, font_path):
        self.value = 0
        self.text = ""
        try:
            self.font = pygame.font.Font(font_path, size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, size)
        self.color = color

    def draw(self, screen, position_x, position_y):
        """Draw text and numbers
        1. Screen    - the surface where we will draw a text
        2. PositionX - position on the x-axis where we will draw
        3. PositionY - postion on the y-axis where we will draw"""

        score_render = self.font.render(str(self.text) + str(self.value), True, self.color)
        screen.blit(score_render, (position_x, position_y))

    def draw_text(self, screen, position_x, position_y):
        """Draw text
        1. Screen    - the surface where we will draw a text
        2. PositionX - position on the x-axis where we will draw
        3. PositionY - postion on the y-axis where we will draw"""

        score_render = self.font.render(str(self.text), True, self.color)
        screen.blit(score_render, (position_x, position_y))

    def draw_center(self, screen, position_y):
        """Draw text center on the x-axis
        1. Screen    - the surface where we will draw a text"""

        score_render = self.font.render(str(self.text), True, self.color)
        centerx = (screen.get_width() / 2) - (score_render.get_width() / 2)
        screen.blit(score_render, (centerx, position_y))
