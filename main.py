"""Main"""

import random
import pygame

from player import Player
from enemy import Enemy
from text import Text
from objects import Object

from pause import pause
from game_over import game_over
from toolbox import moving_background2, is_collision

if not pygame.mixer:
    print("Pygame mixer module not available")

def main(state, display, object_icons, object_sounds):
    """Main loop"""

    player_icon = object_icons[7:9]
    enemy_icon = object_icons[:7]
    missile_icon = object_icons[9]
    explosion_icon = object_icons[10]
    package_icon = object_icons[11]
    asteroid_icon = object_icons[12]
    debris_icon = object_icons[13]

    missile_sound = object_sounds[0]
    explosion_sound = object_sounds[1]
    package_sound = object_sounds[2]

    clock = pygame.time.Clock()

    player = Player(7, 3, player_icon[0], missile_sound[0])

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
    asteroid = []
    debris = []
    number_of_enemies = 0
    is_upgraded = False

    bg1_y = 0
    bg2_y = display[2][0].get_height() * -1

    while number_of_enemies < 5:
        enemies.append(Enemy(display[0], enemy_icon[0], 4000))
        number_of_enemies += 1

    while state:
        clock.tick(60)

        bg1_y, bg2_y = moving_background2(display[2][0], display[1], bg1_y, bg2_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if pause(display, score, hitpoints):
                        return True

        # Player's move
        player.move(display[1], display[0])

        # Player's shoot
        if is_upgraded:
            player.shoot(player_missile, missile_icon[0])
        else:
            player.shoot(player_missile, missile_icon[1])

        # Player's collision with environment
        player_envi = enemies + enemy_missile + debris + asteroid
        for i, _ in enumerate(player_envi):

            if player_envi[i].state and is_collision(player_envi[i], player, 40):
                player.hitpoints -= 1

                explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                explosion[-1].burst(display[1], player_envi[i].position)
                explosion[-1].sound.set_volume(0.25)
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    player.state = False

                player_envi[i].state = False

        # Enemies collision with environment
        enemy_envi = player_missile + asteroid
        for i, _ in enumerate(enemies):
            for _i, _ in enumerate(enemy_envi):
                if enemy_envi[_i].state and is_collision(enemy_envi[_i], enemies[i], 40):
                    enemies[i].hitpoints -= 1

                    explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                    explosion[-1].burst(display[1], enemy_envi[_i].position)
                    explosion[-1].sound.set_volume(0.25)
                    explosion[-1].sound.play()

                    if enemies[i].hitpoints == 0:
                        if enemy_envi[_i].type == 4:
                            score.value += 1
                        enemies[i].state = False

                    enemy_envi[_i].state = False

        # Player's missiles collision with environment
        missile_envi = debris + asteroid + enemy_missile
        for i, _ in enumerate(player_missile):
            for _i, _ in enumerate(missile_envi):
                if missile_envi[_i].state and is_collision(missile_envi[_i], player_missile[i], 40):
                    missile_envi[_i].hitpoints -= 1

                    explodex = missile_envi[_i].position[0] + \
                        missile_envi[_i].icon[0].get_width() / 2
                    explodey = missile_envi[_i].position[1] + \
                        missile_envi[_i].icon[0].get_height() / 2

                    explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                    explosion[-1].burst(display[1], [explodex, explodey])
                    explosion[-1].sound.set_volume(0.25)
                    explosion[-1].sound.play()

                    if missile_envi[_i].hitpoints == 0:
                        missile_envi[_i].state = False

                    player_missile[i].state = False

        # Enemies
        for i, _ in enumerate(enemies):
            if not enemies[i].state:
                debris.append(Object(debris_icon, enemies[i].position, 0.5, False))
                debris[-1].state = True

                if random.randint(0, 10) <= enemies[i].drop_rate:
                    ptype = random.randint(0, 3)
                    package.append(Object(\
                        [package_icon[ptype]], [0, 0], 0.5, package_sound))

                    package[-1].position[0] = enemies[i].position[0] + \
                        enemies[i].icon[0].get_width() / 4
                    package[-1].position[1] = enemies[i].position[1] + \
                        enemies[i].icon[0].get_height() / 4
                    package[-1].state = True
                    package[-1].sound.set_volume(0.20)
                    package[-1].type = ptype

                enemies[i] = Enemy(display[0], enemy_icon[0], 4000)
                enemies[i].level(score.value, enemy_icon)

            enemies[i].move(display[:2])

            if enemies[i].position[1] > (display[0][1] - (enemies[i].icon[0].get_height() / 2)):
                player.hitpoints -= 1

                enemies[i] = Enemy(display[0], enemy_icon[0], 4000)
                enemies[i].level(score.value, enemy_icon)

                if player.hitpoints == 0:
                    player.state = False

            enemies[i].draw_hp(display[1])

            enemies[i].shoot(enemy_missile, missile_icon[2])

        # Enemy's missiles
        for i, _ in enumerate(enemy_missile):
            if enemy_missile[i].state:
                enemy_missile[i].movex(display[1])

                if enemy_missile[i].position[1] > display[0][1]:
                    enemy_missile[i].state = False

                for _i, _ in enumerate(asteroid):
                    if is_collision(asteroid[_i], enemy_missile[i], 40):
                        asteroid[_i].hitpoints -= 1

                        explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                        explosion[-1].burst(display[1], asteroid[_i].position)

                        if asteroid[_i].hitpoints == 0:
                            asteroid[_i].state = False

                        enemy_missile[i].state = False

            if not enemy_missile[i].state:
                enemy_missile.pop(i)

        # Player's missiles
        for i, _ in enumerate(player_missile):
            if player_missile[i].state:
                player_missile[i].movex(display[1])

                if player_missile[i].position[1] < -32:
                    player_missile[i].state = False

            if not player_missile[i].state:
                player_missile.pop(i)

        # Debrises
        for i, _ in enumerate(debris):
            if debris[i].state:
                debris[i].keep(display[1])

                if debris[i].position[1] > display[0][1]:
                    debris[i].state = False

            if not debris[i].state:
                debris.pop(i)

        # Packages
        for i, _ in enumerate(package):
            package[i].movex(display[1])

            if is_collision(package[i], player, 40):
                is_upgraded = package[i].open(player, is_upgraded, player_icon[1], missile_sound[1])
                package[i].sound.play()
                package.pop(i)

        # Spot boss
        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(display[0], enemy_icon[6], 2500))
            enemies[-1].boss()

        # Draw explosions
        for i, _ in enumerate(explosion):
            explosion[i].burst_last(display[1])

            if not explosion[i].state:
                explosion.pop(i)

        # Create asteroids
        if random.randint(0, 70) == 42:
            asteroid.append(Object([random.choice(asteroid_icon)], \
                [random.randint(5, display[0][0] - 50), -30], 0.5, 0))
            asteroid[-1].state = True

        # Asteroids
        for i, _ in enumerate(asteroid):
            if asteroid[i].state:
                asteroid[i].movex(display[1])

                if asteroid[i].position[1] > display[0][1]:
                    asteroid[i].state = False

            if not asteroid[i].state:
                asteroid.pop(i)

        # Game over
        if not player.state:
            state = False
            if game_over(score, display):
                return True

        score.draw(display[1], [10, 10])
        hitpoints.value = player.hitpoints
        hitpoints.draw(display[1], [10, 30])
        pygame.display.update()
