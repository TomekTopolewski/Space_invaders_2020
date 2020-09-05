"""Space Invaders 2020
Based on a great tutorial "Python game development course" by freeCodeCamp.org.
Icons made by smalllikeart from www.flaticon.com
Background made by vectorpouch from www.freepik.com
Music thanks to www.freesound.org"""

import random
import pygame

from pygame import mixer
from package import Package
from explosion import Explosion
from text import Text
from enemy import Enemy
from player import Player

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

pygame.mixer.pre_init(0, 0, 16, 0)
pygame.init()
screen_params = (827, 900)
screen = pygame.display.set_mode((screen_params[0], screen_params[1]))
pygame.display.set_caption("Space Invaders 2020")
window_icon = load_image('data/icons/aircraft-icon.png')
pygame.display.set_icon(window_icon)
clock = pygame.time.Clock()

try:
    background = [pygame.image.load('data/images/background_001.jpg')]
except pygame.error:
    background = pygame.Surface((screen_params[0], screen_params[1]))
    background.fill((0, 0, 0))

if load_music('data/sound/background.wav') is not False:
    mixer.music.play(-1)

e1 = [load_image('data/icons/enemy_001.png'), \
    load_image('data/icons/enemy_001-left.png'), load_image('data/icons/enemy_001-right.png')]

e2 = [load_image('data/icons/enemy_002.png'), \
    load_image('data/icons/enemy_002-left.png'), load_image('data/icons/enemy_002-right.png')]

e3 = [load_image('data/icons/enemy_003.png'), \
    load_image('data/icons/enemy_003-left.png'), load_image('data/icons/enemy_003-right.png')]

e4 = [load_image('data/icons/enemy_004.png'), \
    load_image('data/icons/enemy_004-left.png'), load_image('data/icons/enemy_004-right.png')]

e5 = [load_image('data/icons/enemy_005.png'), \
    load_image('data/icons/enemy_005-left.png'), load_image('data/icons/enemy_005-right.png')]

e6 = [load_image('data/icons/enemy_006.png'), \
    load_image('data/icons/enemy_006-left.png'), load_image('data/icons/enemy_006-right.png')]

e7 = [load_image('data/icons/enemy_007.png'), \
    load_image('data/icons/enemy_007-left.png'), load_image('data/icons/enemy_007-right.png')]

enemy_skin = [e1, e2, e3, e4, e5, e6, e7]

package_icon = [load_image('data/icons/box_003.png'), \
                load_image('data/icons/box_004.png'), \
                load_image('data/icons/box_001.png'), \
                load_image('data/icons/box_002.png')]

package_sound = load_sound('data/sound/package.wav')

p1 = [load_image('data/icons/player_001.png'), load_image('data/icons/player_001-left.png'), \
                                                load_image('data/icons/player_001-right.png')]
p2 = [load_image('data/icons/player_002.png'), load_image('data/icons/player_002-left.png'), \
                                                load_image('data/icons/player_002-right.png')]

player_skin = [p1, p2]

missile_skin = [load_image('data/icons/missile_001.png'),\
                load_image('data/icons/missile_002.png'),\
                load_image('data/icons/missile_003.png')]
missile_sound = [load_sound('data/sound/shoot.wav'), load_sound('data/sound/shoot2.wav')]

explosion_icon = load_image('data/icons/explosion.png')
explosion_sound = load_sound('data/sound/explosion.wav')

def intro(state):
    """Intro"""
    try:
        lines = open('ReadMe.txt', 'r').readlines()
    except FileNotFoundError:
        lines = ["Can't load intro, press space to play anyway"]

    position = [20, 0]
    intro_font = Text(22, (255, 255, 255), "data/fonts/BebasNeue-Regular.ttf")

    for i in lines:
        render_line = intro_font.font.render(i.strip(), True, intro_font.color)
        screen.blit(render_line, (position[0], position[1]))
        position[1] += 30

    pygame.display.update()
    while state:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                state = False
                pygame.quit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    state = False

def game_over(score):
    """Game over"""
    game_over_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    game_over_txt.text = "Game Over!"

    play_again_txt = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    play_again_txt.text = "Press space to play again"

    screen.blit(background[0], (0, 0))

    game_over_txt.draw_text(screen, 140, 120)
    score.draw(screen, 300, 180)
    play_again_txt.draw_text(screen, 80, 720)
    pygame.display.update()
    game_over_status = True

    while game_over_status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over_status = False
                    main_loop(True)

def pause():
    """Pause"""
    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"
    pause_txt.draw_text(screen, 250, 200)
    pygame.display.update()
    pause_status = True

    while pause_status:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
            if _event.type == pygame.KEYDOWN:
                if _event.key == pygame.K_p:
                    pause_status = False

def main_loop(state):
    """Main loop"""
    clock.tick(23)

    player = Player(7, 3, player_skin[0])

    score = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    score.text = "Score: "

    hitpoints = Text(22, (255, 255, 255), 'data/fonts/space_age.ttf')
    hitpoints.text = "HP: "
    hitpoints.value = player.hitpoints

    package = []
    enemies = []
    enemy_missile = []
    player_missile = []
    explosion = []
    number_of_enemies = 0
    is_upgraded = False

    while number_of_enemies < 5:
        enemies.append(Enemy(screen_params, enemy_skin[0]))
        number_of_enemies += 1

    while state:
        screen.blit(background[0], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

        # Player's move, shoot and reload
        player.move(screen, screen_params)
        player.shoot(player_missile, is_upgraded, missile_skin, missile_sound, -10, 45)

        if player.is_reloading:
            player.reload(500)

        # Loop through the enemy list and do various tasks
        for i, _ in enumerate(enemies):
            # Move
            enemies[i].move(screen, screen_params)

            # Check screen leave
            if enemies[i].position[1] > (screen_params[1] - \
                                    (pygame.Surface.get_height(enemies[i].icon[0]) / 2)):
                player.hitpoints -= 1

                if player.hitpoints >= 1:
                    enemies[i] = Enemy(screen_params, enemy_skin[0])
                    enemies[i].level(score.value, enemy_skin)
                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    state = False
                    game_over(score)

            # Draw hitpoints bar
            enemies[i].draw_hp(screen)

            # Shoot
            enemies[i].shoot(enemy_missile, screen, missile_skin[2], 3, 45)

            # Reload the gun
            if enemies[i].is_reloading:
                enemies[i].reload(150)

            # Check collision with the player
            if player.is_collision(enemies[i].position[0], enemies[i].position[1]):
                player.hitpoints -= 1

                if player.hitpoints >= 1:
                    explosion.append(Explosion(explosion_icon, explosion_sound))
                    explosion[-1].splash(screen, enemies[i].position[0], enemies[i].position[1])
                    enemies[i] = Enemy(screen_params, enemy_skin[0])
                    enemies[i].level(score.value, enemy_skin)
                    player.position[0] = 0
                    player.position[1] = screen_params[1] - \
                                        pygame.Surface.get_height(player.icon[0])
                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    state = False
                    game_over(score)

        # Loop through the enemy's missile list and do various tasks
        for i, _ in enumerate(enemy_missile):
            # Fly
            enemy_missile[i].move(screen)

            # Check screen leave
            if enemy_missile[i].position[1] > screen_params[1]:
                enemy_missile[i].state = False

            # Check the player's ship hit
            hit_x = player.position[0] + (pygame.Surface.get_width(player.icon[0]) / 2)
            hit_y = player.position[1] + (pygame.Surface.get_height(player.icon[0]) / 2)

            if enemy_missile[i].state and enemy_missile[i].is_collision(hit_x, hit_y):
                player.hitpoints -= 1
                hitpoints.value = player.hitpoints

                if player.hitpoints > 0:
                    explosion.append(Explosion(explosion_icon, explosion_sound))
                    explosion[-1].splash(screen, \
                        enemy_missile[i].position[0], enemy_missile[i].position[1])
                    enemy_missile[i].state = False

                elif player.hitpoints == 0:
                    explosion.append(Explosion(explosion_icon, explosion_sound))
                    explosion[-1].splash(screen, \
                        enemy_missile[i].position[0], enemy_missile[i].position[1])
                    state = False
                    game_over(score)

            # Remove unnecessary objects
            if not enemy_missile[i].state:
                enemy_missile.pop(i)

        # Loop through the player's missile list and do various tasks
        for i, _ in enumerate(player_missile):
            # Move
            player_missile[i].move(screen)

            # Check leave
            if player_missile[i].position[1] < -32:
                player_missile[i].state = False

            # Check collision with the enemy's missile
            if player_missile[i].state:
                hit_x = player_missile[i].position[0] + \
                                    (pygame.Surface.get_width(player_missile[i].icon) / 2)
                hit_y = player_missile[i].position[1] + \
                                    (pygame.Surface.get_height(player_missile[i].icon) / 2)

                for _i, _ in enumerate(enemy_missile):
                    if enemy_missile[_i].is_collision(hit_x, hit_y) and \
                                                            enemy_missile[_i].state:
                        enemy_missile[_i].state = False
                        explosion.append(Explosion(explosion_icon, explosion_sound))
                        explosion[-1].splash(screen, enemy_missile[_i].position[0], \
                                                        enemy_missile[_i].position[1])
                        enemy_missile.pop(_i)

            # Check enemy's ship hit
            if player_missile[i].state:
                for _i, _ in enumerate(enemies):
                    hit_x = enemies[_i].position[0] + \
                                                (pygame.Surface.get_width(enemies[_i].icon[0]) / 2)
                    hit_y = enemies[_i].position[1] + \
                                                (pygame.Surface.get_height(enemies[_i].icon[0]) / 2)

                    if player_missile[i].is_collision(hit_x, hit_y):
                        enemies[_i].hitpoints -= 1

                        if enemies[_i].hitpoints == 0:
                            score.value += 1
                            player_missile[i].state = False
                            explosion.append(Explosion(explosion_icon, explosion_sound))
                            explosion[-1].splash(screen, player_missile[i].position[0], \
                                                                player_missile[i].position[1])

                            if random.randint(0, 10) <= enemies[_i].drop_rate:
                                package.append(Package(package_sound, package_icon))
                                package[-1].type = random.choice( \
                                    ['hitpoints', 'skin', 'velocity', 'gun_reload'])
                                package[-1].icon.get(package[-1].type)
                                package[-1].position[0] = enemies[_i].position[0]
                                package[-1].position[1] = enemies[_i].position[1]
                                package[-1].state = True
                                screen.blit(package[-1].icon.get(package[-1].type), \
                                    (package[-1].position[0], package[-1].position[1]))

                            enemies[_i] = Enemy(screen_params, enemy_skin[0])
                            enemies[_i].level(score.value, enemy_skin)
                        else:
                            explosion.append(Explosion(explosion_icon, explosion_sound))
                            explosion[-1].splash(screen, player_missile[i].position[0], \
                                                        player_missile[i].position[1])
                            player_missile[i].state = False

            # Remove unnecessary objects
            if not player_missile[i].state:
                player_missile.pop(i)

        # Fly and open the package
        for i, _ in enumerate(package):
            if package[i].state:
                package[i].move(screen)

            if package[i].is_collision(player.position[0], player.position[1]):
                is_upgraded = package[i].open(player, is_upgraded, player_skin[1])
                package[i].sound.play()
                package[i].state = False
                hitpoints.value = player.hitpoints
                package.pop(i)

        # Spot boss
        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(screen_params, enemy_skin[6]))
            enemies[-1].boss()

        # Draw explosion splash
        for i, _ in enumerate(explosion):
            explosion[i].splash_last(screen, explosion[i].position[0], explosion[i].position[1])

            if not explosion[i].state:
                explosion.pop(i)

        score.draw(screen, 10, 10)
        hitpoints.draw(screen, 10, 30)
        pygame.display.update()

intro(True)
main_loop(True)
