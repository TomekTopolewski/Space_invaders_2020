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


def add_box(obj, obj_icons, obj_sounds):
    """obj, obj_icons, obj_sounds"""

    btype = random.randint(0, 2)
    box = Object([obj_icons[11][btype]], obj.pos, 0.5, obj_sounds[2])
    box.type = btype
    return box

def obj_collision(objects1, objects2):
    """objects1, objects2, explosions"""
    obj1_return = False
    obj2_return = False

    for obj1 in objects1:
        for obj2 in objects2:
            if is_collision(obj1, obj2, 40):
                obj1.hpoints -= 1
                obj2.hpoints -= 1

                if obj1.hpoints == 0:
                    obj1_return = obj1
                    objects1.remove(obj1)

                if obj2.hpoints == 0:
                    obj2_return = obj2
                    objects2.remove(obj2)

    return obj1_return, obj2_return

def out_of_screen(objects, scrn):
    """objects, scrn"""

    for obj in objects:
        if obj.pos[1] > scrn[0][1] or obj.pos[1] < 0:
            objects.remove(obj)

def text_def():
    """text_def()"""
    score = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    score.text = "Score: "

    hpoints = Text(22, (255, 255, 255), 'data/fonts/space_age.ttf')
    hpoints.text = "HP: "

    return score, hpoints

def game(scrn, obj_icons, obj_sounds, vol):
    """scrn, obj_icons, obj_sounds, vol"""

    clock = pygame.time.Clock()

    score, hpoints = text_def()

    players = list()
    boxes = list()
    enemies = list()
    enemy_missiles = list()
    player_missiles = list()
    explosions = list()
    asteroids = list()

    bkgd = [0, -scrn[0][1]]

    num_of_ene = 5
    players.append(Player(7, 3, obj_icons[7:9][0]))

    while True:
        clock.tick(60)

        bkgd = moving_bkgd(scrn, bkgd)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    vol = pause(scrn, score, hpoints, vol)

        while len(enemies) < num_of_ene:
            enemies.append(Enemy(scrn[0], obj_icons[:7][random.randint(0, 5)], 4000, 2))

        if random.randint(0, 70) == 42:
            asteroids.append((Object([random.choice(obj_icons[12])], \
                [random.randint(5, scrn[0][0] - 50), 0], 0.5, 0)))

        for asteroid in asteroids:
            asteroid.movex(scrn[1])

        players[0].move(scrn)

        players[0].shoot(player_missiles, obj_icons[9][1], obj_sounds[0][0])

        for enemy in enemies:
            enemy.move(scrn[:2])
            enemy.draw_hp(scrn[1])
            enemy.shoot(enemy_missiles, obj_icons[9][2])

            if enemy.pos[1] > scrn[0][1]:
                players[0].hpoints -= 1
                enemies.remove(enemy)

        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(scrn[0], obj_icons[:7][6], 2500 , 5))
            num_of_ene += 1

        for missile in player_missiles:
            missile.movex(scrn[1])

        for missile in enemy_missiles:
            missile.movex(scrn[1])

        _, obj = obj_collision(players, enemies)
        if obj is not False:
            explosions.append(Object(obj_icons[10], obj.pos, False, obj_sounds[1]))
            explosions[-1].sound.play()

        _, obj = obj_collision(players, asteroids)
        if obj is not False:
            explosions.append(Object(obj_icons[10], obj.pos, False, False))

        _, obj = obj_collision(enemies, asteroids)
        if obj is not False:
            explosions.append(Object(obj_icons[10], obj.pos, False, False))

        obj, _ = obj_collision(player_missiles, asteroids)
        if obj is not False:
            explosions.append(Object(obj_icons[10], obj.pos, False, obj_sounds[1]))
            explosions[-1].sound.play()

        obj, _ = obj_collision(player_missiles, enemy_missiles)
        if obj is not False:
            explosions.append(Object(obj_icons[10], obj.pos, False, obj_sounds[1]))
            explosions[-1].sound.play()

        obj1, obj2 = obj_collision(player_missiles, enemies)
        if obj1 is not False:
            explosions.append(Object(obj_icons[10], obj1.pos, False, obj_sounds[1]))
            explosions[-1].sound.play()
        if obj2 is not False:
            score.value += 1
            if random.randint(0, 1) == 1:
                boxes.append(add_box(obj2, obj_icons, obj_sounds))

        obj, _ = obj_collision(enemy_missiles, asteroids)
        if obj is not False:
            explosions.append(Object(obj_icons[10], obj.pos, False, False))

        obj, _ = obj_collision(enemy_missiles, players)
        if obj is not False:
            explosions.append(Object(obj_icons[10], obj.pos, False, obj_sounds[1]))
            explosions[-1].sound.play()

        out_of_screen(asteroids, scrn)
        out_of_screen(player_missiles, scrn)
        out_of_screen(enemy_missiles, scrn)

        for box in boxes:
            box.movex(scrn[1])
            if is_collision(box, players[0], 40):
                box.open(players[0])
                box.sound.play()
                boxes.remove(box)

        if not players:
            return vol, score

        for explosion in explosions:
            if pygame.time.get_ticks() - explosion.time0 < 200:
                scrn[1].blit(explosion.icon, (explosion.pos))
            else:
                explosions.remove(explosion)

        mixer.music.set_volume(vol)
        for obj in explosions + boxes + player_missiles:
            if obj.sound:
                obj.sound.set_volume(vol)

        score.draw(scrn[1], [10, 10])
        hpoints.value = players[0].hpoints
        hpoints.draw(scrn[1], [10, 30])

        pygame.display.update()
