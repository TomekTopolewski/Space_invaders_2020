"""File for package class"""

import random
import pygame

class Package(pygame.sprite.Sprite):
    """
    1. Sound        - sound when the player picks up the box
    2. Package_icon - a list with four different box icons"""

    def __init__(self, sound, icon):
        self.position = [0, 0]
        self.state = False
        self.sound = sound
        self.velocity = 0.5
        self.icon = icon

        self.sound.set_volume(0.20)
        self.type = random.randint(0, 3)

    def open(self, player, is_upgraded, player_icon, player_sound):
        """Modify values based on package type
        1. Player      - object of a player class
        2. Is_upgraded - flag used for determining which missile icon to use
        3. Player_icon - a list with new three icons - center, left, right"""

        if self.type == 0:
            player.hitpoints += 1
        elif self.type == 1:
            player.icon = player_icon
            player.sound = player_sound
            is_upgraded = True
        elif self.type == 3:
            player.velocity += 1
        elif self.type == 2:
            if player.reload_step < 20:
                player.reload_step += 1
        return is_upgraded

    def move(self, screen):
        """Move and draw package
        1. Screen    - the surface where we will draw a package"""

        self.position[1] += self.velocity
        screen.blit(self.icon[self.type], (self.position[0], self.position[1]))
