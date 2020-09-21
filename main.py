"""Main"""

import random
import pygame

from pygame import mixer
from player import Player
from enemy import Enemy
from text import Text
from objects import Object

from pause import pause
from toolbox import moving_bkgd, is_collision

if not pygame.mixer:
    print("Pygame mixer module not available")

def main(display, obj_icons, obj_sounds, vol):
    """Main loop"""

    pla_icon = obj_icons[7:9]
    ene_icon = obj_icons[:7]
    mis_icon = obj_icons[9]
    exp_icon = obj_icons[10]
    box_icon = obj_icons[11]
    ast_icon = obj_icons[12]
    deb_icon = obj_icons[13]

    mis_sound = obj_sounds[0]
    exp_sound = obj_sounds[1]
    box_sound = obj_sounds[2]

    clock = pygame.time.Clock()

    player = Player(7, 3, pla_icon[0])

    score = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    score.text = "Score: "

    hitpoints = Text(22, (255, 255, 255), 'data/fonts/space_age.ttf')
    hitpoints.text = "HP: "
    hitpoints.value = player.hitpoints

    box = []
    enemies = []
    ene_missile = []
    pla_missile = []
    explosion = []
    asteroid = []
    debris = []
    number_of_enemies = 0
    is_upgraded = False

    bkgd_one = 0
    bkgd_two = display[2][0].get_height() * -1

    while number_of_enemies < 5:
        enemies.append(Enemy(display[0], ene_icon[0], 4000))
        number_of_enemies += 1

    while True:
        clock.tick(60)

        bkgd_one, bkgd_two = moving_bkgd(display[2][0], display[1], bkgd_one, bkgd_two)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    vol = pause(display, score, hitpoints, vol)

        player.move(display[1], display[0])

        if is_upgraded:
            player.shoot(pla_missile, mis_icon[0], mis_sound[1])
        else:
            player.shoot(pla_missile, mis_icon[1], mis_sound[0])

        for i, _ in enumerate(enemies):
            if is_collision(player, enemies[i], 40):
                player.hitpoints -= 1

                explosion.append(Object(exp_icon, enemies[i].pos, False, exp_sound))
                explosion[-1].state = True
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    return vol, score

                enemies.pop(i)

        for i, _ in enumerate(ene_missile):
            if is_collision(player, ene_missile[i], 40):
                player.hitpoints -= 1

                explosion.append(Object(exp_icon, ene_missile[i].pos, False, exp_sound))
                explosion[-1].state = True
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    return vol, score

                ene_missile.pop(i)

        for i, _ in enumerate(asteroid):
            if is_collision(player, asteroid[i], 40):
                player.hitpoints -= 1

                explosion.append(Object(exp_icon, asteroid[i].pos, False, exp_sound))
                explosion[-1].state = True
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    return vol, score

                asteroid.pop(i)

        for i, _ in enumerate(enemies):
            for j, _ in enumerate(pla_missile):
                if is_collision(enemies[i], pla_missile[j], 40):
                    enemies[i].hitpoints -= 1

                    explosion.append(Object(exp_icon, pla_missile[j].pos, False, exp_sound))
                    explosion[-1].state = True
                    explosion[-1].sound.play()

                    if enemies[i].hitpoints == 0:
                        score.value += 1

                        debris.append(Object(deb_icon, enemies[i].pos, 0.5, False))
                        debris[-1].state = True

                        if random.randint(0, 15) <= enemies[i].drop:
                            ptype = random.randint(0, 3)
                            box.append(Object([box_icon[ptype]], enemies[i].pos, 0.25, box_sound))
                            box[-1].state = True
                            box[-1].type = ptype

                        enemies[i] = Enemy(display[0], ene_icon[0], 4000)
                        enemies[i].level(score.value, ene_icon)
                        pla_missile.pop(j)
                        break

                    pla_missile.pop(j)

        for i, _ in enumerate(enemies):
            for j, _ in enumerate(asteroid):
                if is_collision(enemies[i], asteroid[j], 40):
                    enemies[i].hitpoints -= 1

                    explosion.append(Object(exp_icon, asteroid[j].pos, False, exp_sound))
                    explosion[-1].state = True

                    if enemies[i].hitpoints == 0:
                        debris.append(Object(deb_icon, enemies[i].pos, 0.5, False))
                        debris[-1].state = True

                        enemies[i] = Enemy(display[0], ene_icon[0], 4000)
                        enemies[i].level(score.value, ene_icon)
                        asteroid.pop(j)
                        break

                    asteroid.pop(j)

        for i, _ in enumerate(pla_missile):
            for j, _ in enumerate(asteroid):
                if is_collision(pla_missile[i], asteroid[j], 40):
                    asteroid[j].hitpoints -= 1

                    explosion.append(Object(exp_icon, pla_missile[i].pos, False, exp_sound))
                    explosion[-1].state = True
                    explosion[-1].sound.play()

                    if asteroid[j].hitpoints == 0:
                        asteroid.pop(j)

                    pla_missile.pop(i)
                    break

        for i, _ in enumerate(pla_missile):
            for j, _ in enumerate(ene_missile):
                if is_collision(pla_missile[i], ene_missile[j], 40):
                    ene_missile[j].hitpoints -= 1

                    explosion.append(Object(exp_icon, pla_missile[i].pos, False, exp_sound))
                    explosion[-1].state = True
                    explosion[-1].sound.play()

                    if ene_missile[j].hitpoints == 0:
                        ene_missile.pop(j)

                    pla_missile.pop(i)
                    break

        for i, _ in enumerate(ene_missile):
            for j, _ in enumerate(asteroid):
                if is_collision(ene_missile[i], asteroid[j], 40):
                    asteroid[j].hitpoints -= 1

                    explosion.append(Object(exp_icon, asteroid[j].pos, False, False))
                    explosion[-1].state = True

                    if asteroid[j].hitpoints == 0:
                        asteroid.pop(j)

                    ene_missile.pop(i)
                    break

        for i, _ in enumerate(enemies):
            enemies[i].move(display[:2])
            enemies[i].draw_hp(display[1])
            enemies[i].shoot(ene_missile, mis_icon[2])

            if enemies[i].pos[1] > (display[0][1] - (enemies[i].icon[0].get_height() / 2)):
                player.hitpoints -= 1

                enemies[i] = Enemy(display[0], ene_icon[0], 4000)
                enemies[i].level(score.value, ene_icon)

                if player.hitpoints == 0:
                    return vol, score

        for i, _ in enumerate(pla_missile):
            pla_missile[i].movex(display[1])

            if pla_missile[i].pos[1] < -32:
                pla_missile.pop(i)

        for i, _ in enumerate(ene_missile):
            ene_missile[i].movex(display[1])

            if ene_missile[i].pos[1] > display[0][1]:
                ene_missile.pop(i)

        for i, _ in enumerate(debris):
            debris[i].keep(display[1])

            if debris[i].pos[1] > display[0][1]:
                debris.pop(i)

        for i, _ in enumerate(box):
            box[i].movex(display[1])

            if is_collision(box[i], player, 40):
                is_upgraded = box[i].open(player, is_upgraded, pla_icon[1])
                box[i].sound.play()
                box.pop(i)

        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(display[0], ene_icon[6], 2500))
            enemies[-1].boss()

        for i, _ in enumerate(explosion):
            if pygame.time.get_ticks() - explosion[i].time0 < 200:
                display[1].blit(explosion[i].icon, (explosion[i].pos))
            else:
                explosion.pop(i)

        if random.randint(0, 70) == 42:
            asteroid.append(Object([random.choice(ast_icon)], \
                [random.randint(5, display[0][0] - 50), -30], 0.5, 0))
            asteroid[-1].state = True

        for i, _ in enumerate(asteroid):
            asteroid[i].movex(display[1])

            if asteroid[i].pos[1] > display[0][1]:
                asteroid.pop(i)

        obj = explosion + box + pla_missile
        mixer.music.set_volume(vol)

        for i, _ in enumerate(obj):
            if obj[i].sound:
                obj[i].sound.set_volume(vol)

        score.draw(display[1], [10, 10])
        hitpoints.value = player.hitpoints
        hitpoints.draw(display[1], [10, 30])

        pygame.display.update()
