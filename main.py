"""Main"""

import random
import pygame

from player import Player
from enemy import Enemy
from text import Text
from explosion import Explosion
from package import Package
from object import Object

from pause import pause
from game_over import game_over
from toolbox import moving_background

def main(state, display, object_icons, object_sounds):
    """Main loop"""

    screen = display[1]
    screen_params = display[0]
    background = display[2]

    player_skin = object_icons[7:9]
    enemy_skin = object_icons[:7]
    missile_skin = object_icons[9]
    explosion_icon = object_icons[10]
    package_icon = object_icons[11]
    asteroid_icon = object_icons[12]
    debris_icon = object_icons[13]

    missile_sound = object_sounds[0]
    explosion_sound = object_sounds[1]
    package_sound = object_sounds[2]

    clock = pygame.time.Clock()

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
    asteroid = []
    debris = []
    number_of_enemies = 0
    is_upgraded = False

    bg1_y = 0
    bg2_y = background.get_height()

    while number_of_enemies < 5:
        enemies.append(Enemy(screen_params, enemy_skin[0]))
        number_of_enemies += 1

    while state:
        clock.tick(60)

        bg1_y, bg2_y = moving_background(background, screen, bg1_y, bg2_y)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause(screen, score, hitpoints)

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
                    if game_over(score, screen, screen_params):
                        return True

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
                    explosion[-1].burst(screen, enemies[i].position[0], enemies[i].position[1])

                    debris.append(Object(debris_icon, screen_params))
                    debris[-1].position[0] = enemies[i].position[0]
                    debris[-1].position[1] = enemies[i].position[1]

                    enemies[i] = Enemy(screen_params, enemy_skin[0])
                    enemies[i].level(score.value, enemy_skin)

                    player.position[0] = 0
                    player.position[1] = screen_params[1] - \
                                        pygame.Surface.get_height(player.icon[0])

                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    state = False
                    if game_over(score, screen, screen_params):
                        return True

            # Check collision with asteroids
            for _i, _ in enumerate(asteroid):
                if asteroid[_i].is_collision(enemies[i].position[0], enemies[i].position[1]):
                    enemies[i].hitpoints -= 1

                    if enemies[i].hitpoints == 0:
                        explosion.append(Explosion(explosion_icon, explosion_sound))
                        explosion[-1].burst2(screen, enemies[i].position[0], enemies[i].position[1])

                        debris.append(Object(debris_icon, screen_params))
                        debris[-1].position[0] = enemies[i].position[0]
                        debris[-1].position[1] = enemies[i].position[1]

                        enemies[i] = Enemy(screen_params, enemy_skin[0])
                        enemies[i].level(score.value, enemy_skin)

                    asteroid[_i].state = False

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
                    explosion[-1].burst(screen, \
                        enemy_missile[i].position[0], enemy_missile[i].position[1])
                    enemy_missile[i].state = False

                elif player.hitpoints == 0:
                    explosion.append(Explosion(explosion_icon, explosion_sound))
                    explosion[-1].burst(screen, \
                        enemy_missile[i].position[0], enemy_missile[i].position[1])
                    state = False
                    if game_over(score, screen, screen_params):
                        return True

            # Check collision with asteroids
            if enemy_missile[i].state:
                for _i, _ in enumerate(asteroid):
                    if asteroid[_i].is_collision(enemy_missile[i].position[0], \
                            enemy_missile[i].position[1]) and enemy_missile[i].state:
                        asteroid[_i].state = False
                        enemy_missile[i].state = False
                        explosion.append(Explosion(explosion_icon, explosion_sound))
                        explosion[-1].burst2(screen, asteroid[_i].position[0], \
                                                        asteroid[_i].position[1])
                        asteroid[_i].state = False

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
                        explosion[-1].burst(screen, enemy_missile[_i].position[0], \
                                                        enemy_missile[_i].position[1])
                        enemy_missile.pop(_i)

            # Check collision with asteroids
            if player_missile[i].state:
                for _i, _ in enumerate(asteroid):
                    if asteroid[_i].is_collision(player_missile[i].position[0], \
                            player_missile[i].position[1]) and player_missile[i].state:
                        asteroid[_i].state = False
                        player_missile[i].state = False
                        explosion.append(Explosion(explosion_icon, explosion_sound))
                        explosion[-1].burst(screen, asteroid[_i].position[0], \
                                                        asteroid[_i].position[1])
                        asteroid[_i].state = False

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
                            explosion[-1].burst(screen, player_missile[i].position[0], \
                                                                player_missile[i].position[1])

                            debris.append(Object(debris_icon, screen_params))
                            debris[-1].position[0] = enemies[_i].position[0]
                            debris[-1].position[1] = enemies[_i].position[1]

                            if random.randint(0, 10) <= enemies[_i].drop_rate:
                                package.append(Package(package_sound, package_icon))
                                package[-1].type = random.choice( \
                                    ['hitpoints', 'skin', 'velocity', 'gun_reload'])
                                package[-1].icon.get(package[-1].type)
                                package[-1].position[0] = enemies[_i].position[0] + \
                                    pygame.Surface.get_width(enemies[_i].icon[0]) / 4
                                package[-1].position[1] = enemies[_i].position[1] + \
                                    pygame.Surface.get_height(enemies[_i].icon[0]) / 4
                                package[-1].state = True
                                screen.blit(package[-1].icon.get(package[-1].type), \
                                    (package[-1].position[0], package[-1].position[1]))

                            enemies[_i] = Enemy(screen_params, enemy_skin[0])
                            enemies[_i].level(score.value, enemy_skin)
                        else:
                            explosion.append(Explosion(explosion_icon, explosion_sound))
                            explosion[-1].burst(screen, player_missile[i].position[0], \
                                                        player_missile[i].position[1])
                            player_missile[i].state = False

            # Remove unnecessary objects
            if not player_missile[i].state:
                player_missile.pop(i)

        # Loop through debris list an do various tasks
        for i, _ in enumerate(debris):
            # Move
            debris[i].move(screen)

            # Check screen leave
            if debris[i].position[1] > screen_params[1]:
                debris[i].state = False

            # Remove unnecessary objects
            if not debris[i].state:
                debris.pop(i)

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

        # Draw explosion
        for i, _ in enumerate(explosion):
            explosion[i].burst_last(screen, explosion[i].position[0], explosion[i].position[1])

            if not explosion[i].state:
                explosion.pop(i)

        # Create asteroids
        if random.randint(0, 200) == 101:
            asteroid.append(Object(asteroid_icon, screen_params))

        # Loop through asteroid list and do various tasks
        for i, _ in enumerate(asteroid):
            # Move
            asteroid[i].move(screen)

            # Check player's ship hit
            if asteroid[i].state and \
                    asteroid[i].is_collision(player.position[0], player.position[1]):
                player.hitpoints -= 1
                hitpoints.value = player.hitpoints

                if player.hitpoints > 0:
                    explosion.append(Explosion(explosion_icon, explosion_sound))
                    explosion[-1].burst(screen, \
                        asteroid[i].position[0], asteroid[i].position[1])
                    asteroid[i].state = False

                elif player.hitpoints == 0:
                    explosion.append(Explosion(explosion_icon, explosion_sound))
                    explosion[-1].burst(screen, \
                        asteroid[i].position[0], asteroid[i].position[1])
                    state = False
                    if game_over(score, screen, screen_params):
                        return True

            # Check screen leave
            if asteroid[i].position[1] > screen_params[1]:
                asteroid[i].state = False

            # Remove unnecessary objects
            if not asteroid[i].state:
                asteroid.pop(i)

        score.draw(screen, 10, 10)
        hitpoints.draw(screen, 10, 30)
        pygame.display.update()
