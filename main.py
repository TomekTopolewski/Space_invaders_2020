"""Main"""

import random
import pygame

from player import Player
from enemy import Enemy
from text import Text
from objects import Object

from pause import pause
from game_over import game_over
from toolbox import moving_bkgd, is_collision

if not pygame.mixer:
    print("Pygame mixer module not available")

def main(state, display, obj_icons, obj_sounds):
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

    while state:
        clock.tick(60)

        bkgd_one, bkgd_two = moving_bkgd(display[2][0], display[1], bkgd_one, bkgd_two)

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
            player.shoot(pla_missile, mis_icon[0], mis_sound[1])
        else:
            player.shoot(pla_missile, mis_icon[1], mis_sound[0])

        # Player's collision with environment
        player_envi = enemies + ene_missile + asteroid
        for i, _ in enumerate(player_envi):

            if player_envi[i].state and is_collision(player_envi[i], player, 40):
                player.hitpoints -= 1

                explosion.append(Object(exp_icon, player_envi[i].pos, False, exp_sound))
                explosion[-1].state = True
                explosion[-1].sound.play()

                if player.hitpoints == 0:
                    player.state = False

                player_envi[i].state = False

        # Enemies collision with environment
        enemy_envi = pla_missile + asteroid
        for i, _ in enumerate(enemies):
            for _i, _ in enumerate(enemy_envi):
                if enemy_envi[_i].state and is_collision(enemy_envi[_i], enemies[i], 40):
                    enemies[i].hitpoints -= 1

                    explosion.append(Object(exp_icon, enemy_envi[_i].pos, False, exp_sound))
                    explosion[-1].state = True
                    # Play sound only when enemies are hit by one of the player's missiles
                    if enemy_envi[_i].type == 4:
                        explosion[-1].sound.play()

                    if enemies[i].hitpoints == 0:
                        if enemy_envi[_i].type == 4:
                            score.value += 1
                        enemies[i].state = False

                    enemy_envi[_i].state = False

        # Player's missiles collision with environment
        missile_envi = debris + asteroid + ene_missile
        for i, _ in enumerate(pla_missile):
            for _i, _ in enumerate(missile_envi):
                if missile_envi[_i].state and is_collision(missile_envi[_i], pla_missile[i], 40):
                    missile_envi[_i].hitpoints -= 1

                    exp_x = missile_envi[_i].pos[0] + missile_envi[_i].icon[0].get_width() / 2
                    exp_y = missile_envi[_i].pos[1] + missile_envi[_i].icon[0].get_height() / 2

                    explosion.append(Object(exp_icon, [exp_x, exp_y], False, exp_sound))
                    explosion[-1].state = True
                    explosion[-1].sound.play()

                    if missile_envi[_i].hitpoints == 0:
                        missile_envi[_i].state = False

                    pla_missile[i].state = False

        # Enemies
        for i, _ in enumerate(enemies):
            if not enemies[i].state:
                debris.append(Object(deb_icon, enemies[i].pos, 0.5, False))
                debris[-1].state = True

                if random.randint(0, 15) <= enemies[i].drop:
                    ptype = random.randint(0, 3)
                    box.append(Object([box_icon[ptype]], enemies[i].pos, 0.5, box_sound))
                    box[-1].state = True
                    box[-1].type = ptype

                enemies[i] = Enemy(display[0], ene_icon[0], 4000)
                enemies[i].level(score.value, ene_icon)

            enemies[i].move(display[:2])

            if enemies[i].pos[1] > (display[0][1] - (enemies[i].icon[0].get_height() / 2)):
                player.hitpoints -= 1

                enemies[i] = Enemy(display[0], ene_icon[0], 4000)
                enemies[i].level(score.value, ene_icon)

                if player.hitpoints == 0:
                    player.state = False

            enemies[i].draw_hp(display[1])

            enemies[i].shoot(ene_missile, mis_icon[2])

        # Enemy's missiles
        for i, _ in enumerate(ene_missile):
            if ene_missile[i].state:
                ene_missile[i].movex(display[1])

                if ene_missile[i].pos[1] > display[0][1]:
                    ene_missile[i].state = False

                for _i, _ in enumerate(asteroid):
                    if is_collision(asteroid[_i], ene_missile[i], 40):
                        asteroid[_i].hitpoints -= 1

                        explosion.append(Object(exp_icon, asteroid[_i].pos, False, False))
                        explosion[-1].state = True

                        if asteroid[_i].hitpoints == 0:
                            asteroid[_i].state = False

                        ene_missile[i].state = False

            if not ene_missile[i].state:
                ene_missile.pop(i)

        # Player's missiles
        for i, _ in enumerate(pla_missile):
            if pla_missile[i].state:
                pla_missile[i].movex(display[1])

                if pla_missile[i].pos[1] < -32:
                    pla_missile[i].state = False

            if not pla_missile[i].state:
                pla_missile.pop(i)

        # Debrises
        for i, _ in enumerate(debris):
            if debris[i].state:
                debris[i].keep(display[1])

                if debris[i].pos[1] > display[0][1]:
                    debris[i].state = False

            if not debris[i].state:
                debris.pop(i)

        # Boxes
        for i, _ in enumerate(box):
            box[i].movex(display[1])

            if is_collision(box[i], player, 40):
                is_upgraded = box[i].open(player, is_upgraded, pla_icon[1])
                box[i].sound.play()
                box.pop(i)

        # Spot enemy boss
        if random.randint(0, 3000) == 666:
            enemies.append(Enemy(display[0], ene_icon[6], 2500))
            enemies[-1].boss()

        # Draw explosions
        for i, _ in enumerate(explosion):
            if pygame.time.get_ticks() - explosion[i].time0 < 200:
                display[1].blit(explosion[i].icon, (explosion[i].pos))
            else:
                explosion[i].state = False

            if not explosion[i].state:
                explosion.pop(i)

        # Create asteroids
        if random.randint(0, 70) == 42:
            asteroid.append(Object([random.choice(ast_icon)], \
                [random.randint(5, display[0][0] - 50), -30], 0.5, 0))
            asteroid[-1].state = True

        # Asteroids
        for i, _ in enumerate(asteroid):
            if asteroid[i].state:
                asteroid[i].movex(display[1])

                if asteroid[i].pos[1] > display[0][1]:
                    asteroid[i].state = False

            if not asteroid[i].state:
                asteroid.pop(i)

        # Game over
        if not player.state:
            state = False
            if game_over(score, display):
                return True

        # Set sound level
        obj = explosion + box + pla_missile
        for i, _ in enumerate(obj):
            if obj[i].sound:
                obj[i].sound.set_volume(0.25)

        score.draw(display[1], [10, 10])
        hitpoints.value = player.hitpoints
        hitpoints.draw(display[1], [10, 30])
        pygame.display.update()
