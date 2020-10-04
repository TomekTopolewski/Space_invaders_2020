"""Game"""

import sys
import random
import pygame

from pygame import mixer
from player import Player
from enemy import Enemy
from text import Text
from objects import Object

from pause import pause
from toolbox import moving_bkgd, is_collision

def game(scrn, obj_icons, obj_sounds, vol):
    """scrn, obj_icons, obj_sounds, vol"""

    clock = pygame.time.Clock()

    player = Player(7, 3, obj_icons[7:9][0])

    score = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    score.text = "Score: "

    hitpoints = Text(22, (255, 255, 255), 'data/fonts/space_age.ttf')
    hitpoints.text = "HP: "
    hitpoints.value = player.hitpoints

    boxes = list()
    enemies = list()
    enemy_missiles = list()
    player_missiles = list()
    explosions = list()
    asteroids = list()
    debris = list()
    is_upgraded = False

    bkgd_one = 0
    bkgd_two = scrn[2].get_height() * -1

    number_of_enemies = 5

    while True:
        clock.tick(60)

        bkgd_one, bkgd_two = moving_bkgd(scrn, bkgd_one, bkgd_two)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    vol = pause(scrn, score, hitpoints, vol)


        while len(enemies) < number_of_enemies:
            enemies.append(Enemy(scrn[0], obj_icons[:7][random.randint(0, 5)], 4000))

        player.move(scrn)

        if is_upgraded:
            player.shoot(player_missiles, obj_icons[9][0], obj_sounds[0][1])
        else:
            player.shoot(player_missiles, obj_icons[9][1], obj_sounds[0][0])

        for enemy in enemies:
            if is_collision(player, enemy, 40):
                player.hitpoints -= 1

                explosions.append(Object(obj_icons[10], enemy.pos, False, obj_sounds[1]))
                explosions[-1].state = True
                explosions[-1].sound.play()

                if player.hitpoints == 0:
                    return vol, score

                enemies.remove(enemy)

        for missile in enemy_missiles:
            if is_collision(player, missile, 40):
                player.hitpoints -= 1

                explosions.append(Object(obj_icons[10], missile.pos, False, obj_sounds[1]))
                explosions[-1].state = True
                explosions[-1].sound.play()

                if player.hitpoints == 0:
                    return vol, score

                enemy_missiles.remove(missile)

        for asteroid in asteroids:
            if is_collision(player, asteroid, 40):
                player.hitpoints -= 1

                explosions.append(Object(obj_icons[10], asteroid.pos, False, obj_sounds[1]))
                explosions[-1].state = True
                explosions[-1].sound.play()

                if player.hitpoints == 0:
                    return vol, score

                asteroids.remove(asteroid)

        for enemy in enemies:
            for missile in player_missiles:
                if is_collision(enemy, missile, 40):
                    enemy.hitpoints -= 1

                    explosions.append(Object(obj_icons[10], missile.pos, False, obj_sounds[1]))
                    explosions[-1].state = True
                    explosions[-1].sound.play()

                    if enemy.hitpoints == 0:
                        score.value += 1

                        debris.append(Object(obj_icons[13], enemy.pos, 0.5, False))
                        debris[-1].state = True

                        if random.randint(0, 15) <= enemy.drop:
                            ptype = random.randint(0, 3)
                            boxes.append(Object([obj_icons[11][ptype]], \
                                enemy.pos, 0.25, obj_sounds[2]))
                            boxes[-1].state = True
                            boxes[-1].type = ptype

                        enemies.remove(enemy)
                        player_missiles.remove(missile)
                        break

                    player_missiles.remove(missile)

        for enemy in enemies:
            for asteroid in asteroids:
                if is_collision(enemy, asteroid, 40):
                    enemy.hitpoints -= 1

                    explosions.append(Object(obj_icons[10], asteroid.pos, False, obj_sounds[1]))
                    explosions[-1].state = True

                    if enemy.hitpoints == 0:
                        debris.append(Object(obj_icons[13], enemy.pos, 0.5, False))
                        debris[-1].state = True

                        enemies.remove(enemy)
                        asteroids.remove(asteroid)
                        break

                    asteroids.remove(asteroid)

        for missile in player_missiles:
            for asteroid in asteroids:
                if is_collision(missile, asteroid, 40):
                    asteroid.hitpoints -= 1

                    explosions.append(Object(obj_icons[10], missile.pos, False, obj_sounds[1]))
                    explosions[-1].state = True
                    explosions[-1].sound.play()

                    if asteroid.hitpoints == 0:
                        asteroids.remove(asteroid)

                    player_missiles.remove(missile)
                    break

        for player_missile in player_missiles:
            for enemy_missile in  enemy_missiles:
                if is_collision(player_missile, enemy_missile, 40):
                    enemy_missile.hitpoints -= 1

                    explosions.append(Object(obj_icons[10], player_missile.pos, \
                        False, obj_sounds[1]))
                    explosions[-1].state = True
                    explosions[-1].sound.play()

                    if enemy_missile.hitpoints == 0:
                        enemy_missiles.remove(enemy_missile)

                    player_missiles.remove(player_missile)
                    break

        for missile in enemy_missiles:
            for asteroid in asteroids:
                if is_collision(missile, asteroid, 40):
                    asteroid.hitpoints -= 1

                    explosions.append(Object(obj_icons[10], asteroid.pos, False, False))
                    explosions[-1].state = True

                    if asteroid.hitpoints == 0:
                        asteroids.remove(asteroid)

                    enemy_missiles.remove(missile)
                    break

        for enemy in enemies:
            enemy.move(scrn[:2])
            enemy.draw_hp(scrn[1])
            enemy.shoot(enemy_missiles, obj_icons[9][2])

            if enemy.pos[1] > (scrn[0][1] - (enemy.icon[0].get_height() / 2)):
                player.hitpoints -= 1
                enemies.remove(enemy)

                if player.hitpoints == 0:
                    return vol, score

        for missile in player_missiles:
            missile.movex(scrn[1])

            if missile.pos[1] < -32:
                player_missiles.remove(missile)

        for missile in enemy_missiles:
            missile.movex(scrn[1])

            if missile.pos[1] > scrn[0][1]:
                enemy_missiles.remove(missile)

        for deb in debris:
            deb.keep(scrn[1])

            if deb.pos[1] > scrn[0][1]:
                debris.remove(deb)

        for box in boxes:
            box.movex(scrn[1])

            if is_collision(box, player, 40):
                is_upgraded = box.open(player, is_upgraded, obj_icons[7:9][1])
                box.sound.play()
                boxes.remove(box)

        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(scrn[0], obj_icons[:7][6], 2500))
            enemies[-1].boss()
            number_of_enemies += 1

        for explosion in explosions:
            if pygame.time.get_ticks() - explosion.time0 < 200:
                scrn[1].blit(explosion.icon, (explosion.pos))
            else:
                explosions.remove(explosion)

        if random.randint(0, 70) == 42:
            asteroids.append(Object([random.choice(obj_icons[12])], \
                [random.randint(5, scrn[0][0] - 50), -30], 0.5, 0))
            asteroids[-1].state = True

        for asteroid in asteroids:
            asteroid.movex(scrn[1])

            if asteroid.pos[1] > scrn[0][1]:
                asteroids.remove(asteroid)

        objects = explosions + boxes + player_missiles
        mixer.music.set_volume(vol)

        for obj in objects:
            if obj.sound:
                obj.sound.set_volume(vol)

        score.draw(scrn[1], [10, 10])
        hitpoints.value = player.hitpoints
        hitpoints.draw(scrn[1], [10, 30])

        pygame.display.update()
