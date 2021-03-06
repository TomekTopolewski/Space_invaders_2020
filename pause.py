"""Pause"""

import sys
import pygame

from pygame import mixer
from text import Text
from button import Button
from toolbox import load_img, vol_buttons_def, vol_buttons_act, button_act

def menu_buttons_def(scrn_param):
    """scrn_param"""
    back = Button([0, 0], "Return", 36)
    end = Button([0, 0], "Quit", 36)
    menu_buttons = [back, end]

    pos = [0, scrn_param[1] - 100]
    for button in menu_buttons:
        button.render()
        button.pos[0] = scrn_param[0] - button.line.get_width() - 15
        button.pos[1] = pos[1]
        pos[1] += 50

    return menu_buttons

def pause(scrn_param, scrn_surf, bkgd_img, score, hpoints, vol):
    """Pause"""
    clock = pygame.time.Clock()
    cursor = load_img('data/icons/cursor.png')

    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    vol_buttons = vol_buttons_def(scrn_param)
    menu_buttons = menu_buttons_def(scrn_param)

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                sys.exit()

        vol = vol_buttons_act(vol_buttons, mouse, click, vol)

        if button_act(menu_buttons[0], mouse, click):
            return vol

        if button_act(menu_buttons[1], mouse, click):
            sys.exit()

        mixer.music.set_volume(vol)

        scrn_surf.blit(bkgd_img, (0, 0))

        score.draw(scrn_surf, [10, 10])
        hpoints.draw(scrn_surf, [10, 30])
        pause_txt.draw_text(scrn_surf, [270, 200])

        for button in menu_buttons:
            button.render()
            button.draw(scrn_surf)

        for button in vol_buttons:
            button.draw(scrn_surf)

        scrn_surf.blit(cursor, mouse)

        pygame.display.update()
