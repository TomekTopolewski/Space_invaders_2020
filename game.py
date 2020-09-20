"""Main game file"""

import pygame
from main import main
from menu import intro
from game_over import game_over
from toolbox import load_img, load_sound

pygame.init()

pygame.display.set_caption("Space Invaders 2020")
window_icon = load_img('data/icons/aircraft-icon.png')
pygame.display.set_icon(window_icon)

bkgd = [load_img('data/images/background_004.jpg'), \
    load_img('data/images/background_004a.jpg'), \
    load_img('data/images/background_004b.jpg'), \
    load_img('data/images/background_004c.jpg'), \
    load_img('data/images/background_004d.jpg'), \
    load_img('data/images/background_004e.jpg')]

# Build screen
screen = [(827, 880)]
screen.append(pygame.display.set_mode((screen[0][0], screen[0][1])))
screen.append(bkgd)

# Hide default cursor
pygame.mouse.set_visible(0)

# Load icons
enemy1 = [load_img('data/icons/enemy_001.png'), load_img('data/icons/enemy_001-left.png'), \
    load_img('data/icons/enemy_001-right.png')]

enemy2 = [load_img('data/icons/enemy_002.png'), load_img('data/icons/enemy_002-left.png'), \
    load_img('data/icons/enemy_002-right.png')]

enemy3 = [load_img('data/icons/enemy_003.png'), load_img('data/icons/enemy_003-left.png'), \
    load_img('data/icons/enemy_003-right.png')]

enemy4 = [load_img('data/icons/enemy_004.png'), load_img('data/icons/enemy_004-left.png'), \
    load_img('data/icons/enemy_004-right.png')]

enemy5 = [load_img('data/icons/enemy_005.png'), load_img('data/icons/enemy_005-left.png'), \
    load_img('data/icons/enemy_005-right.png')]

enemy6 = [load_img('data/icons/enemy_006.png'), load_img('data/icons/enemy_006-left.png'), \
    load_img('data/icons/enemy_006-right.png')]

enemy7 = [load_img('data/icons/enemy_007.png'), load_img('data/icons/enemy_007-left.png'), \
    load_img('data/icons/enemy_007-right.png')]

box = [load_img('data/icons/box_003.png'), load_img('data/icons/box_004.png'), \
    load_img('data/icons/box_001.png'), load_img('data/icons/box_002.png')]

player1 = [load_img('data/icons/player_001.png'), load_img('data/icons/player_001-left.png'), \
    load_img('data/icons/player_001-right.png')]

player2 = [load_img('data/icons/player_002.png'), load_img('data/icons/player_002-left.png'), \
    load_img('data/icons/player_002-right.png')]

missile1 = [load_img('data/icons/missile_001.png'), load_img('data/icons/missile_002.png'),\
    load_img('data/icons/missile_003.png')]

explosion1 = load_img('data/icons/explosion.png')

asteroid1 = [load_img('data/icons/asteroid_001.png'), load_img('data/icons/asteroid_002.png'),\
    load_img('data/icons/asteroid_003.png'), load_img('data/icons/asteroid_004.png'), \
    load_img('data/icons/asteroid_005.png')]

debris1 = [load_img('data/icons/debris_001.png'), load_img('data/icons/debris_002.png'), \
    load_img('data/icons/debris_003.png')]

# Load sounds
missile1s = [load_sound('data/sound/shoot.wav'), load_sound('data/sound/shoot2.wav')]

explosion1s = load_sound('data/sound/explosion.wav')

box1s = load_sound('data/sound/package.wav')

# Build a list with icons
object_icons = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, \
    player1, player2, missile1, explosion1, box, asteroid1, debris1]

# Build a list with sounds
object_sounds = [missile1s, explosion1s, box1s]

vol = 0.2

# Start game
while True:
    vol = intro(screen, vol)

    vol, score = main(screen, object_icons, object_sounds, vol)

    game_over(score, screen, vol)
