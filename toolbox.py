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

def moving_bkgd(scrn_surf, scrn_param, bkgd_img, bkgd_pos):
    """scrn, bkgd_pos"""
    bkgd_pos[0] += 0.5
    bkgd_pos[1] += 0.5

    if bkgd_pos[0] > scrn_param[1]:
        bkgd_pos[0] = scrn_param[1] * -1

    if bkgd_pos[1] > scrn_param[1]:
        bkgd_pos[1] = scrn_param[1] * -1

    scrn_surf.blit(bkgd_img, (0, bkgd_pos[0]))
    scrn_surf.blit(bkgd_img, (0, bkgd_pos[1]))

    return bkgd_pos

def is_collision(obj_one, obj_two, rng):
    """obj_one, obj_two, rng"""
    obj1x = obj_one.pos[0] + (obj_one.icon[0].get_width() / 2)
    obj1y = obj_one.pos[1] + (obj_one.icon[0].get_height() / 2)

    obj2x = obj_two.pos[0] + (obj_two.icon[0].get_width() / 2)
    obj2y = obj_two.pos[1] + (obj_two.icon[0].get_height() / 2)

    distance = math.sqrt(math.pow(obj1x - obj2x, 2) + (math.pow(obj1y - obj2y, 2)))

    return bool(distance < rng)

def vol_buttons_def(scrn_param):
    """scrn_param"""
    vol_up = ButtonImg([0, 10], load_img('data/icons/speaker_001.png'))
    vol_down = ButtonImg([0, 60], load_img('data/icons/speaker_002.png'))
    vol_off = ButtonImg([0, 110], load_img('data/icons/speaker_003.png'))

    vol_buttons = [vol_up, vol_down, vol_off]

    for button in vol_buttons:
        button.pos[0] = scrn_param[0] - button.img.get_width() - 15

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

def button_act(button, mouse, click):
    """button, mouse, click"""
    status = False
    if button.inside(mouse):
        button.color = (255, 255, 255)
        if click[0] == 1:
            status = True
    else:
        button.color = (155, 155, 155)

    return status
