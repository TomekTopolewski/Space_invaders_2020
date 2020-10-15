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

    def draw(self, scrn_surf, pos):
        """self, scrn_surf, pos"""
        line = self.font.render(str(self.text) + str(self.value), True, self.color)
        scrn_surf.blit(line, (pos[0], pos[1]))

    def draw_text(self, scrn_surf, pos):
        """self, scrn_surf, pos"""
        line = self.font.render(str(self.text), True, self.color)
        scrn_surf.blit(line, (pos[0], pos[1]))

    def draw_center(self, scrn_surf, scrn_param, pos):
        """self, scrn, pos"""
        line = self.font.render(str(self.text), True, self.color)
        centerx = (scrn_param[0] / 2) - (line.get_width() / 2)
        scrn_surf.blit(line, (centerx, pos))
