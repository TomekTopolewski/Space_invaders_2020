"""File for intro function"""

import random
import pygame

from pygame import mixer
from text import Text
from object import Object
from toolbox import load_image, load_sound, load_music
from button import Button

def menu(state, display):
    """Intro window
    1. Screen - the surface where we will draw objects"""

    clock = pygame.time.Clock()
    cometx = []
    comety = []
    comet_icon = load_image('data/icons/comet_001.png')

    change_background = 0
    background = display[2][0]

    try:
        about_txt = open('data/text/about.txt', 'r').readlines()
    except FileNotFoundError:
        about_txt = ["Can't load text"]

    try:
        options_txt = open('data/text/options.txt', 'r').readlines()
    except FileNotFoundError:
        options_txt = ["Can't load text"]

    position = [5, 70]
    normal_font = Text(22, (200, 200, 200), "data/fonts/BebasNeue-Regular.ttf")

    title = Text(38, (125, 125, 125), 'data/fonts/space_age.ttf')
    title.text = "Space Invaders 2020"

    play_button = Button([0, 0], "Play", 36, (125, 125, 125), \
        load_sound('data/sound/button.wav'))
    about_button = Button([0, 0], "About", 36, (125, 125, 125), \
        load_sound('data/sound/button.wav'))
    quit_button = Button([0, 0], "Quit", 36, (125, 125, 125), \
        load_sound('data/sound/button.wav'))
    options_button = Button([0, 0], "Options", 36, (125, 125, 125), \
        load_sound('data/sound/button.wav'))

    button = [play_button, options_button, about_button, quit_button]

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
        display[1].blit(background, (0, 0))
        change_background += 1

        # Animate background
        if change_background == 30:
            background = random.choice(display[2])
            change_background = 0

        # Drop comets x
        if random.randint(0, 250) == 42:
            cometx.append(Object([comet_icon], [827, random.randint(0, 850)], 5, False))
            cometx[-1].state = True

        # Drop comets y
        if random.randint(0, 250) == 42:
            comety.append(Object([comet_icon], [random.randint(0, 800), 0], 5, False))
            comety[-1].state = True

        # Loop through comets x
        for i, _ in enumerate(cometx):
            # Move
            cometx[i].movexy(display[1])

            # Check screen leave
            if cometx[i].position[1] > display[0][1]:
                cometx.pop(i)

        # Loop through comets y
        for i, _ in enumerate(comety):
            # Move
            comety[i].movexy(display[1])

            # Check screen leave
            if comety[i].position[1] > display[0][1]:
                comety.pop(i)

        title.draw_center(display[1], 5)

        # Loop through buttons and display them
        position_y = display[0][1] - 200

        for i, _ in enumerate(button):
            button[i].render()
            button[i].position[0] = display[0][0] - button[i].renderb.get_width() - 15
            button[i].position[1] = position_y
            button[i].draw(display[1])
            choose = button[i].action_menu(mouse, click, choose, i)
            position_y += 50

        if choose[0]:
            if play_button.sound.get_num_channels() == 0:
                play_button.sound.play()

            state = False

        elif choose[1]:
            if options_button.sound.get_num_channels() == 0:
                options_button.sound.play()

            for i, j in enumerate(options_txt):
                render_line = normal_font.font.render(j.strip(), True, normal_font.color)
                display[1].blit(render_line, (position[0], position[1]))
                position[1] += 30

                if i == len(options_txt) - 1:
                    position[1] = 70

        elif choose[2]:
            if about_button.sound.get_num_channels() == 0:
                about_button.sound.play()

            for i, j in enumerate(about_txt):
                render_line = normal_font.font.render(j.strip(), True, normal_font.color)
                display[1].blit(render_line, (position[0], position[1]))
                position[1] += 30

                if i == len(about_txt) - 1:
                    position[1] = 70

        elif choose[3]:
            state = False
            pygame.quit()
            quit()

        # Draw custom cursor
        cursor = load_image('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
