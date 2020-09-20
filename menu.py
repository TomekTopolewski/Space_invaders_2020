"""File for intro function"""

import random
import pygame

from pygame import mixer
from text import Text
from objects import Object
from toolbox import load_img, load_sound, load_music
from button import Button
from button_img import ButtonImg

def menus(state, display):
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

    about = Button([0, 0], "About", 36, (125, 125, 125), load_sound('data/sound/button.wav'))

    quits = Button([0, 0], "Quit", 36, (125, 125, 125), load_sound('data/sound/button.wav'))

    gears = ButtonImg([0, 0], load_img('data/icons/gears_001.png'), \
        load_sound('data/sound/package.wav'))

    volume_up = ButtonImg([0, 0], load_img('data/icons/speaker_001.png'), \
        load_sound('data/sound/package.wav'))

    volume_down = ButtonImg([0, 0], load_img('data/icons/speaker_002.png'), \
        load_sound('data/sound/package.wav'))

    volume_off = ButtonImg([0, 0], load_img('data/icons/speaker_003.png'), \
        load_sound('data/sound/package.wav'))

    controls = ButtonImg([0, 0], load_img('data/icons/controls_001.png'), \
        load_sound('data/sound/package.wav'))

    main_opt = [play, about, quits]
    opt = [volume_up, volume_down, volume_off, controls]

    pygame.display.update()

    pygame.mixer.pre_init(0, 0, 16, 0)
    if load_music('data/sound/background.wav') is not False:
        mixer.music.set_volume(0.50)
        mixer.music.play(-1)

    choose = [False] * 4

    while state:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Read keyboard
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                state = False
                pygame.quit()
                quit()

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
            # Move
            comets_x[i].movexy(display[1])

            # Check screen leave
            if comets_x[i].pos[1] > display[0][1]:
                comets_x.pop(i)

        # Loop through comets y
        for i, _ in enumerate(comets_y):
            # Move
            comets_y[i].movexy(display[1])

            # Check screen leave
            if comets_y[i].pos[1] > display[0][1]:
                comets_y.pop(i)

        title.draw_center(display[1], 5)

        # Loop through options buttons and display them
        pos_y = 10

        gears.pos[0] = display[0][0] - gears.img.get_width() - 10
        gears.pos[1] = pos_y
        gears.draw(display[1])
        gears.action(mouse, click)
        pos_y += 50

        if gears.state:
            for i, _ in enumerate(opt):
                opt[i].pos[0] = display[0][0] - opt[i].img.get_width() - 10
                opt[i].pos[1] = pos_y
                opt[i].draw(display[1])
                opt[i].action(mouse, click)
                pos_y += 50

        if controls.state:
            pos[1] = 200
            for i, j in enumerate(options_txt):
                line = norm_font.font.render(j.strip(), True, norm_font.color)
                display[1].blit(line, (pos))
                pos[1] += 30

                if i == len(options_txt) - 1:
                    pos[1] = 200

        # Loop through menu buttons and display them
        pos_y = display[0][1] - 150

        for i, _ in enumerate(main_opt):
            main_opt[i].render()
            main_opt[i].pos[0] = display[0][0] - main_opt[i].line.get_width() - 15
            main_opt[i].pos[1] = pos_y
            main_opt[i].draw(display[1])
            choose = main_opt[i].action_menu(mouse, click, choose, i)
            pos_y += 50

        if choose[0]:
            if play.sound.get_num_channels() == 0:
                play.sound.play()

            state = False

        elif choose[1]:
            if about.sound.get_num_channels() == 0:
                about.sound.play()

            pos[1] = 70
            for i, j in enumerate(about_txt):
                line = norm_font.font.render(j.strip(), True, norm_font.color)
                display[1].blit(line, (pos))
                pos[1] += 30

                if i == len(about_txt) - 1:
                    pos[1] = 70

        elif choose[2]:
            state = False
            pygame.quit()
            quit()

        # Draw custom cursor
        cursor = load_img('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
