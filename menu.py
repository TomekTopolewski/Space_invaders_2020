"""Menu"""

import sys
import pygame

from pygame import mixer
from text import Text
from toolbox import load_img, vol_buttons_def, vol_buttons_act, button_act
from button import Button

def menu_buttons_def(scrn):
    """scrn"""

    play = Button([0, 0], "Play", 36)
    about = Button([0, 0], "About", 36)
    end = Button([0, 0], "Quit", 36)
    opt = Button([0, 0], "Options", 36)
    menu_buttons = [play, about, opt, end]

    pos = [0, scrn[0][1] - 200]
    for button in menu_buttons:
        button.render()
        button.pos[0] = scrn[0][0] - button.line.get_width() - 15
        button.pos[1] = pos[1]
        pos[1] += 50

    return menu_buttons

def sh_text(fname, font, scrn):
    """fname, font, scrn"""
    try:
        txt = open(fname, 'r').readlines()
    except FileNotFoundError:
        txt = ["Can't load text"]

    pos = [5, 70]
    for line in txt:
        line = font.font.render(line.strip(), True, font.color)
        scrn[1].blit(line, (pos))
        pos[1] += 30

def menu(scrn, vol):
    """Menu"""

    clock = pygame.time.Clock()

    cursor = load_img('data/icons/cursor.png')

    font = Text(22, (200, 200, 200), "data/fonts/BebasNeue-Regular.ttf")

    title = Text(38, (125, 125, 125), 'data/fonts/space_age.ttf')
    title.text = "Space Invaders 2020"

    vol_buttons = vol_buttons_def(scrn)
    menu_buttons = menu_buttons_def(scrn)

    sh_txt = [False, False]

    while True:
        clock.tick(60)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        vol = vol_buttons_act(vol_buttons, mouse, click, vol)

        if button_act(menu_buttons[0], mouse, click):
            return vol

        if button_act(menu_buttons[3], mouse, click):
            sys.exit()

        if button_act(menu_buttons[1], mouse, click):
            sh_txt[0] = True
            sh_txt[1] = False

        if button_act(menu_buttons[2], mouse, click):
            sh_txt[1] = True
            sh_txt[0] = False

        mixer.music.set_volume(vol)

        scrn[1].blit(scrn[2], (0, 0))
        title.draw_center(scrn[1], 5)

        for button in menu_buttons:
            button.render()
            button.draw(scrn[1])

        for button in vol_buttons:
            button.draw(scrn[1])

        if sh_txt[0]:
            sh_text('data/text/about.txt', font, scrn)

        if sh_txt[1]:
            sh_text('data/text/options.txt', font, scrn)

        scrn[1].blit(cursor, mouse)

        pygame.display.update()
