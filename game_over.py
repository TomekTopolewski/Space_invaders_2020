"""Game over"""

import pygame
from text import Text

def game_over(score, screen, screen_params):
    """Game over"""
    try:
        background = [pygame.image.load('data/images/background_001.jpg')]
    except pygame.error:
        background = pygame.Surface((screen_params[0], screen_params[1]))
        background.fill((0, 0, 0))

    game_over_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    game_over_txt.text = "Game Over!"

    play_again_txt = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    play_again_txt.text = "Press space to play again"

    screen.blit(background[0], (0, 0))

    game_over_txt.draw_text(screen, 140, 120)
    score.draw(screen, 300, 180)
    play_again_txt.draw_text(screen, 80, 720)
    pygame.display.update()
    game_over_status = True

    while game_over_status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over_status = False
                    return True
