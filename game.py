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

def add_expl(explosions, obj, obj_icons, obj_sounds):
    """explosions, obj, obj_icons, obj_sounds"""

    explosions.append(Object(obj_icons[10], obj.pos, False, obj_sounds[1]))
    explosions[-1].state = True
    explosions[-1].sound.play()

def ships_coll(ships, objects, explosions, obj_icons, obj_sounds):
    """ships, objects, explosions, obj_icons, obj_sounds"""
    for ship in ships:
        for obj in objects:
            if is_collision(ship, obj, 40):
                add_expl(explosions, obj, obj_icons, obj_sounds)
                ship.hitpoints -= 1
                objects.remove(obj)

def missile_coll(missiles, objects, explosions, obj_icons, obj_sounds):
    """missiles, objects, explosions, obj_icons, obj_sounds"""

    for missile in missiles:
        for obj in objects:
            if is_collision(missile, obj, 40):
                obj.hitpoints -= 1

                add_expl(explosions, missile, obj_icons, obj_sounds)

                if obj.hitpoints == 0:
                    objects.remove(obj)

                missiles.remove(missile)
                break

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

        ships_coll([player], enemies, explosions, obj_icons, obj_sounds)

        ships_coll([player], enemy_missiles, explosions, obj_icons, obj_sounds)

        ships_coll([player], asteroids, explosions, obj_icons, obj_sounds)

        for enemy in enemies:
            for missile in player_missiles:
                if is_collision(enemy, missile, 40):
                    enemy.hitpoints -= 1

                    add_expl(explosions, missile, obj_icons, obj_sounds)

                    if enemy.hitpoints == 0:
                        score.value += 1

                        debris.append(Object(obj_icons[13], enemy.pos, 0.5, False))
                        debris[-1].state = True

                        if random.randint(0, 15) <= enemy.drop:
                            btype = random.randint(0, 3)
                            boxes.append(Object([obj_icons[11][btype]], \
                                enemy.pos, 0.25, obj_sounds[2]))
                            boxes[-1].state = True
                            boxes[-1].type = btype

                        enemies.remove(enemy)
                        player_missiles.remove(missile)
                        break

                    player_missiles.remove(missile)

        ships_coll(enemies, asteroids, explosions, obj_icons, obj_sounds)

        missile_coll(player_missiles, asteroids, explosions, obj_icons, obj_sounds)

        missile_coll(player_missiles, enemy_missiles, explosions, obj_icons, obj_sounds)

        missile_coll(enemy_missiles, asteroids, explosions, obj_icons, obj_sounds)

        for enemy in enemies:
            enemy.move(scrn[:2])
            enemy.draw_hp(scrn[1])
            enemy.shoot(enemy_missiles, obj_icons[9][2])

            if enemy.hitpoints == 0:
                debris.append(Object(obj_icons[13], enemy.pos, 0.5, False))
                debris[-1].state = True
                enemies.remove(enemy)

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

        for explosion in explosions:
            if pygame.time.get_ticks() - explosion.time0 < 200:
                scrn[1].blit(explosion.icon, (explosion.pos))
            else:
                explosions.remove(explosion)

        for asteroid in asteroids:
            asteroid.movex(scrn[1])

            if asteroid.pos[1] > scrn[0][1]:
                asteroids.remove(asteroid)

        if random.randint(0, 70) == 42:
            asteroids.append(Object([random.choice(obj_icons[12])], \
                [random.randint(5, scrn[0][0] - 50), -30], 0.5, 0))
            asteroids[-1].state = True

        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(scrn[0], obj_icons[:7][6], 2500))
            enemies[-1].boss()
            number_of_enemies += 1

        mixer.music.set_volume(vol)
        for obj in explosions + boxes + player_missiles:
            if obj.sound:
                obj.sound.set_volume(vol)

        score.draw(scrn[1], [10, 10])
        hitpoints.value = player.hitpoints
        hitpoints.draw(scrn[1], [10, 30])

        pygame.display.update()
