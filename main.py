"""Main"""

import pygame
from game import game
from menu import menu
from game_over import game_over
from toolbox import load_img, load_sound

pygame.init()

pygame.display.set_caption("Space Invaders 2020")
window_icon = load_img('data/icons/aircraft-icon.png')
pygame.display.set_icon(window_icon)

screen = [(827, 880)]
screen.append(pygame.display.set_mode((screen[0][0], screen[0][1])))
screen.append(load_img('data/images/background_004.jpg'))

pygame.mouse.set_visible(0)

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

missile = [load_img('data/icons/missile_001.png'), load_img('data/icons/missile_002.png'),\
    load_img('data/icons/missile_003.png')]

explosion = load_img('data/icons/explosion.png')

asteroid = [load_img('data/icons/asteroid_001.png'), load_img('data/icons/asteroid_002.png'),\
    load_img('data/icons/asteroid_003.png'), load_img('data/icons/asteroid_004.png'), \
    load_img('data/icons/asteroid_005.png')]

debris = [load_img('data/icons/debris_001.png'), load_img('data/icons/debris_002.png'), \
    load_img('data/icons/debris_003.png')]

m_sound = [load_sound('data/sound/shoot.wav'), load_sound('data/sound/shoot2.wav')]
exp_sound = load_sound('data/sound/explosion.wav')
box_sound = load_sound('data/sound/package.wav')
enter_game = load_sound('data/sound/button.wav')

object_icons = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6, enemy7, \
    player1, player2, missile, explosion, box, asteroid, debris]

object_sounds = [m_sound, exp_sound, box_sound]

while True:
    vol = menu(screen, 0.2)

    enter_game.set_volume(vol)
    enter_game.play()

    vol, score = game(screen, object_icons, object_sounds, vol)

    game_over(score, screen)
