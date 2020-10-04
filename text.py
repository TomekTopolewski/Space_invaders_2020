"""Text"""

import pygame

class Text():
    """Text"""

    def __init__(self, size, color, fpath):
        self.value = 0
        self.text = ""
        try:
            self.font = pygame.font.Font(fpath, size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, size)
        self.color = color

    def draw(self, screen, pos):
        """self, screen, pos"""

        line = self.font.render(str(self.text) + str(self.value), True, self.color)
        screen.blit(line, (pos[0], pos[1]))

    def draw_text(self, screen, pos):
        """self, screen, pos"""

        line = self.font.render(str(self.text), True, self.color)
        screen.blit(line, (pos[0], pos[1]))

    def draw_center(self, screen, pos):
        """self, screen, pos"""

        line = self.font.render(str(self.text), True, self.color)
        centerx = (screen.get_width() / 2) - (line.get_width() / 2)
        screen.blit(line, (centerx, pos))
