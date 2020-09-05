"""Toolbox"""

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
    "Loading images"
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
    """Loading background"""
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        image = pygame.Surface((width, height))
        image.fill((0, 0, 0))
    return image

def load_sound(filename):
    """Loading sounds"""
    try:
        sound = mixer.Sound(filename)
    except FileNotFoundError:
        sound = NoneSound()
    return sound

def load_music(filename):
    """Load background music"""
    try:
        music = mixer.music.load(filename)
    except pygame.error:
        music = False
    return music
