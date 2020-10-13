"""Game"""

from text import Text
from level import level
from player import Player
from toolbox import load_img, load_sound

def game2(scrn, vol):
    """scrn, vol"""

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

    box = [load_img('data/icons/box_001.png'), load_img('data/icons/box_002.png'), \
        load_img('data/icons/box_003.png'), load_img('data/icons/box_004.png')]

    player1 = [load_img('data/icons/player_001.png'), load_img('data/icons/player_001-left.png'), \
        load_img('data/icons/player_001-right.png')]

    player2 = [load_img('data/icons/player_002.png'), load_img('data/icons/player_002-left.png'), \
        load_img('data/icons/player_002-right.png')]

    missile = [load_img('data/icons/missile_002.png'), load_img('data/icons/missile_001.png'),\
        load_img('data/icons/missile_003.png')]

    explosion = load_img('data/icons/explosion.png')

    asteroid = [load_img('data/icons/asteroid_001.png'), load_img('data/icons/asteroid_002.png'),\
        load_img('data/icons/asteroid_003.png'), load_img('data/icons/asteroid_004.png'), \
        load_img('data/icons/asteroid_005.png')]

    m_sound = [load_sound('data/sound/shoot.wav'), load_sound('data/sound/shoot2.wav')]
    exp_sound = load_sound('data/sound/explosion.wav')
    box_sound = load_sound('data/sound/package.wav')


    score = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    score.text = "Score: "

    player = Player(7, 3, player1)

    obj_icons = [enemy1, missile, asteroid[0], explosion, box]
    obj_sounds = [m_sound[0], exp_sound, box_sound]

    score, player, vol = level(scrn, score, vol, obj_icons, obj_sounds, player)

    if player.hpoints == 0:
        return score, vol
