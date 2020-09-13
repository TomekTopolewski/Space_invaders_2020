"""File for intro function"""

import random
import pygame

from text import Text
from comet import Comet
from toolbox import load_image, load_sound
from button import Button

def intro(state, display):
    """Intro window
    1. Screen - the surface where we will draw a text"""

    clock = pygame.time.Clock()
    comet = []
    comet_icon = load_image('data/icons/comet_001.png')
    comet.append(Comet(comet_icon, [827, random.randint(0, 850)]))

    change_background = 0
    background = display[2][0]

    try:
        lines = open('ReadMe.txt', 'r').readlines()
    except FileNotFoundError:
        lines = ["Can't load intro, press space to play anyway"]

    position = [5, 5]
    normal_font = Text(22, (218, 218, 218), "data/fonts/BebasNeue-Regular.ttf")

    button_sound = load_sound('data/sound/button.wav')
    play_button = Button([680, 700], "Play", 36, (100, 100, 100), button_sound)
    about_button = Button([600, 750], "Credits", 36, (100, 100, 100), button_sound)
    quit_button = Button([700, 800], "Quit", 36, (100, 100, 100), button_sound)

    pygame.display.update()

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

        # Write text
        for i, j in enumerate(lines):
            render_line = normal_font.font.render(j.strip(), True, normal_font.color)
            display[1].blit(render_line, (position[0], position[1]))
            position[1] += 30

            if i == len(lines) - 1:
                position[1] = 5

        # Drop comets
        if random.randint(0, 180) == 42:
            comet.append(Comet(comet_icon, [827, random.randint(0, 850)]))

        # Loop through comets
        for i, _ in enumerate(comet):
            # Move
            comet[i].move(display[1])

            # Check screen leave
            if comet[i].position[1] > display[0][1]:
                comet.pop(i)

        # Buttons
        play_button.draw(display[1])
        play_button.action(mouse, click)

        if play_button.status:
            state = False

        about_button.draw(display[1])
        about_button.action(mouse, click)

        quit_button.draw(display[1])
        quit_button.action(mouse, click)

        if quit_button.status:
            state = False
            pygame.quit()
            quit()

        pygame.display.update()
