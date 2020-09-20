"""File for pause function"""

import pygame
from text import Text
from button import Button
from toolbox import load_sound, load_img

def pause(display, score, hitpoints):
    """1. display - the surface where we will draw objects
    2. score - number of points the player earned
    3. hitpoints - number of hitpoints the player has"""

    clock = pygame.time.Clock()

    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    returns = Button([0, 0], "Return", 36, (100, 100, 100), \
    load_sound('data/sound/button.wav'))

    play = Button([0, 0], "New game", 36, (100, 100, 100), \
    load_sound('data/sound/button.wav'))

    quits = Button([0, 0], "Quit", 36, (100, 100, 100), \
        load_sound('data/sound/button.wav'))

    button = [returns, play, quits]
    choose = [False] * 3
    state = True

    while state:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        display[1].blit(display[2][0], (0, 0))

        score.draw(display[1], [10, 10])
        hitpoints.draw(display[1], [10, 30])
        pause_txt.draw_text(display[1], [270, 200])

        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                state = False
                pygame.quit()
                quit()

        # Loop through buttons and display them
        pos_y = display[0][1] - 150

        for i, _ in enumerate(button):
            button[i].render()
            button[i].pos[0] = display[0][0] - button[i].line.get_width() - 15
            button[i].pos[1] = pos_y
            button[i].draw(display[1])
            choose = button[i].action_menu(mouse, click, choose, i)
            pos_y += 50

        if choose[0]:
            if play.sound.get_num_channels() == 0:
                play.sound.play()
            state = False

        if choose[1]:
            if play.sound.get_num_channels() == 0:
                play.sound.play()
            state = False
            return True

        elif choose[2]:
            state = False
            pygame.quit()
            quit()

        # Draw custom cursor
        cursor = load_img('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
