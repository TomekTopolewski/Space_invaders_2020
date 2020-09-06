"""File for functions which load resources"""

import random
import pygame
from pygame import mixer

if not pygame.mixer:
    print("Pygame mixer module not available")

class NoneSound:
    """Empty sound"""
    def play(self):
        """Play"""

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
