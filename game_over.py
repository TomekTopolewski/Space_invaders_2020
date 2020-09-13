"""File for game over function"""

import pygame
from text import Text
from button import Button
from toolbox import load_sound

def game_over(score, screen, screen_params):
    """Game over window
    1. Score         - number of points the player earned
    2. Screen        - the surface where we will draw a text
    3. Screen params - a list of two values, window's width and height"""
    clock = pygame.time.Clock()

    try:
        background = [pygame.image.load('data/images/background_001.jpg')]
    except pygame.error:
        background = pygame.Surface((screen_params[0], screen_params[1]))
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

        screen.blit(background[0], (0, 0))
        game_over_txt.draw_center(screen, 120)
        score.draw_center(screen, 180)

        again_button.draw(screen)
        again_button.action(mouse, click)

        if again_button.status:
            state = False
            return True

        pygame.display.update()
