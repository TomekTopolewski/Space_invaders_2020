"""File for object class"""

import pygame

class Object(pygame.sprite.Sprite):
    """
    1. Icon     - image of an object (list)
    2. Position - position on the screen (list)
    3. Velocity - move in x and y-axis (int)
    4. Sound    - sound of an object (false if none)"""

    def __init__(self, icon, position, velocity, sound):
        self.position = position
        self.velocity = velocity
        self.state = False
        self.icon = icon
        self.sound = sound
        self.type = 0
        self.hitpoints = 1
        self.time0 = pygame.time.get_ticks()

        if self.sound:
            self.sound.set_volume(0.25)

    def movex(self, screen):
        """Move in x-axis
        1. Screen - surface where we will draw an object"""

        self.position[1] += self.velocity
        screen.blit(self.icon[0], (self.position[0], self.position[1]))

    def movexy(self, screen):
        """Move in x and y-axis
         1. Screen - surface where we will draw an object"""

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
            if player.reload > 500:
                player.reload -= 50
        return is_upgraded

    def keep(self, screen):
        """(for debris) Disappering animation
         1. Screen - surface where we will draw an object"""

        self.position[1] += self.velocity
        time1 = pygame.time.get_ticks()

        if time1 - self.time0 < 100:
            screen.blit(self.icon[0], (self.position[0], self.position[1]))

        elif time1 - self.time0 >= 100 and time1 - self.time0 < 200:
            screen.blit(self.icon[1], (self.position[0], self.position[1]))

        elif time1 - self.time0 >= 200 and time1 - self.time0 < 300:
            screen.blit(self.icon[2], (self.position[0], self.position[1]))

        elif time1 - self.time0 >= 300:
            self.state = False
