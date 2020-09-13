"""File for package class"""

import math
import pygame

class Package(pygame.sprite.Sprite):
    """Package class
    1. Sound        - sound when the player picks up the box
    2. Package_icon - a list with four different box icons"""

    def __init__(self, sound, package_icon):
        self.position = [0, 0]
        self.state = False
        self.sound = sound
        self.range = 50
        self.type = 0
        self.velocity = 0.5
        self.icon = {'hitpoints': package_icon[0], 'skin': package_icon[1], \
                    'velocity': package_icon[3], 'gun_reload': package_icon[2]}

        self.sound.set_volume(0.20)

    def open(self, player, is_upgraded, player_icon):
        """Modify values based on package type
        1. Player      - object of a player class
        2. Is_upgraded - flag used for determining which missile icon to use
        3. Player_icon - a list with new three icons - center, left, right"""

        if self.type == 'hitpoints':
            player.hitpoints += 1
        elif self.type == 'skin':
            player.icon = player_icon
            is_upgraded = True
        elif self.type == 'velocity':
            player.velocity += 1
        elif self.type == 'gun_reload':
            if player.reload_step < 20:
                player.reload_step += 1
        return is_upgraded

    def is_collision(self, position_x, position_y):
        """Check if the player picks up a package
        1. PositionX - position on the x-axis where the package collides with an object
        2. PositionY - position on the y-axis where the package collides with an object"""

        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False

    def move(self, screen):
        """Move and draw package
        1. Screen    - the surface where we will draw a package"""

        self.position[1] += self.velocity
        screen.blit(self.icon[self.type], (self.position[0], self.position[1]))
