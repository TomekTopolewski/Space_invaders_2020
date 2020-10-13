"""Main"""

import pygame
from pygame import mixer

from game2 import game2
from menu import menu
from game_over import game_over
from toolbox import load_img, load_sound, load_music

pygame.init()

pygame.display.set_caption("Space Invaders 2020")
window_icon = load_img('data/icons/aircraft-icon.png')
pygame.display.set_icon(window_icon)

scrn = [(827, 880)]
scrn.append(pygame.display.set_mode((scrn[0][0], scrn[0][1])))
scrn.append(load_img('data/images/background_004.jpg'))

pygame.mouse.set_visible(0)

enter_game = load_sound('data/sound/button.wav')

pygame.mixer.pre_init(0, 0, 16, 0)
if load_music('data/sound/background.wav') is not False:
    mixer.music.play(-1)

while True:
    vol = menu(scrn, 0.2)

    enter_game.set_volume(vol)
    enter_game.play()

    score, vol = game2(scrn, vol)

    game_over(score, scrn)
