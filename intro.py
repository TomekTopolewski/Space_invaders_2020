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
    screen = display

    comet = []
    comet_icon = load_image('data/icons/comet_001.png')
    comet.append(Comet(comet_icon, [827, random.randint(0, 850)]))

    try:
        lines = open('ReadMe.txt', 'r').readlines()
    except FileNotFoundError:
        lines = ["Can't load intro, press space to play anyway"]

    position = [5, 5]
    intro_font = Text(22, (255, 255, 255), "data/fonts/BebasNeue-Regular.ttf")

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

        screen[1].blit(display[2], (0, 0))

        # Write text
        for i, j in enumerate(lines):
            render_line = intro_font.font.render(j.strip(), True, intro_font.color)
            screen[1].blit(render_line, (position[0], position[1]))
            position[1] += 30

            if i == len(lines) - 1:
                position[1] = 5

        # Drop comets
        if random.randint(0, 180) == 42:
            comet.append(Comet(comet_icon, [827, random.randint(0, 850)]))

        # Loop through comets
        for i, _ in enumerate(comet):
            # Move
            comet[i].move(screen[1])

            # Check screen leave
            if comet[i].position[1] > screen[0][1]:
                comet.pop(i)

        pygame.display.update()
