"""File for pause function"""

import pygame

from pygame import mixer
from text import Text
from button import Button
from button_img import ButtonImg
from toolbox import load_img

def pause(display, score, hitpoints, vol):
    """1. display - the surface where we will draw objects
    2. score - number of points the player earned
    3. hitpoints - number of hitpoints the player has"""

    clock = pygame.time.Clock()

    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    back = Button([0, 0], "Return", 36, (155, 155, 155), False)

    end = Button([0, 0], "Quit", 36, (155, 155, 155), False)

    gears = ButtonImg([0, 0], load_img('data/icons/gears_001.png'), False)

    vol_up = ButtonImg([0, 0], load_img('data/icons/speaker_001.png'), False)

    vol_down = ButtonImg([0, 0], load_img('data/icons/speaker_002.png'), False)

    vol_off = ButtonImg([0, 0], load_img('data/icons/speaker_003.png'), False)

    opt = [vol_up, vol_down, vol_off]
    button = [back, end]
    sh_options = False

    while True:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        display[1].blit(display[2][0], (0, 0))

        score.draw(display[1], [10, 10])
        hitpoints.draw(display[1], [10, 30])
        pause_txt.draw_text(display[1], [270, 200])

        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Draw buttons
        pos_y = display[0][1] - 100
        for i, _ in enumerate(button):
            button[i].render()
            button[i].pos[0] = display[0][0] - button[i].line.get_width() - 15
            button[i].pos[1] = pos_y
            button[i].draw(display[1])
            pos_y += 50

        if back.inside(mouse):
            back.color = (255, 255, 255)
            if click[0] == 1:
                return vol
        else:
            back.color = (155, 155, 155)

        if end.inside(mouse):
            end.color = (255, 255, 255)
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            end.color = (155, 155, 155)

        # Options buttons
        pos_y = 10
        gears.pos[0] = display[0][0] - gears.img.get_width() - 10
        gears.pos[1] = pos_y
        gears.draw(display[1])
        pos_y += 50

        if gears.inside(mouse) and click[0] == 1 and not gears.state:
            gears.state = True
            sh_options = not sh_options
        elif click[0] == 0 and gears.state:
            gears.state = False

        if sh_options:
            for i, _ in enumerate(opt):
                opt[i].pos[0] = display[0][0] - opt[i].img.get_width() - 10
                opt[i].pos[1] = pos_y
                opt[i].draw(display[1])
                pos_y += 50

        if vol_up.inside(mouse) and click[0] == 1 and not vol_up.state:
            vol_up.state = True
            if vol <= 1.00:
                vol += 0.10
        elif click[0] == 0 and vol_up.state:
            vol_up.state = False

        if vol_down.inside(mouse) and click[0] == 1 and not vol_down.state:
            vol_down.state = True
            if vol > 0:
                vol -= 0.10
        elif click[0] == 0 and vol_down.state:
            vol_down.state = False

        if vol_off.inside(mouse) and click[0] == 1 and not vol_off.state:
            vol_off.state = True
            vol = 0
        elif click[0] == 0 and vol_off.state:
            vol_off.state = False

        # Draw custom cursor
        cursor = load_img('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        # Set sound level
        mixer.music.set_volume(vol)

        pygame.display.update()
