"""File for object class"""

import pygame

class Object(pygame.sprite.Sprite):
    """
    1. Icon     - image of an object
    2. Position - position on the screen
    3. Velocity - move in x and y-axis
    4. Sound    - sound of an object (false if none)"""

    def __init__(self, icon, position, velocity, sound):
        self.position = position
        self.velocity = velocity
        self.state = False
        self.icon = icon
        self.sound = sound
        self.type = 0
        self.last = 0

    def movex(self, screen):
        """Move and draw an object
        1. Screen - the surface where we will draw an object"""

        self.position[1] += self.velocity
        screen.blit(self.icon[0], (self.position[0], self.position[1]))

    def movexy(self, screen):
        """Move and draw an object
         1. Screen - the surface where we will draw an object"""

        self.position[0] -= self.velocity
        self.position[1] += self.velocity
        screen.blit(self.icon[0], (self.position[0], self.position[1]))

    def open(self, player, is_upgraded, player_icon, player_sound):
        """(fox boxes) Modify values based on a object type
        1. Player      - object of a player class
        2. Is_upgraded - flag used for determining which missile icon to use
        3. Player_icon - list with new three icons - center, left, right"""

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

    def keep(self, screen):
        """(for debris) Keep object for four seconds
         1. Screen - the surface where we will draw an object"""

        self.position[1] += self.velocity
        if self.last < 60:
            self.last += 1
            screen.blit(self.icon[0], (self.position[0], self.position[1]))
        elif self.last >= 60 and self.last < 120:
            self.last += 1
            screen.blit(self.icon[1], (self.position[0], self.position[1]))
        elif self.last >= 120 and self.last < 180:
            self.last += 1
            screen.blit(self.icon[2], (self.position[0], self.position[1]))
        elif self.last >= 180:
            self.state = False

    def burst(self, screen, position):
        """(for explosion) Draw on the screen
        1. Screen   - the surface where we will draw an explosion
        2. Position - position on the x and y-axis where the explosion will appear"""

        self.last = 10
        self.state = True
        self.position = position
        screen.blit(self.icon, (self.position[0], self.position[1]))

    def burst_last(self, screen):
        """(for explosion) Keep on the screen
        1. Screen - the surface where we will draw an explosion"""

        if self.last > 0:
            screen.blit(self.icon, (self.position[0], self.position[1]))
            self.last -= 1
        else:
            self.state = False
