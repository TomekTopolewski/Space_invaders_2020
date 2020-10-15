"""ButtonImg"""

class ButtonImg():
    """ButtonImg"""

    def __init__(self, pos, img):
        self.pos = pos
        self.img = img
        self.state = False

    def draw(self, scrn):
        """self, scrn"""
        scrn.blit(self.img, (self.pos))

    def inside(self, mouse):
        """self, mouse"""
        return bool(self.pos[0] + self.img.get_width() > mouse[0] > self.pos[0] and \
            self.pos[1] + self.img.get_height() > mouse[1] > self.pos[1])
