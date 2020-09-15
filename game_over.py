"""File for game over function"""

import pygame
from text import Text
from button import Button
from toolbox import load_sound, load_image

def game_over(score, display):
    """Game over window
    1. Score         - number of points the player earned
    2. Display       - the surface where we will draw a text"""

    clock = pygame.time.Clock()

    try:
        background = [pygame.image.load('data/images/background_001.jpg')]
    except pygame.error:
        background = pygame.Surface((display[0][0], display[0][1]))
        background.fill((0, 0, 0))

    game_over_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    game_over_txt.text = "Game Over!"

    button_sound = load_sound('data/sound/button.wav')
    again_button = Button([270, 720], "Play again", 36, (100, 100, 100), button_sound)

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
        score.draw(display[1], 320, 180)

        again_button.render()
        again_button.draw(display[1])
        again_button.action(mouse, click)

        if again_button.status:
            state = False
            return True

        # Draw custom cursor
        cursor = load_image('data/icons/cursor.png')
        display[1].blit(cursor, mouse)

        pygame.display.update()
