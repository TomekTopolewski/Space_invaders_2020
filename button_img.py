"""File for button image class"""

class ButtonImg():
    """1. pos - position of a button
    2. image - image of a button
    3. sound - sound when clicked"""

    def __init__(self, pos, img, sound):
        self.pos = pos
        self.img = img
        self.sound = sound
        self.state = False

    def draw(self, screen):
        """1. screen - surface where to draw a button"""

        screen.blit(self.img, (self.pos))

    def inside(self, mouse):
        """1. mouse - mouse position"""

        return bool(self.pos[0] + self.img.get_width() > mouse[0] > self.pos[0] and \
            self.pos[1] + self.img.get_height() > mouse[1] > self.pos[1])
