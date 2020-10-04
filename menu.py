"""Menu"""

import sys
import pygame

from pygame import mixer
from text import Text
from toolbox import load_img, load_music, vol_buttons_def, vol_buttons_act
from button import Button

def menu(screen, vol):
    """Menu"""

    clock = pygame.time.Clock()

    cursor = load_img('data/icons/cursor.png')

    try:
        about_txt = open('data/text/about.txt', 'r').readlines()
    except FileNotFoundError:
        about_txt = ["Can't load text"]

    try:
        options_txt = open('data/text/options.txt', 'r').readlines()
    except FileNotFoundError:
        options_txt = ["Can't load text"]

    font = Text(22, (200, 200, 200), "data/fonts/BebasNeue-Regular.ttf")

    title = Text(38, (125, 125, 125), 'data/fonts/space_age.ttf')
    title.text = "Space Invaders 2020"

    vol_buttons = vol_buttons_def(screen)

    play = Button([0, 0], "Play", 36)
    about = Button([0, 0], "About", 36)
    end = Button([0, 0], "Quit", 36)
    opt = Button([0, 0], "Options", 36)
    menu_buttons = [play, about, opt, end]

    pos = [0, screen[0][1] - 200]
    for button in menu_buttons:
        button.render()
        button.pos[0] = screen[0][0] - button.line.get_width() - 15
        button.pos[1] = pos[1]
        pos[1] += 50

    pygame.mixer.pre_init(0, 0, 16, 0)
    if load_music('data/sound/background.wav') is not False:
        mixer.music.play(-1)

    sh_controls = False
    sh_about = False

    while True:
        clock.tick(60)

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()

        vol = vol_buttons_act(vol_buttons, mouse, click, vol)

        if play.inside(mouse):
            play.color = (255, 255, 255)
            if click[0] == 1:
                return vol
        else:
            play.color = (155, 155, 155)

        if end.inside(mouse):
            end.color = (255, 255, 255)
            if click[0] == 1:
                sys.exit()
        else:
            end.color = (155, 155, 155)

        if about.inside(mouse):
            about.color = (255, 255, 255)
            if click[0] == 1 and not about.status:
                about.status = True
                sh_about = not sh_about
            elif click[0] == 0 and about.status:
                about.status = False
        else:
            about.color = (155, 155, 155)

        if opt.inside(mouse):
            opt.color = (255, 255, 255)
            if click[0] == 1 and not opt.status:
                opt.status = True
                sh_controls = not sh_controls
            elif click[0] == 0 and opt.status:
                opt.status = False
        else:
            opt.color = (155, 155, 155)

        mixer.music.set_volume(vol)

        screen[1].blit(screen[2], (0, 0))
        title.draw_center(screen[1], 5)

        for button in menu_buttons:
            button.render()
            button.draw(screen[1])

        for button in vol_buttons:
            button.draw(screen[1])

        if sh_about:
            pos = [5, 70]
            for line in about_txt:
                line = font.font.render(line.strip(), True, font.color)
                screen[1].blit(line, (pos))
                pos[1] += 30

        if sh_controls:
            pos = [5, 200]
            for line in options_txt:
                line = font.font.render(line.strip(), True, font.color)
                screen[1].blit(line, (pos))
                pos[1] += 30

        screen[1].blit(cursor, mouse)

        pygame.display.update()
