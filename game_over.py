"""File for game over function"""

import pygame
from text import Text
from button import Button
from toolbox import load_sound, load_image

def game_over(score, display):
    """Game over window
    1. Score   - number of points the player earned
    2. Display - the surface where we will draw a text"""

    clock = pygame.time.Clock()

    try:
        background = [pygame.image.load('data/images/background_004.jpg')]
    except pygame.error:
        background = pygame.Surface((display[0][0], display[0][1]))
        background.fill((0, 0, 0))

    game_over_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    game_over_txt.text = "Game Over!"

    again_button = Button([0, 0], "Play again", 36, (100, 100, 100), \
        load_sound('data/sound/button.wav'))

    quit_button = Button([0, 0], "Quit", 36, (125, 125, 125), \
        load_sound('data/sound/button.wav'))

    button = [again_button, quit_button]
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

        display[1].blit(background[0], (0, 0))
        game_over_txt.draw_center(display[1], 120)
        score.draw(display[1], [320, 180])

        # Loop through buttons and display them
        position_y = display[0][1] - 100

        for i, _ in enumerate(button):
            button[i].render()
            button[i].position[0] = display[0][0] - button[i].renderb.get_width() - 15
            button[i].position[1] = position_y
            button[i].draw(display[1])
            choose = button[i].action_menu(mouse, click, choose, i)
            position_y += 50

        if choose[0]:
            if again_button.sound.get_num_channels() == 0:
                again_button.sound.play()
            state = False
            return True

        elif choose[1]:
            state = False
            pygame.quit()
            quit()

        # Draw custom cursor
        cursor = load_image('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
