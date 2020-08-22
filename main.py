"""Basic game in Python

Based on a great tutorial https://www.youtube.com/watch?v=FfWpgLFMI7w

Icons made by:
Good Ware    -  https://www.flaticon.com/authors/good-ware
Freepik      -  https://www.flaticon.com/authors/freepik
Nhor Phai    -  https://www.flaticon.com/authors/nhor-phai
Ecalyp       -  https://www.flaticon.com/authors/eucalyp
Someone?     -  https://www.flaticon.com/free-icon/aircraft_3116083?term=aircraft&page=2&position=31
Someone?     -  https://www.flaticon.com/free-icon/rocket_3232245?term=spaceship&page=2&position=50
itim2101     -  https://www.flaticon.com/authors/itim2101
smalllikeart -  https://www.flaticon.com/authors/smalllikeart
vectors-market  https://www.flaticon.com/authors/vectors-market
Nikita Golubev  https://www.flaticon.com/authors/nikita-golubev"

Music thanks to www.freesound.org"""

import os
import math
import random
import pygame

from pygame import mixer

def file_path(file_name):
    """File path"""
    main_dir = os.path.split(os.path.abspath(__file__))[0]
    data_dir = os.path.join(main_dir, "data")
    return os.path.join(data_dir, file_name)

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders 2020")
icon = pygame.image.load(file_path('tank-icon.png'))
pygame.display.set_icon(icon)
background = pygame.image.load(file_path('background.png'))
mixer.music.load(file_path('background.wav'))
mixer.music.play(-1)

enemy_skin = []
enemy_skin.append(pygame.image.load(file_path('spaceship.png')))
enemy_skin.append(pygame.image.load(file_path('spaceship2.png')))
enemy_skin.append(pygame.image.load(file_path('spaceship3.png')))
enemy_skin.append(pygame.image.load(file_path('spaceship4.png')))
enemy_skin.append(pygame.image.load(file_path('spaceship5.png')))
enemy_skin.append(pygame.image.load(file_path('spaceship6.png')))
enemy_skin.append(pygame.image.load(file_path('boss.png')))

package_icon = []
package_icon.append(pygame.image.load(file_path('aid-icon.png')))      # 0
package_icon.append(pygame.image.load(file_path('aircraft-icon.png'))) # 1
package_icon.append(pygame.image.load(file_path('reload-icon.png')))   # 2
package_icon.append(pygame.image.load(file_path('speed-icon.png')))    # 3
package_icon.append(pygame.image.load(file_path('splash-icon.png')))   # 4
package_icon.append(pygame.image.load(file_path('thunder-icon.png')))  # 5

class Player(pygame.sprite.Sprite):
    """ Player class"""
    def __init__(self):
        self.icon = pygame.image.load(file_path('tank.png'))
        self.position_x = 370
        self.position_y = 480
        self.position_x_change = 0
        self.position_y_change = 0
        self.agility = 6
        self.health = 3

    def _check_edges(self):
        """Don't let player escape the screen"""
        # Special cases for corners
        if self.position_y >= 536 and self.position_x == 736:
            self.position_x = 736
            self.position_y = 536
        elif self.position_y >= 536 and self.position_x == 0:
            self.position_x = 0
            self.position_y = 536
        elif self.position_y <= 0 and self.position_x == 736:
            self.position_x = 736
            self.position_y = 0
        elif self.position_y <= 0 and self.position_x == 0:
            self.position_x = 0
            self.position_y = 0

        # General rules
        if self.position_x <= 0:
            self.position_x = 0
        elif self.position_x >= 736:
            self.position_x = 736
        elif self.position_y <= 0:
            self.position_y = 0
        elif self.position_y >= 536:
            self.position_y = 536

    def is_collision(self, position_x, position_y):
        """Check if player collide with enemy"""
        distance = math.sqrt(math.pow(position_x - self.position_x, 2) + \
                            (math.pow(position_y - self.position_y, 2)))
        if distance < 35:
            return True
        else:
            return False

    def upgrade(self):
        """Upgrade icon and agility"""
        self.icon = pygame.image.load(file_path('aircraft.png'))
        self.agility = 8
        self.health = 3

    def move(self):
        """Player's move"""
        self.position_x += self.position_x_change
        self.position_y += self.position_y_change
        self._check_edges()

    def draw(self):
        """Draw player's position"""
        screen.blit(self.icon, (self.position_x, self.position_y))

class Missile(pygame.sprite.Sprite):
    """Missile class"""
    def __init__(self):
        self.icon = pygame.image.load(file_path('fire.png'))
        self.sound = mixer.Sound(file_path('shoot.wav'))
        self.position_x = 0
        self.position_y = 0
        self.position_y_change = 10
        self.state = False
        self.range = 45
        self.reload = 0

    def fly(self, position_x, position_y, launch_x, launch_y):
        """Draw missile position"""
        self.state = True
        screen.blit(self.icon, (position_x + launch_x, position_y + launch_y))

    def is_collision(self, position_x, position_y):
        """Check if missile hit the target"""
        distance = math.sqrt(math.pow(position_x - self.position_x, 2) + \
                            (math.pow(position_y - self.position_y, 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False

    def upgrade(self):
        """Changes in weapon"""
        self.sound = mixer.Sound(file_path('shoot2.wav'))
        self.icon = pygame.image.load(file_path('missile.png'))
        self.position_y_change = 13

class Enemy(pygame.sprite.Sprite):
    """Enemy class"""
    def __init__(self):
        self.icon = enemy_skin[0]
        self.position_x = random.randint(25, 700)
        self.position_y = random.randint(5, 10)
        self.position_x_change = 2
        self.position_y_change = 35
        self.step = 0 # Fly y-axis counter used for changes in direction x-direction
        self.step_direction = False # Used for changing direction during advanced move
        self.adv_move_flag = False  # Used for activating advanced movement (y-axis)
        self.health = 1
        self.drop_rate = 2

    def level(self, score_value):
        "Progress mechanism"
        if score_value > 10 and score_value <= 20:
            self.icon = enemy_skin[1]
        elif score_value > 20 and score_value <= 30:
            self.icon = enemy_skin[2]
            self.adv_move_flag = True
        elif score_value > 30 and score_value <= 40:
            self.icon = enemy_skin[3]
            self.adv_move_flag = True
        elif score_value > 40 and score_value <= 50:
            self.icon = enemy_skin[4]
            self.adv_move_flag = True
            self.health = 2
        elif score_value > 50:
            self.icon = enemy_skin[5]
            self.health = 2

    def move(self):
        """Enemy's move"""
        self.position_x += self.position_x_change

        if self.position_x <= 5:
            self.position_x = 6
            self.position_x_change = -self.position_x_change
            self.position_y += self.position_y_change
        elif self.position_x >= 730:
            self.position_x = 729
            self.position_x_change = -self.position_x_change
            self.position_y += self.position_y_change

    def draw(self):
        """Draw enemy's position"""
        screen.blit(self.icon, (self.position_x, self.position_y))

    def advanced_move(self, position_x_change, position_y_change, step):
        """Enemy's advanced move"""
        self.position_x_change = position_x_change
        self.position_y_change = position_y_change

        if self.step == step and self.step_direction is False:
            self.position_x += self.position_x_change
            self.step = 0
            self.step_direction = True
        elif self.step == step and self.step_direction is True:
            self.position_x += -self.position_x_change
            self.step = 0
            self.step_direction = False

        if self.position_x <= 5:
            self.position_x += self.position_x_change # Change direction
            self.step = 0
        elif self.position_x >= 730:
            self.position_x += -self.position_x_change
            self.step = 0

        if random.randint(0, 1) == 1: #Slow them a little
            self.position_y += self.position_y_change

        self.step += 1

    def boss(self):
        """Boss"""
        self.drop_rate = 10
        self.icon = enemy_skin[6]
        self.health = 5
        self.adv_move_flag = True

class Text():
    """Text class"""
    def __init__(self, size, color):
        self.value = 0
        self.text = ""
        self.font = pygame.font.Font(file_path("space_age.ttf"), size)
        self.color = color

    def draw(self, position_x, position_y):
        """Draw text and numbers"""
        score_render = self.font.render(str(self.text) + str(self.value), True, self.color)
        screen.blit(score_render, (position_x, position_y))

    def draw_text(self, position_x, position_y):
        """Draw text"""
        score_render = self.font.render(str(self.text), True, self.color)
        screen.blit(score_render, (position_x, position_y))

class Explosion(pygame.sprite.Sprite):
    """Clas for handling explosions"""
    def __init__(self):
        self.explosion = pygame.image.load(file_path('explosion.png'))
        self.sound = mixer.Sound(file_path('explosion.wav'))
        self.position_x = 0
        self.position_y = 0
        self.last = 0

    def splash(self, position_x, position_y):
        """Draw exlosion splash"""
        self.last = 10
        self.position_x = position_x
        self.position_y = position_y
        screen.blit(self.explosion, (position_x, position_y))

    def splash_last(self, position_x, position_y):
        """Maintain explosion spalsh"""
        if self.last > 0:
            screen.blit(self.explosion, (position_x, position_y))
            self.last -= 1

class Package(pygame.sprite.Sprite):
    """Package class"""
    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        self.position_y_change = 1
        self.state = False
        self.icon = 0
        self.sound = mixer.Sound(file_path('package-sound.wav'))
        self.range = 50
        self.type = 0

    def draw(self, position_x, position_y):
        """Draw package position"""
        if self.type == 'hitpoints':
            self.icon = package_icon[0]
        elif self.type == 'skin':
            self.icon = package_icon[1]
        elif self.type == 'agility':
            self.icon = package_icon[5]
        elif self.type == 'missile_range':
            self.icon = package_icon[4]
        elif self.type == 'missile_speed':
            self.icon = package_icon[3]

        self.position_x = position_x
        self.position_y = position_y
        screen.blit(self.icon, (self.position_x, self.position_y))

    def fly(self):
        "Fly"
        if random.randint(0, 1) == 1: #Slow them a little
            self.position_y += self.position_y_change

        screen.blit(self.icon, (self.position_x, self.position_y))

    def open(self, ship, missile):
        """Modifi values based on package type"""
        if self.type == 'hitpoints':
            ship.health += 1
        elif self.type == 'skin':
            ship.icon = pygame.image.load(file_path('aircraft.png'))
            missile.sound = mixer.Sound(file_path('shoot2.wav'))
            missile.icon = pygame.image.load(file_path('missile.png'))
        elif self.type == 'agility':
            ship.agility += 1
        elif self.type == 'missile_range':
            missile.range += 2
        elif self.type == 'missile_speed':
            missile.position_y_change += 1

    def is_collision(self, position_x, position_y):
        """Check if player pick up a package"""
        distance = math.sqrt(math.pow(position_x - self.position_x, 2) + \
                            (math.pow(position_y - self.position_y, 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False

def intro(state):
    """Intro"""
    txt_file = open(file_path('intro.txt'), 'r')
    from_file = txt_file.readlines()
    text = []

    line_y_position = [10, 50, 50, 150, 150, 200, 250, 250, 350, 350, 400, 450, 550, 550]

    for index in from_file:
        text.append(index.strip()) # Delete new line characters

    intro_font = pygame.font.Font(file_path("BebasNeue-Regular.ttf"), 22)

    for index, _ in enumerate(text):
        render_line = intro_font.render(text[index], True, (255, 255, 255))
        screen.blit(render_line, (20, line_y_position[index]))

    pygame.display.update()
    while state:

        for j in pygame.event.get():
            if j.type == pygame.QUIT:
                state = False
                pygame.quit()
            if j.type == pygame.KEYDOWN:
                if j.key == pygame.K_SPACE:
                    state = False

def main_loop(state):
    """Main loop"""
    pause = False
    game_over_status = False
    pygame.display.update()

    player = Player()
    player_missile = Missile()
    explosion = Explosion()

    score = Text(32, (0, 0, 0))
    score.text = "Score: "

    play_again_txt = Text(32, (0, 0, 0))
    play_again_txt.text = "Press space to play again"

    game_over = Text(72, (47, 79, 79))
    game_over.text = "Game Over!"

    pause_txt = Text(72, (47, 79, 79))
    pause_txt.text = "Pause"

    hitpoints = Text(22, (0, 0, 0))
    hitpoints.text = "HP: "
    hitpoints.value = player.health

    agility = Text(22, (0, 0, 0))
    agility.text = "Agility: "
    agility.value = player.agility

    missile_range_txt = Text(22, (0, 0, 0))
    missile_range_txt.text = "Range: "
    missile_range_txt.value = player_missile.range

    missile_speed_txt = Text(22, (0, 0, 0))
    missile_speed_txt.text = "Speed: "
    missile_speed_txt.value = player_missile.position_y_change

    missile_txt = Text(22, (0, 0, 0))
    missile_txt.text = "Missile"

    player_txt = Text(22, (0, 0, 0))
    player_txt.text = "Player"

    package = []
    enemies = []
    enemy_missile = []
    number_of_enemies = 0

    while number_of_enemies < 5:
        enemies.append(Enemy())
        #enemy_missile.append(Missile())
        number_of_enemies += 1

    # Main while loop
    while state:
        screen.blit(background, (0, 0))

        # Read keyboard
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.position_x_change = -player.agility
                if event.key == pygame.K_RIGHT:
                    player.position_x_change = player.agility
                if event.key == pygame.K_UP:
                    player.position_y_change = -player.agility
                if event.key == pygame.K_DOWN:
                    player.position_y_change = player.agility
                if event.key == pygame.K_SPACE or event.key == pygame.K_LSHIFT:
                    if not player_missile.state: # One missile at a time
                        player_missile.position_x = player.position_x
                        player_missile.position_y = player.position_y
                        player_missile.fly(player_missile.position_x, \
                                            player_missile.position_y, 16, 10)
                        player_missile.sound.play()
                if event.key == pygame.K_p:
                    pause = True
                    pause_txt.draw_text(265, 200)
                    pygame.display.update()
                    while pause:
                        for _event in pygame.event.get():
                            if _event.type == pygame.QUIT:
                                pause = False
                                state = False
                            if _event.type == pygame.KEYDOWN:
                                if _event.key == pygame.K_p:
                                    pause = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                                event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.position_x_change = 0
                    player.position_y_change = 0

        player.move()

        # Fly enemy missile after they launch
        for _i, _ in enumerate(enemy_missile):
            if enemy_missile[_i].state:
                enemy_missile[_i].fly(enemy_missile[_i].position_x, \
                                        enemy_missile[_i].position_y, 0, 0)
                enemy_missile[_i].position_y += enemy_missile[_i].position_y_change

        # Loop through a list of enemies - fly, check player's hit, drop package
        for i, _ in enumerate(enemies):
            if enemies[i].adv_move_flag:
                enemies[i].advanced_move(40, 1, 70)
            else:
                enemies[i].move()

            if player_missile.is_collision(enemies[i].position_x, enemies[i].position_y):
                enemies[i].health -= 1

                if enemies[i].health == 0:
                    score.value += 1
                    player_missile.state = False
                    explosion.sound.play()
                    explosion.splash(player_missile.position_x, player_missile.position_y)

                    if random.randint(0, 20) < enemies[i].drop_rate: #Drop
                        package.append(Package())
                        package[-1].type = random.choice( \
                               ['hitpoints', 'skin', 'agility', 'missile_range', 'missile_speed'])
                        package[-1].draw(enemies[i].position_x, enemies[i].position_y)
                        package[-1].state = True

                    enemies[i] = Enemy()
                    #enemy_missile[i] = Missile()

                    if score.value > 55 and score.value < 60:
                        enemies.append(Enemy())
                        enemies[-1].level(random.randint(0, 50))
                    elif score.value >= 60:
                        enemies[i].level(random.randint(0, 50))
                    else:
                        enemies[i].level(score.value)

                    if score.value > 70 and random.randint(0, 10) == 6:
                        enemies[i].boss()

                else:
                    player_missile.state = False
                    explosion.sound.play()
                    explosion.splash(player_missile.position_x, player_missile.position_y)

            player.draw()

            score.draw(10, 10)
            player_txt.draw_text(10, 50)
            hitpoints.draw(10, 70)
            agility.draw(10, 90)
            missile_txt.draw_text(10, 120)
            missile_range_txt.draw(10, 140)
            missile_speed_txt.draw(10, 160)

            # Enemy leave the screen
            if enemies[i].position_y > 500:
                player.health -= 1
                if player.health >= 1:
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    hitpoints.value = player.health
                    hitpoints.draw(10, 30)
                else:
                    for _i, _ in enumerate(enemies):
                        enemies[_i].position_y = 1000
                    for _i, _ in enumerate(enemy_missile):
                        enemy_missile[_i].state = False
                        enemy_missile[_i].position_y_change = 1000
                    player.position_x = 800
                    player.health = 0
                    hitpoints.value = player.health
                    screen.blit(background, (0, 0))
                    game_over.draw_text(130, 200)
                    score.draw(320, 260)
                    play_again_txt.draw_text(100, 300)
                    pygame.display.update()
                    game_over_status = True

            # Player's collision with enemy
            if player.is_collision(enemies[i].position_x, enemies[i].position_y):
                player.health -= 1

                if player.health >= 1:
                    explosion.sound.play()
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    player.position_x = 0
                    player.position_y = 536
                    hitpoints.value = player.health
                    hitpoints.draw(10, 30)
                else:
                    for _i, _ in enumerate(enemies):
                        enemies[_i].position_y = 1000
                    for _i, _ in enumerate(enemy_missile):
                        enemy_missile[_i].state = False
                        enemy_missile[_i].position_y_change = 1000
                    player.position_x = 800
                    player.health = 0
                    hitpoints.value = player.health
                    screen.blit(background, (0, 0))
                    game_over.draw_text(130, 200)
                    score.draw(320, 260)
                    play_again_txt.draw_text(80, 500)
                    pygame.display.update()
                    game_over_status = True

            enemies[i].draw()

            # Launch enemy missile
            if random.randint(0, 600) == 42:
                #and not enemy_missile[i].state:
                enemy_missile.append(Missile())
                enemy_missile[-1].icon = pygame.image.load(file_path('atomic-bomb.png'))
                enemy_missile[-1].position_y_change = 4
                enemy_missile[-1].position_x = enemies[i].position_x # Take coordinates
                enemy_missile[-1].position_y = enemies[i].position_y
                enemy_missile[-1].fly(enemy_missile[-1].position_x, \
                                    enemy_missile[-1].position_y, -16, -10)

        # Fly the player's missile
        if player_missile.state:
            player_missile.fly(player_missile.position_x, player_missile.position_y, 0, 0)
            player_missile.position_y -= player_missile.position_y_change

        # Fly the package and open
        for _i, _ in enumerate(package):
            if package[_i].state:
                package[_i].fly()

            if package[_i].is_collision(player.position_x, player.position_y):
                package[_i].open(player, player_missile)
                package[_i].sound.play()
                package[_i].state = False

                hitpoints.value = player.health
                agility.value = player.agility
                missile_range_txt.value = player_missile.range
                missile_speed_txt.value = player_missile.position_y_change

        #Enemy missile hit player
        for _i, _ in enumerate(enemy_missile):
            if enemy_missile[_i].is_collision(player.position_x, player.position_y):
                player.health -= 1
                hitpoints.value = player.health
                if player.health > 0:
                    explosion.splash(enemy_missile[_i].position_x, enemy_missile[_i].position_y)
                    explosion.sound.play()
                    enemy_missile[_i].state = False
                elif player.health == 0:
                    explosion.splash(enemy_missile[_i].position_x, enemy_missile[_i].position_y)
                    explosion.sound.play()
                    for _i, _ in enumerate(enemy_missile):
                        enemy_missile[_i].state = False
                        enemy_missile[_i].position_y_change = 1000
                    for _i, _ in enumerate(enemies):
                        enemies[_i].position_y = 1000
                    player.position_x = 800
                    screen.blit(background, (0, 0))
                    game_over.draw_text(130, 200)
                    score.draw(320, 260)
                    play_again_txt.draw_text(80, 500)
                    pygame.display.update()
                    game_over_status = True

        #Enemy missile leave the screen
        for _i, _ in enumerate(enemy_missile):
            if enemy_missile[_i].position_y > 600:
                enemy_missile[_i].state = False

        # Player missile leave the screen
        if player_missile.position_y <= player_missile.reload:
            player_missile.state = False

        #Game over
        while game_over_status:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over_status = False
                    state = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_over_status = False
                        state = False
                        main_loop(True)

        player.draw()
        explosion.splash_last(explosion.position_x, explosion.position_y)
        pygame.display.update() # Update display each time

# Game sequence
intro(True)
main_loop(True)
