"""File for intro function"""

import random
import pygame

from text import Text
from comet import Comet
from toolbox import load_image

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
    intro_font = Text(22, (218, 218, 218), "data/fonts/BebasNeue-Regular.ttf")

    pygame.display.update()

    while state:
        clock.tick(60)

        # Read keyboard
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                state = False
                pygame.quit()
                quit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    state = False

        display[1].blit(background, (0, 0))
        change_background += 1

        # Animate background
        if change_background == 30:
            background = random.choice(display[2])
            change_background = 0

        # Write text
        for i, j in enumerate(lines):
            render_line = intro_font.font.render(j.strip(), True, intro_font.color)
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

        pygame.display.update()
