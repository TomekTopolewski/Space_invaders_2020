"""File with useful functions"""

import math
import random
import pygame

from pygame import mixer

if not pygame.mixer:
    print("Pygame mixer module not available")

class NoneSound:
    """Empty sound"""
    def play(self):
        """Play"""

    def set_volume(self, value):
        """Set volume"""

def load_img(file):
    """1. file - path to a file"""

    try:
        img = pygame.image.load(file)
    except pygame.error:
        default = pygame.Surface((64, 64))
        pygame.draw.rect(default, \
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), \
                (0, 0, 64, 64))
        img = default
    return img

def load_sound(file):
    """1. file - path to a file"""

    try:
        sound = mixer.Sound(file)
    except FileNotFoundError:
        sound = NoneSound()
    return sound

def load_music(file):
    """1. file - path to a file"""

    try:
        music = mixer.music.load(file)
    except pygame.error:
        music = False
    return music

def moving_bkgd(bkgd, screen, bkgd_one_y, bkgd_two_y):
    """1. bkgd - image we want to move
    2. screen - surface where we will draw an image
    3. bkgd_one_y - position on the y-axis of the first image
    4. bkgd_two_y - position on the y-axis of the second image"""

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
    """1. obj_one - object one
    2. obj_two - object two
    3. rng - distance between two points when function returns true"""

    o1x = obj_one.pos[0] + (obj_one.icon[0].get_width() / 2)
    o1y = obj_one.pos[1] + (obj_one.icon[0].get_height() / 2)

    o2x = obj_two.pos[0] + (obj_two.icon[0].get_width() / 2)
    o2y = obj_two.pos[1] + (obj_two.icon[0].get_height() / 2)

    distance = math.sqrt(math.pow(o1x - o2x, 2) + (math.pow(o1y - o2y, 2)))

    return bool(distance < rng)
