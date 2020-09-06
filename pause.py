"""File for pause function"""

import pygame
from text import Text

def pause(screen, score, hitpoints):
    """Pause
    1. Screen    - the surface where we will draw a text
    2. Score     - number of points the player earned
    3. Hitpoints - number of hitpoints the player has"""

    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    score.draw(screen, 10, 10)
    hitpoints.draw(screen, 10, 30)
    pause_txt.draw_text(screen, 270, 200)
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
