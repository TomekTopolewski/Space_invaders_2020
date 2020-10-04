"""Button"""

import pygame

class Button():
    """Button"""

    def __init__(self, pos, msg, size):
        self.msg = msg
        self.pos = pos
        self.color = (255, 255, 255)
        self.size = size
        self.line = 0
        self.status = False

        try:
            self.font = pygame.font.Font("data/fonts/space_age.ttf", self.size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, size)

    def render(self):
        """self"""

        self.line = self.font.render(self.msg, True, self.color)

    def draw(self, screen):
        """self, screen"""

        screen.blit(self.line, (self.pos))

    def inside(self, mouse):
        """self, mouse"""

        return bool(self.pos[0] + self.line.get_width() > mouse[0] > self.pos[0] and \
            self.pos[1] + self.line.get_height() > mouse[1] > self.pos[1])
