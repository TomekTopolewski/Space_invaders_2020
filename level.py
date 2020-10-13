"""Level"""

import sys
import random
import pygame

from pygame import mixer
from enemy import Enemy
from text import Text
from objects import Object

from pause import pause
from toolbox import moving_bkgd, is_collision

def rand_pos(scrn_param):
    """scrn_param"""
    pos_x = random.randint(0, scrn_param[0])
    pos_y = random.randint(0, scrn_param[1])
    return pos_x, pos_y

def out_of_screen(objects, scrn):
    """objects, scrn"""
    for obj in objects:
        if obj.pos[1] > scrn[1] or obj.pos[1] < -100:
            objects.remove(obj)

def level(scrn, score, vol, obj_icons, obj_sounds, player):
    """scrn, score, vol, obj_icons, obj_sounds, player)"""

    clock = pygame.time.Clock()

    hpoints = Text(22, (255, 255, 255), 'data/fonts/space_age.ttf')
    hpoints.text = "HP: "

    boxes = list()
    enemies = list()
    enemy_missiles = list()
    player_missiles = list()
    explosions = list()
    asteroids = list()

    bkgd_pos = [0, -scrn[0][1]]

    while len(asteroids) < 8:
        asteroids.append(Object(obj_icons[2], list(rand_pos(scrn[0])), 0.5))

    while True:
        clock.tick(60)

        bkgd_pos = moving_bkgd(scrn, bkgd_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    vol = pause(scrn, score, hpoints, vol)

        if random.randint(0, 100) == 1:
            pos = rand_pos(scrn[0])
            asteroids.append(Object(obj_icons[2], [pos[0], - 50], 0.5))

        for asteroid in asteroids:
            asteroid.move(scrn[1])

        out_of_screen(asteroids, scrn[0])

        while len(enemies) < 5:
            pos = rand_pos(scrn[0])
            enemies.append(Enemy([pos[0], -50], obj_icons[0], 4000, 2))

        for enemy in enemies:
            enemy.move(scrn[:2])
            enemy.draw_hp(scrn[1])
            enemy.shoot(enemy_missiles, obj_icons[1][2])

            if is_collision(enemy, player, 40):
                enemy.hpoints -= 1
                player.hpoints -= 1
                explosions.append(Object(obj_icons[3], player.pos, sound = obj_sounds[1]))
                explosions[-1].sound.play()

                if enemy.hpoints == 0:
                    enemies.remove(enemy)
                    continue

            if enemy.pos[1] > scrn[0][1]:
                player.hpoints -= 1
                enemies.remove(enemy)

        player.move(scrn[:2])
        player.shoot(player_missiles, obj_icons[1][0], obj_sounds[0])

        for missile in player_missiles:
            missile.move(scrn[1])

        out_of_screen(player_missiles, scrn[0])

        for missile in enemy_missiles:
            missile.move(scrn[1])

        out_of_screen(enemy_missiles, scrn[0])

        mixer.music.set_volume(vol)
        for obj in explosions + boxes + player_missiles:
            if obj.sound:
                obj.sound.set_volume(vol)

        for asteroid in asteroids:
            if is_collision(player, asteroid, 40):
                player.hpoints -= 1
                explosions.append(Object(obj_icons[3], player.pos, sound = obj_sounds[1]))
                explosions[-1].sound.play()
                asteroids.remove(asteroid)
                break

        for asteroid in asteroids:
            for missile in player_missiles:
                if is_collision(asteroid, missile, 40):
                    explosions.append(Object(obj_icons[3], missile.pos, sound = obj_sounds[1]))
                    explosions[-1].sound.play()
                    asteroids.remove(asteroid)
                    player_missiles.remove(missile)
                    break

        for asteroid in asteroids:
            for missile in enemy_missiles:
                if is_collision(asteroid, missile, 40):
                    explosions.append(Object(obj_icons[3], missile.pos))
                    asteroids.remove(asteroid)
                    enemy_missiles.remove(missile)
                    break

        for missile in enemy_missiles:
            if is_collision(missile, player, 40):
                player.hpoints -= 1
                explosions.append(Object(obj_icons[3], missile.pos, sound = obj_sounds[1]))
                explosions[-1].sound.play()
                enemy_missiles.remove(missile)
                break

        for emissile in enemy_missiles:
            for pmissile in player_missiles:
                if is_collision(emissile, pmissile, 30):
                    explosions.append(Object(obj_icons[3], emissile.pos, sound = obj_sounds[1]))
                    explosions[-1].sound.play()
                    enemy_missiles.remove(emissile)
                    player_missiles.remove(pmissile)
                    break

        for enemy in enemies:
            for missile in player_missiles:
                if is_collision(enemy, missile, 40):
                    enemy.hpoints -= 1
                    explosions.append(Object(obj_icons[3], missile.pos, sound = obj_sounds[1]))
                    explosions[-1].sound.play()

                    if enemy.hpoints == 0:
                        score.value += 1
                        enemies.remove(enemy)

                    player_missiles.remove(missile)

        for explosion in explosions:
            if pygame.time.get_ticks() - explosion.time0 < 200:
                scrn[1].blit(explosion.icon[0], (explosion.pos))
            else:
                explosions.remove(explosion)

        if player.hpoints == 0:
            return score, player, vol

        score.draw(scrn[1], [10, 10])
        hpoints.value = player.hpoints
        hpoints.draw(scrn[1], [10, 30])

        pygame.display.update()
