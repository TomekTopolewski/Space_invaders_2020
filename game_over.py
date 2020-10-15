"""Game over"""

import sys
import pygame

from text import Text
from button import Button
from toolbox import load_img, button_act

def menu_buttons_def(scrn_param):
    """scrn"""
    again = Button([0, 0], "Main menu", 36)
    end = Button([0, 0], "Quit", 36)
    menu_buttons = [again, end]

    pos = [0, scrn_param[1] - 100]
    for button in menu_buttons:
        button.render()
        button.pos[0] = scrn_param[0] - button.line.get_width() - 15
        button.pos[1] = pos[1]
        pos[1] += 50

    return menu_buttons

def game_over(score, scrn_param, scrn_surf, bkgd_img):
    """score, scrn"""
    clock = pygame.time.Clock()
    cursor = load_img('data/icons/cursor.png')

    title = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    title.text = "Game Over!"

    menu_buttons = menu_buttons_def(scrn_param)

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if button_act(menu_buttons[0], mouse, click):
            return True

        if button_act(menu_buttons[1], mouse, click):
            sys.exit()

        scrn_surf.blit(bkgd_img, (0, 0))
        title.draw_center(scrn_surf, scrn_param, 120)
        score.draw(scrn_surf, [320, 180])

        for button in menu_buttons:
            button.render()
            button.draw(scrn_surf)

        scrn_surf.blit(cursor, mouse)

        pygame.display.update()
