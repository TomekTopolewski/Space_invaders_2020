"""Space Invaders 2020
Based on a great tutorial "Python game development course" by freeCodeCamp.org.
Icons made by smalllikeart from www.flaticon.com
Background made by vectorpouch from www.freepik.com
Music thanks to www.freesound.org"""


import pygame
from pygame import mixer
from main import main
from intro import intro
from toolbox import load_image, load_sound, load_music, load_background

if not pygame.mixer:
    print("Pygame mixer module not available")

pygame.mixer.pre_init(0, 0, 16, 0)
pygame.init()

pygame.display.set_caption("Space Invaders 2020")
window_icon = load_image('data/icons/aircraft-icon.png')
pygame.display.set_icon(window_icon)

screen = [(827, 900)]
screen.append(pygame.display.set_mode((screen[0][0], screen[0][1])))
screen.append(load_background('data/images/background_001.jpg', screen[0][0], screen[0][1]))

if load_music('data/sound/background.wav') is not False:
    mixer.music.play(-1)

e1_icon = [load_image('data/icons/enemy_001.png'), load_image('data/icons/enemy_001-left.png'), \
    load_image('data/icons/enemy_001-right.png')]

e2_icon = [load_image('data/icons/enemy_002.png'), load_image('data/icons/enemy_002-left.png'), \
    load_image('data/icons/enemy_002-right.png')]

e3_icon = [load_image('data/icons/enemy_003.png'), load_image('data/icons/enemy_003-left.png'), \
    load_image('data/icons/enemy_003-right.png')]

e4_icon = [load_image('data/icons/enemy_004.png'), load_image('data/icons/enemy_004-left.png'), \
    load_image('data/icons/enemy_004-right.png')]

e5_icon = [load_image('data/icons/enemy_005.png'), load_image('data/icons/enemy_005-left.png'), \
    load_image('data/icons/enemy_005-right.png')]

e6_icon = [load_image('data/icons/enemy_006.png'), load_image('data/icons/enemy_006-left.png'), \
    load_image('data/icons/enemy_006-right.png')]

e7_icon = [load_image('data/icons/enemy_007.png'), load_image('data/icons/enemy_007-left.png'), \
    load_image('data/icons/enemy_007-right.png')]

bx1_icon = [load_image('data/icons/box_003.png'), load_image('data/icons/box_004.png'), \
    load_image('data/icons/box_001.png'), load_image('data/icons/box_002.png')]

p1_icon = [load_image('data/icons/player_001.png'), load_image('data/icons/player_001-left.png'), \
    load_image('data/icons/player_001-right.png')]

p2_icon = [load_image('data/icons/player_002.png'), load_image('data/icons/player_002-left.png'), \
    load_image('data/icons/player_002-right.png')]

m1_icon = [load_image('data/icons/missile_001.png'), load_image('data/icons/missile_002.png'),\
    load_image('data/icons/missile_003.png')]

ex1_icon = load_image('data/icons/explosion.png')

m1_sound = [load_sound('data/sound/shoot.wav'), load_sound('data/sound/shoot2.wav')]

ex1_sound = load_sound('data/sound/explosion.wav')

bx1_sound = load_sound('data/sound/package.wav')

object_icons = [e1_icon, e2_icon, e3_icon, e4_icon, e5_icon, e6_icon, e7_icon, \
    p1_icon, p2_icon, m1_icon, ex1_icon, bx1_icon]

object_sounds = [m1_sound, ex1_sound, bx1_sound]

intro(True, screen)

if main(True, screen, object_icons, object_sounds):
    main(True, screen, object_icons, object_sounds)
