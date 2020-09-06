"""File for intro function"""

import pygame
from text import Text

def intro(state, display):
    """Intro window
    1. Screen - the surface where we will draw a text"""

    screen = display[1]

    try:
        lines = open('ReadMe.txt', 'r').readlines()
    except FileNotFoundError:
        lines = ["Can't load intro, press space to play anyway"]

    position = [20, 0]
    intro_font = Text(22, (255, 255, 255), "data/fonts/BebasNeue-Regular.ttf")

    for i in lines:
        render_line = intro_font.font.render(i.strip(), True, intro_font.color)
        screen.blit(render_line, (position[0], position[1]))
        position[1] += 30

    pygame.display.update()
    while state:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                state = False
                pygame.quit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    state = False
