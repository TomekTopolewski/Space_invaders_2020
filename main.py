"""Main"""

import random
import pygame

from player import Player
from enemy import Enemy
from text import Text
from object import Object

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
        enemies.append(Enemy(display[0], enemy_icon[0]))
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
                    pause(display, score, hitpoints)

        # Player's move, shoot and reload
        player.move(display[1], display[0])

        if is_upgraded:
            player.shoot(player_missile, missile_icon[0])
        else:
            player.shoot(player_missile, missile_icon[1])

        if player.is_reloading:
            player.reload(500)

        # Loop through the enemy list and do various tasks
        for i, _ in enumerate(enemies):
            # Move
            enemies[i].move(display[:2])

            # Check screen leave
            if enemies[i].position[1] > (display[0][1] - (enemies[i].icon[0].get_height() / 2)):
                player.hitpoints -= 1

                if player.hitpoints >= 1:
                    enemies[i] = Enemy(display[0], enemy_icon[0])
                    enemies[i].level(score.value, enemy_icon)
                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    state = False
                    if game_over(score, display):
                        return True

            # Draw hitpoints bar
            enemies[i].draw_hp(display[1])

            # Shoot
            enemies[i].shoot(enemy_missile, missile_icon[2])

            # Reload the gun
            if enemies[i].is_reloading:
                enemies[i].reload(150)

            # Check collision with the player
            if is_collision(player, enemies[i], 40):
                player.hitpoints -= 1

                explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                explosion[-1].burst(display[1], enemies[i].position)
                explosion[-1].sound.set_volume(0.25)
                explosion[-1].sound.play()

                debris.append(Object(debris_icon, enemies[i].position, 0.5, False))
                debris[-1].state = True

                hitpoints.value = player.hitpoints

                if player.hitpoints >= 1:
                    enemies[i] = Enemy(display[0], enemy_icon[0])
                    enemies[i].level(score.value, enemy_icon)

                    player.position[0] = 0
                    player.position[1] = display[0][1] - player.icon[0].get_height()
                else:
                    state = False
                    if game_over(score, display):
                        return True

            # Check collision with asteroids
            for _i, _ in enumerate(asteroid):
                if is_collision(asteroid[_i], enemies[i], 40):
                    enemies[i].hitpoints -= 1

                    explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                    explosion[-1].burst(display[1], asteroid[_i].position)

                    if enemies[i].hitpoints == 0:
                        debris.append(Object(debris_icon, enemies[i].position, 0.5, False))
                        debris[-1].state = True

                        enemies[i] = Enemy(display[0], enemy_icon[0])
                        enemies[i].level(score.value, enemy_icon)

                    asteroid.pop(_i)

        # Loop through the enemy's missile list and do various tasks
        for i, _ in enumerate(enemy_missile):
            # Fly
            enemy_missile[i].movex(display[1])

            # Check screen leave
            if enemy_missile[i].position[1] > display[0][1]:
                enemy_missile[i].state = False

            # Check the player's ship hit
            if enemy_missile[i].state and is_collision(enemy_missile[i], player, 40):
                player.hitpoints -= 1
                hitpoints.value = player.hitpoints
                enemy_missile[i].state = False

                explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                explosion[-1].burst(display[1], enemy_missile[i].position)
                explosion[-1].sound.set_volume(0.25)
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    state = False
                    if game_over(score, display):
                        return True

            # Check collision with asteroids
            if enemy_missile[i].state:
                for _i, _ in enumerate(asteroid):
                    if is_collision(asteroid[_i], enemy_missile[i], 40):
                        explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                        explosion[-1].burst(display[1], asteroid[_i].position)
                        asteroid.pop(_i)
                        enemy_missile[i].state = False

            # Remove unnecessary objects
            if not enemy_missile[i].state:
                enemy_missile.pop(i)

        # Loop through the player's missile list and do various tasks
        for i, _ in enumerate(player_missile):
            # Move
            player_missile[i].movex(display[1])

            # Check leave
            if player_missile[i].position[1] < -32:
                player_missile[i].state = False

            # Check collision with the enemy's missile
            if player_missile[i].state:
                for _i, _ in enumerate(enemy_missile):
                    if is_collision(enemy_missile[_i], player_missile[i], 40):
                        explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                        explosion[-1].burst(display[1], enemy_missile[_i].position)
                        explosion[-1].sound.set_volume(0.25)
                        explosion[-1].sound.play()
                        enemy_missile.pop(_i)
                        player_missile[i].state = False

            # Check collision with asteroids
            if player_missile[i].state:
                for _i, _ in enumerate(asteroid):
                    if is_collision(asteroid[_i], player_missile[i], 40):
                        explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                        explosion[-1].burst(display[1], player_missile[i].position)
                        explosion[-1].sound.set_volume(0.25)
                        explosion[-1].sound.play()
                        asteroid.pop(_i)
                        player_missile[i].state = False

            # Check collision with debris
            if player_missile[i].state:
                for _i, _ in enumerate(debris):
                    if is_collision(debris[_i], player_missile[i], 40):
                        explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                        explosion[-1].burst(display[1], player_missile[i].position)
                        explosion[-1].sound.set_volume(0.25)
                        explosion[-1].sound.play()
                        debris.pop(_i)
                        player_missile[i].state = False

            # Check enemy's ship hit
            if player_missile[i].state:
                for _i, _ in enumerate(enemies):
                    if is_collision(player_missile[i], enemies[_i], 40):
                        enemies[_i].hitpoints -= 1
                        player_missile[i].state = False

                        explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                        explosion[-1].burst(display[1], player_missile[i].position)
                        explosion[-1].sound.set_volume(0.25)
                        explosion[-1].sound.play()

                        if enemies[_i].hitpoints == 0:
                            score.value += 1
                            debris.append(Object(debris_icon, enemies[_i].position, 0.5, False))
                            debris[-1].state = True

                            if random.randint(0, 10) <= enemies[_i].drop_rate:
                                ptype = random.randint(0, 3)
                                package.append(Object([package_icon[ptype]], [0, 0], 0.5, package_sound))

                                package[-1].position[0] = enemies[_i].position[0] + \
                                    enemies[_i].icon[0].get_width() / 4
                                package[-1].position[1] = enemies[_i].position[1] + \
                                    enemies[_i].icon[0].get_height() / 4
                                package[-1].state = True
                                package[-1].sound.set_volume(0.20)
                                package[-1].type = ptype

                            enemies[_i] = Enemy(display[0], enemy_icon[0])
                            enemies[_i].level(score.value, enemy_icon)

            # Remove unnecessary objects
            if not player_missile[i].state:
                player_missile.pop(i)

        # Loop through debris list an do various tasks
        for i, _ in enumerate(debris):

            # Slowly disappear
            debris[i].keep(display[1])

            # Check player's ship hit
            if is_collision(debris[i], player, 40):
                player.hitpoints -= 1
                hitpoints.value = player.hitpoints

                explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                explosion[-1].burst(display[1], debris[i].position)
                explosion[-1].sound.set_volume(0.25)
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    state = False
                    if game_over(score, display):
                        return True

                debris[i].state = False

            # Check screen leave
            if debris[i].state and debris[i].position[1] > display[0][1]:
                debris[i].state = False

            # Remove unnecessary objects
            if not debris[i].state:
                debris.pop(i)

        # Fly and open the package
        for i, _ in enumerate(package):
            package[i].movex(display[1])

            if is_collision(package[i], player, 40):
                is_upgraded = package[i].open(player, is_upgraded, player_icon[1], missile_sound[1])
                package[i].sound.play()
                hitpoints.value = player.hitpoints
                package.pop(i)

        # Spot boss
        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(display[0], enemy_icon[6]))
            enemies[-1].boss()

        # Draw explosion
        for i, _ in enumerate(explosion):
            explosion[i].burst_last(display[1])

            if not explosion[i].state:
                explosion.pop(i)

        # Create asteroids
        if random.randint(0, 70) == 42:
            asteroid.append(Object([random.choice(asteroid_icon)], \
                [random.randint(5, display[0][0] - 50), -30], 0.5, 0))
            asteroid[-1].state = True

        # Loop through asteroid list and do various tasks
        for i, _ in enumerate(asteroid):
            # Move
            asteroid[i].movex(display[1])

            # Check player's ship hit
            if is_collision(asteroid[i], player, 40):
                player.hitpoints -= 1
                hitpoints.value = player.hitpoints

                explosion.append(Object(explosion_icon, [0, 0], False, explosion_sound))
                explosion[-1].burst(display[1], asteroid[i].position)
                explosion[-1].sound.set_volume(0.25)
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    state = False
                    if game_over(score, display):
                        return True

                asteroid[i].state = False

            # Check screen leave
            if asteroid[i].state and asteroid[i].position[1] > display[0][1]:
                asteroid[i].state = False

            # Remove unnecessary objects
            if not asteroid[i].state:
                asteroid.pop(i)

        score.draw(display[1], 10, 10)
        hitpoints.draw(display[1], 10, 30)
        pygame.display.update()
