"""Pause"""

import pygame
from text import Text

def pause(screen, score, hitpoints):
    """Pause"""
    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"

    score.draw(screen, 10, 10)
    hitpoints.draw(screen, 10, 30)
    pause_txt.draw_text(screen, 250, 200)
    pygame.display.update()
    pause_status = True

    while pause_status:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
            if _event.type == pygame.KEYDOWN:
                if _event.key == pygame.K_p:
                    pause_status = False
