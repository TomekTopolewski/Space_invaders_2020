"""File for pause function"""

import pygame
from text import Text

def pause(screen, background, score, hitpoints):
    """Pause window
    1. Screen    - the surface where we will draw a text
    2. Score     - number of points the player earned
    3. Hitpoints - number of hitpoints the player has"""

    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    pause_txt2 = Text(36, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt2.text = "Press P to play again"

    screen.blit(background, (0, 0))
    score.draw(screen, 10, 10)
    hitpoints.draw(screen, 10, 30)
    pause_txt.draw_text(screen, 270, 200)
    pause_txt2.draw_center(screen, 270)
    pygame.display.update()
    state = True

    while state:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                state = False
                pygame.quit()
                quit()
            if _event.type == pygame.KEYDOWN:
                if _event.key == pygame.K_p:
                    state = False
