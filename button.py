"""File for button class"""

import pygame

class Button():
    """
    1. Position - position of a button
    2. Message  - displayed text
    3. Size     - size of a text
    4. Color    - color of a text"""

    def __init__(self, position, message, size, color, sound):
        self.message = message
        self.position = position
        self.color = color
        self.size = size
        self.renderb = 0
        self.status = False
        self.sound = sound
        self.sound.set_volume(0.70)

        try:
            self.font = pygame.font.Font("data/fonts/space_age.ttf", self.size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, size)

    def render(self):
        """Render"""

        self.renderb = self.font.render(self.message, True, self.color)

    def draw(self, screen):
        """Draw
        1. Screen - surface where to draw a button"""

        screen.blit(self.renderb, (self.position[0], self.position[1]))

    def action_menu(self, mouse, click, choose, position):
        """Action for menu
        1. Mouse    - mouse position
        2. Click    - click event
        3. Choose   - menu list
        4. Position - position in the menu list"""

        if self.position[0] + self.renderb.get_width() > mouse[0] > self.position[0] and \
            self.position[1] + self.renderb.get_height() > mouse[1] > self.position[1]:
            self.color = (255, 255, 255)

            if click[0] == 1:
                choose = [False for i in choose]
                choose[position] = True

        else:
            self.color = (125, 125, 125)

        return choose

    def action(self, mouse, click):
        """Action
        1. Mouse - mouse position
        2. Click - click event"""

        if self.position[0] + self.renderb.get_width() > mouse[0] > self.position[0] and \
            self.position[1] + self.renderb.get_height() > mouse[1] > self.position[1]:
            self.color = (255, 255, 255)

            if click[0] == 1:
                self.status = True

        else:
            self.color = (125, 125, 125)
