"""File for functions which load resources"""

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

def load_image(filename):
    """Loading images
    1. Filename - path to a file"""

    try:
        image = pygame.image.load(filename)
    except pygame.error:
        default = pygame.Surface((64, 64))
        pygame.draw.rect(default, \
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), \
                (0, 0, 64, 64))
        image = default
    return image

def load_background(filename, width, height):
    """Loading background
    1. Filename - path to a file
    2. Width    - file width (used when we can't load a file)
    3. Height   - file height (used when we can't load a file)"""

    try:
        image = pygame.image.load(filename)
    except pygame.error:
        image = pygame.Surface((width, height))
        image.fill((0, 0, 0))
    return image

def load_sound(filename):
    """Loading sounds
    1. Filename - path to a file"""

    try:
        sound = mixer.Sound(filename)
    except FileNotFoundError:
        sound = NoneSound()
    return sound

def load_music(filename):
    """Load background music
    1. Filename - path to a file"""

    try:
        music = mixer.music.load(filename)
    except pygame.error:
        music = False
    return music

def moving_background(background, screen, bg1_y, bg2_y):
    """Move the background
    1. Background - image we want to move
    2. Screen     - surface where we will draw an image
    1. Bg1_y      - position on the y-axis of the first image
    2. Bg2_y      - position on the y-axis of the second image"""

    bg1_y -= 0.25
    bg2_y -= 0.25

    if bg1_y < background.get_height() * -1:
        bg1_y = background.get_height()

    if bg2_y < background.get_height() * -1:
        bg2_y = background.get_height()

    screen.blit(background, (0, bg1_y))
    screen.blit(background, (0, bg2_y))

    return bg1_y, bg2_y

def moving_background2(background, screen, bg1_y, bg2_y):
    """Move the background
    1. Background - image we want to move
    2. Screen     - surface where we will draw an image
    1. Bg1_y      - position on the y-axis of the first image
    2. Bg2_y      - position on the y-axis of the second image"""

    bg1_y += 0.5
    bg2_y += 0.5

    if bg1_y > background.get_height():
        bg1_y = background.get_height() * -1

    if bg2_y > background.get_height():
        bg2_y = background.get_height() * -1

    screen.blit(background, (0, bg1_y))
    screen.blit(background, (0, bg2_y))

    return bg1_y, bg2_y

def is_collision(obj1, obj2, crange):
    """Check collision between two objects
    1. obj1    - object one
    2. obj2    - object two
    3. cRange - distance between two points when function returns true"""

    o1x = obj1.position[0] + (obj1.icon[0].get_width() / 2)
    o1y = obj1.position[1] + (obj1.icon[0].get_height() / 2)

    o2x = obj2.position[0] + (obj2.icon[0].get_width() / 2)
    o2y = obj2.position[1] + (obj2.icon[0].get_height() / 2)

    distance = math.sqrt(math.pow(o1x - o2x, 2) + (math.pow(o1y - o2y, 2)))

    return bool(distance < crange)
