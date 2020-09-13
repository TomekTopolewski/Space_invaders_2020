"""File for intro function"""

import random
import pygame

from pygame import mixer
from text import Text
from comet import Comet
from toolbox import load_image, load_sound, load_music
from button import Button

def intro(state, display):
    """Intro window
    1. Screen - the surface where we will draw a text"""

    clock = pygame.time.Clock()
    cometx = []
    comety = []
    comet_icon = load_image('data/icons/comet_001.png')
    cometx.append(Comet(comet_icon, [827, random.randint(0, 850)]))
    comety.append(Comet(comet_icon, [random.randint(0, 800), 0]))

    change_background = 0
    background = display[2][0]

    try:
        lines = open('ReadMe.txt', 'r').readlines()
    except FileNotFoundError:
        lines = ["Can't load about, press Play to play"]

    position = [5, 70]
    normal_font = Text(22, (200, 200, 200), "data/fonts/BebasNeue-Regular.ttf")

    title = Text(38, (125, 125, 125), 'data/fonts/space_age.ttf')
    title.text = "Space Invaders 2020"

    button_sound = load_sound('data/sound/button.wav')
    playing_sound = False
    play_button = Button([690, 720], "Play", 36, (125, 125, 125), button_sound)
    about_button = Button([650, 770], "About", 36, (125, 125, 125), button_sound)
    quit_button = Button([700, 820], "Quit", 36, (125, 125, 125), button_sound)

    pygame.display.update()

    pygame.mixer.pre_init(0, 0, 16, 0)
    if load_music('data/sound/background.wav') is not False:
        mixer.music.set_volume(0.50)
        mixer.music.play(-1)

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
            cometx.append(Comet(comet_icon, [827, random.randint(0, 850)]))

        # Drop comets y
        if random.randint(0, 250) == 42:
            comety.append(Comet(comet_icon, [random.randint(0, 800), 0]))

        # Loop through comets x
        for i, _ in enumerate(cometx):
            # Move
            cometx[i].move(display[1])

            # Check screen leave
            if cometx[i].position[1] > display[0][1]:
                cometx.pop(i)

        # Loop through comets y
        for i, _ in enumerate(comety):
            # Move
            comety[i].move(display[1])

            # Check screen leave
            if comety[i].position[1] > display[0][1]:
                comety.pop(i)

        # Play button
        play_button.draw(display[1])
        play_button.action(mouse, click)

        if play_button.status:
            play_button.sound.play()
            state = False

        # About button
        about_button.draw(display[1])
        about_button.action(mouse, click)

        if about_button.status:
            if not playing_sound:
                playing_sound = True
                about_button.sound.play()

            for i, j in enumerate(lines):
                render_line = normal_font.font.render(j.strip(), True, normal_font.color)
                display[1].blit(render_line, (position[0], position[1]))
                position[1] += 30

                if i == len(lines) - 1:
                    position[1] = 70
        else:
            title.draw_center(display[1], 5)

        # Quit button
        quit_button.draw(display[1])
        quit_button.action(mouse, click)

        if quit_button.status:
            state = False
            pygame.quit()
            quit()

        # Draw custom cursor
        cursor = load_image('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
