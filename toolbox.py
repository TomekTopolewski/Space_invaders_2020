"""Toolbox"""

import math
import random
import pygame

from pygame import mixer
from button_img import ButtonImg

if not pygame.mixer:
    print("Pygame mixer module not available")

class NoneSound:
    """NoneSound"""
    def play(self):
        """Play"""

    def set_volume(self, value):
        """Set volume"""

def load_img(fname):
    """fname"""

    try:
        img = pygame.image.load(fname)
    except pygame.error:
        default = pygame.Surface((64, 64))
        pygame.draw.rect(default, \
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), \
                (0, 0, 64, 64))
        img = default
    return img

def load_sound(fname):
    """fname"""

    try:
        sound = mixer.Sound(fname)
    except FileNotFoundError:
        sound = NoneSound()
    return sound

def load_music(fname):
    """fname"""

    try:
        music = mixer.music.load(fname)
    except pygame.error:
        music = False
    return music

def moving_bkgd(bkgd, screen, bkgd_one_y, bkgd_two_y):
    """bkgd, screen, bkgd_one_y, bkgd_two_y"""

    bkgd_one_y += 0.5
    bkgd_two_y += 0.5

    if bkgd_one_y > bkgd.get_height():
        bkgd_one_y = bkgd.get_height() * -1

    if bkgd_two_y > bkgd.get_height():
        bkgd_two_y = bkgd.get_height() * -1

    screen.blit(bkgd, (0, bkgd_one_y))
    screen.blit(bkgd, (0, bkgd_two_y))

    return bkgd_one_y, bkgd_two_y

def is_collision(obj_one, obj_two, rng):
    """obj_one, obj_two, rng"""

    o1x = obj_one.pos[0] + (obj_one.icon[0].get_width() / 2)
    o1y = obj_one.pos[1] + (obj_one.icon[0].get_height() / 2)

    o2x = obj_two.pos[0] + (obj_two.icon[0].get_width() / 2)
    o2y = obj_two.pos[1] + (obj_two.icon[0].get_height() / 2)

    distance = math.sqrt(math.pow(o1x - o2x, 2) + (math.pow(o1y - o2y, 2)))

    return bool(distance < rng)

def vol_buttons_def(screen):
    """screen"""

    vol_up = ButtonImg([0, 10], load_img('data/icons/speaker_001.png'))
    vol_down = ButtonImg([0, 60], load_img('data/icons/speaker_002.png'))
    vol_off = ButtonImg([0, 110], load_img('data/icons/speaker_003.png'))

    vol_buttons = [vol_up, vol_down, vol_off]

    for button in vol_buttons:
        button.pos[0] = screen[0][0] - button.img.get_width() - 15

    return vol_buttons

def vol_buttons_act(vol_buttons, mouse, click, vol):
    """vol_buttons, mouse, click, vol"""

    if vol_buttons[0].inside(mouse) and click[0] == 1 and not vol_buttons[0].state:
        vol_buttons[0].state = True
        if vol <= 1.00:
            vol += 0.10
    elif click[0] == 0 and vol_buttons[0].state:
        vol_buttons[0].state = False

    if vol_buttons[1].inside(mouse) and click[0] == 1 and not vol_buttons[1].state:
        vol_buttons[1].state = True
        if vol > 0:
            vol -= 0.10
    elif click[0] == 0 and vol_buttons[1].state:
        vol_buttons[1].state = False

    if vol_buttons[2].inside(mouse) and click[0] == 1 and not vol_buttons[2].state:
        vol_buttons[2].state = True
        vol = 0
    elif click[0] == 0 and vol_buttons[2].state:
        vol_buttons[2].state = False

    return vol
