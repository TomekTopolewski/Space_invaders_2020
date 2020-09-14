"""Main game file"""

import pygame
from main import main
from intro import intro
from toolbox import load_image, load_sound

pygame.init()

pygame.display.set_caption("Space Invaders 2020")
window_icon = load_image('data/icons/aircraft-icon.png')
pygame.display.set_icon(window_icon)

bg1_icon = [load_image('data/images/background_004.jpg'), \
    load_image('data/images/background_004a.jpg'), \
    load_image('data/images/background_004b.jpg'), \
    load_image('data/images/background_004c.jpg'), \
    load_image('data/images/background_004d.jpg'), \
    load_image('data/images/background_004e.jpg')]

# Build screen
screen = [(827, 880)]
screen.append(pygame.display.set_mode((screen[0][0], screen[0][1])))
screen.append(bg1_icon)

# Hide default cursor
pygame.mouse.set_visible(0)

# Load icons
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

as1_icon = [load_image('data/icons/asteroid_001.png'), load_image('data/icons/asteroid_002.png'),\
    load_image('data/icons/asteroid_003.png'), load_image('data/icons/asteroid_004.png'), \
    load_image('data/icons/asteroid_005.png')]

de1_icon = [load_image('data/icons/debris_001.png'), load_image('data/icons/debris_002.png'), \
    load_image('data/icons/debris_003.png')]

# Load sounds
m1_sound = [load_sound('data/sound/shoot.wav'), load_sound('data/sound/shoot2.wav')]

ex1_sound = load_sound('data/sound/explosion.wav')

bx1_sound = load_sound('data/sound/package.wav')

# Build a list with icons
object_icons = [e1_icon, e2_icon, e3_icon, e4_icon, e5_icon, e6_icon, e7_icon, \
    p1_icon, p2_icon, m1_icon, ex1_icon, bx1_icon, as1_icon, de1_icon]

# Build a list with sounds
object_sounds = [m1_sound, ex1_sound, bx1_sound]

#Game sequence
intro(True, screen)

while main(True, screen, object_icons, object_sounds):
    main(True, screen, object_icons, object_sounds)
