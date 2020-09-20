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
        self.sound.set_volume(0.70)

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

    def action_menu(self, mouse, click, choose, pos):
        """1. mouse - mouse position
        2. click - click event
        3. choose - menu list
        4. pos - position in the menu list"""

        if self.pos[0] + self.line.get_width() > mouse[0] > self.pos[0] and \
            self.pos[1] + self.line.get_height() > mouse[1] > self.pos[1]:
            self.color = (255, 255, 255)

            if click[0] == 1:
                choose = [False for i in choose]
                choose[pos] = True

        else:
            self.color = (125, 125, 125)

        return choose

    def action(self, mouse, click):
        """1. mouse - mouse position
        2. click - click event"""

        if self.pos[0] + self.line.get_width() > mouse[0] > self.pos[0] and \
            self.pos[1] + self.line.get_height() > mouse[1] > self.pos[1]:
            self.color = (255, 255, 255)

            if click[0] == 1:
                self.status = True

        else:
            self.color = (125, 125, 125)
