"""Pause"""

import sys
import pygame

from pygame import mixer
from text import Text
from button import Button
from toolbox import load_img, vol_buttons_def, vol_buttons_act

def pause(screen, score, hitpoints, vol):
    """Pause"""

    clock = pygame.time.Clock()

    cursor = load_img('data/icons/cursor.png')

    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    vol_buttons = vol_buttons_def(screen)

    back = Button([0, 0], "Return", 36)
    end = Button([0, 0], "Quit", 36)
    menu_buttons = [back, end]

    pos = [0, screen[0][1] - 100]
    for button in menu_buttons:
        button.render()
        button.pos[0] = screen[0][0] - button.line.get_width() - 15
        button.pos[1] = pos[1]
        pos[1] += 50

    while True:
        clock.tick(60)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                sys.exit()

        vol = vol_buttons_act(vol_buttons, mouse, click, vol)

        if back.inside(mouse):
            back.color = (255, 255, 255)
            if click[0] == 1:
                return vol
        else:
            back.color = (155, 155, 155)

        if end.inside(mouse):
            end.color = (255, 255, 255)
            if click[0] == 1:
                sys.exit()
        else:
            end.color = (155, 155, 155)

        mixer.music.set_volume(vol)

        screen[1].blit(screen[2], (0, 0))

        score.draw(screen[1], [10, 10])
        hitpoints.draw(screen[1], [10, 30])
        pause_txt.draw_text(screen[1], [270, 200])

        for button in menu_buttons:
            button.render()
            button.draw(screen[1])

        for button in vol_buttons:
            button.draw(screen[1])

        screen[1].blit(cursor, mouse)

        pygame.display.update()
