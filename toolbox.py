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
