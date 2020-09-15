"""File for pause function"""

import pygame
from text import Text

def pause(display, score, hitpoints):
    """Pause window
    1. Display   - the surface where we will draw a text
    2. Score     - number of points the player earned
    3. Hitpoints - number of hitpoints the player has"""

    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    pause_txt2 = Text(36, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt2.text = "Press P to play again"

    display[1].blit(display[2][0], (0, 0))

    score.draw(display[1], 10, 10)
    hitpoints.draw(display[1], 10, 30)
    pause_txt.draw_text(display[1], 270, 200)
    pause_txt2.draw_center(display[1], 270)

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
