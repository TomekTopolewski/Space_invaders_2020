"""File for intro function"""

import sys
import random
import pygame

from pygame import mixer
from text import Text
from objects import Object
from toolbox import load_img, load_sound, load_music
from button import Button
from button_img import ButtonImg

def intro(display, vol):
    """1. screen - the surface where we will draw objects"""

    clock = pygame.time.Clock()
    comets_x = []
    comets_y = []
    comet_icon = load_img('data/icons/comet_001.png')

    change_bkgd = 0
    bkgd = display[2][0]

    try:
        about_txt = open('data/text/about.txt', 'r').readlines()
    except FileNotFoundError:
        about_txt = ["Can't load text"]

    try:
        options_txt = open('data/text/options.txt', 'r').readlines()
    except FileNotFoundError:
        options_txt = ["Can't load text"]

    pos = [5, 70]
    norm_font = Text(22, (200, 200, 200), "data/fonts/BebasNeue-Regular.ttf")

    title = Text(38, (125, 125, 125), 'data/fonts/space_age.ttf')
    title.text = "Space Invaders 2020"

    play = Button([0, 0], "Play", 36, (125, 125, 125), load_sound('data/sound/button.wav'))

    about = Button([0, 0], "About", 36, (155, 155, 155), False)

    end = Button([0, 0], "Quit", 36, (155, 155, 155), False)

    gears = ButtonImg([0, 0], load_img('data/icons/gears_001.png'), False)

    vol_up = ButtonImg([0, 0], load_img('data/icons/speaker_001.png'), False)

    vol_down = ButtonImg([0, 0], load_img('data/icons/speaker_002.png'), False)

    vol_off = ButtonImg([0, 0], load_img('data/icons/speaker_003.png'), False)

    controls = ButtonImg([0, 0], load_img('data/icons/controls_001.png'), False)

    main_opt = [play, about, end]
    opt = [vol_up, vol_down, vol_off, controls]

    pygame.mixer.pre_init(0, 0, 16, 0)
    if load_music('data/sound/background.wav') is not False:
        mixer.music.play(-1)

    sh_controls = False
    sh_options = False
    sh_about = False

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Read keyboard
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        # Display background
        display[1].blit(bkgd, (0, 0))
        change_bkgd += 1

        # Animate background
        if change_bkgd == 30:
            bkgd = random.choice(display[2])
            change_bkgd = 0

        # Drop comets x
        if random.randint(0, 250) == 42:
            comets_x.append(Object([comet_icon], [827, random.randint(0, 850)], 5, False))
            comets_x[-1].state = True

        # Drop comets y
        if random.randint(0, 250) == 42:
            comets_y.append(Object([comet_icon], [random.randint(0, 800), 0], 5, False))
            comets_y[-1].state = True

        # Loop through comets x
        for i, _ in enumerate(comets_x):
            comets_x[i].movexy(display[1])

            if comets_x[i].pos[1] > display[0][1]:
                comets_x.pop(i)

        # Loop through comets y
        for i, _ in enumerate(comets_y):
            comets_y[i].movexy(display[1])

            if comets_y[i].pos[1] > display[0][1]:
                comets_y.pop(i)

        title.draw_center(display[1], 5)

        # Draw gears button
        pos_y = 10
        gears.pos[0] = display[0][0] - gears.img.get_width() - 10
        gears.pos[1] = pos_y
        gears.draw(display[1])
        pos_y += 50

        if gears.inside(mouse) and click[0] == 1 and not gears.state:
            gears.state = True
            sh_options = not sh_options
        elif click[0] == 0 and gears.state:
            gears.state = False

        # Draw option buttons
        if sh_options:
            for i, _ in enumerate(opt):
                opt[i].pos[0] = display[0][0] - opt[i].img.get_width() - 10
                opt[i].pos[1] = pos_y
                opt[i].draw(display[1])
                pos_y += 50

        if controls.inside(mouse) and click[0] == 1 and not controls.state:
            controls.state = True
            sh_controls = not sh_controls
        elif click[0] == 0 and controls.state:
            controls.state = False

        if sh_controls:
            pos[1] = 200
            for i, j in enumerate(options_txt):
                line = norm_font.font.render(j.strip(), True, norm_font.color)
                display[1].blit(line, (pos))
                pos[1] += 30

                if i == len(options_txt) - 1:
                    pos[1] = 200

        if vol_up.inside(mouse) and click[0] == 1 and not vol_up.state:
            vol_up.state = True
            if vol <= 1.00:
                vol += 0.10
        elif click[0] == 0 and vol_up.state:
            vol_up.state = False

        if vol_down.inside(mouse) and click[0] == 1 and not vol_down.state:
            vol_down.state = True
            if vol > 0:
                vol -= 0.10
        elif click[0] == 0 and vol_down.state:
            vol_down.state = False

        if vol_off.inside(mouse) and click[0] == 1 and not vol_off.state:
            vol_off.state = True
            vol = 0
        elif click[0] == 0 and vol_off.state:
            vol_off.state = False

        # Menu buttons
        pos_y = display[0][1] - 150

        for i, _ in enumerate(main_opt):
            main_opt[i].render()
            main_opt[i].pos[0] = display[0][0] - main_opt[i].line.get_width() - 15
            main_opt[i].pos[1] = pos_y
            main_opt[i].draw(display[1])
            pos_y += 50

        if play.inside(mouse):
            play.color = (255, 255, 255)
            if click[0] == 1:
                if play.sound.get_num_channels() == 0:
                    play.sound.play()
                return vol
        else:
            play.color = (155, 155, 155)

        if end.inside(mouse):
            end.color = (255, 255, 255)
            if click[0] == 1:
                sys.exit()
        else:
            end.color = (155, 155, 155)

        if about.inside(mouse):
            about.color = (255, 255, 255)
            if click[0] == 1 and not about.status:
                about.status = True
                sh_about = not sh_about
            elif click[0] == 0 and about.status:
                about.status = False
        else:
            about.color = (155, 155, 155)

        if sh_about:
            pos[1] = 70
            for i, j in enumerate(about_txt):
                line = norm_font.font.render(j.strip(), True, norm_font.color)
                display[1].blit(line, (pos))
                pos[1] += 30

                if i == len(about_txt) - 1:
                    pos[1] = 70

        # Set sound level
        mixer.music.set_volume(vol)
        play.sound.set_volume(vol)

        # Draw custom cursor
        cursor = load_img('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
