"""File for package class"""

import math
import pygame

class Package(pygame.sprite.Sprite):
    """Package class"""
    def __init__(self, sound, package_icon):
        self.position = [0, 0]
        self.velocity = 1
        self.state = False
        self.sound = sound
        self.range = 50
        self.type = 0
        self.velocity = 1
        self.icon = {'hitpoints': package_icon[0], 'skin': package_icon[1], \
                    'velocity': package_icon[3], 'gun_reload': package_icon[2]}

    def open(self, player, is_upgraded, player_skin):
        """Modify values based on package type"""
        if self.type == 'hitpoints':
            player.hitpoints += 1
        elif self.type == 'skin':
            player.icon = player_skin
            is_upgraded = True
        elif self.type == 'velocity':
            player.velocity += 1
        elif self.type == 'gun_reload':
            if player.reload_step < 20:
                player.reload_step += 1
        return is_upgraded

    def is_collision(self, position_x, position_y):
        """Check if player pick up a package"""
        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False

    def move(self, screen):
        """Move and draw package"""
        self.position[1] += self.velocity
        screen.blit(self.icon[self.type], (self.position[0], self.position[1]))
