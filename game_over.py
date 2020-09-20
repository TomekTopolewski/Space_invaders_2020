"""File for game over function"""

import pygame
from text import Text
from button import Button
from toolbox import load_sound, load_img

def game_over(score, display):
    """1. score - number of points the player earned
    2. display - the surface where we will draw a text"""

    clock = pygame.time.Clock()

    try:
        bkgd = [pygame.image.load('data/images/background_004.jpg')]
    except pygame.error:
        bkgd = pygame.Surface((display[0][0], display[0][1]))
        bkgd.fill((0, 0, 0))

    title = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    title.text = "Game Over!"

    again = Button([0, 0], "Play again", 36, (100, 100, 100), \
        load_sound('data/sound/button.wav'))

    quits = Button([0, 0], "Quit", 36, (125, 125, 125), \
        load_sound('data/sound/button.wav'))

    button = [again, quits]
    choose = [False] * 2

    state = True

    while state:
        clock.tick(60)
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
                pygame.quit()
                quit()

        display[1].blit(bkgd[0], (0, 0))
        title.draw_center(display[1], 120)
        score.draw(display[1], [320, 180])

        # Loop through buttons and display them
        pos_y = display[0][1] - 100

        for i, _ in enumerate(button):
            button[i].render()
            button[i].pos[0] = display[0][0] - button[i].line.get_width() - 15
            button[i].pos[1] = pos_y
            button[i].draw(display[1])
            choose = button[i].action_menu(mouse, click, choose, i)
            pos_y += 50

        if choose[0]:
            if again.sound.get_num_channels() == 0:
                again.sound.play()
            state = False
            return True

        elif choose[1]:
            state = False
            pygame.quit()
            quit()

        # Draw custom cursor
        cursor = load_img('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
