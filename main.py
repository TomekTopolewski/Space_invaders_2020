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

import math
import random
import pygame

from pygame import mixer

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders 2020")
icon = pygame.image.load('data/tank-icon.png')
pygame.display.set_icon(icon)
background = pygame.image.load('data/background.png')
mixer.music.load('data/background.wav')
mixer.music.play(-1)
clock = pygame.time.Clock()

enemy_skin = [pygame.image.load('data/spaceship.png'), \
                pygame.image.load('data/spaceship2.png'), \
                pygame.image.load('data/spaceship3.png'), \
                pygame.image.load('data/spaceship4.png'), \
                pygame.image.load('data/spaceship5.png'), \
                pygame.image.load('data/spaceship6.png'), \
                pygame.image.load('data/boss.png')]

package_icon = [pygame.image.load('data/aid-icon.png'), \
                pygame.image.load('data/aircraft-icon.png'), \
                pygame.image.load('data/reload-icon.png'), \
                pygame.image.load('data/speed-icon.png'), \
                pygame.image.load('data/splash-icon.png'), \
                pygame.image.load('data/thunder-icon.png')]

class Player(pygame.sprite.Sprite):
    """ Player class"""
    def __init__(self):
        self.icon = pygame.image.load('data/tank.png')
        self.position_x = 370
        self.position_y = 480
        self.agility = 6
        self.health = 3

    def is_collision(self, position_x, position_y):
        """Check if player collide with enemy"""
        distance = math.sqrt(math.pow(position_x - self.position_x, 2) + \
                            (math.pow(position_y - self.position_y, 2)))
        if distance < 35:
            return True
        else:
            return False

class Missile(pygame.sprite.Sprite):
    """Missile class"""
    def __init__(self):
        self.icon = pygame.image.load('data/fire.png')
        self.sound = mixer.Sound('data/shoot.wav')
        self.position_x = 0
        self.position_y = 0
        self.position_y_change = 10
        self.state = False
        self.range = 45

    def is_collision(self, position_x, position_y):
        """Check if missile hit the target"""
        distance = math.sqrt(math.pow(position_x - self.position_x, 2) + \
                            (math.pow(position_y - self.position_y, 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False

class Enemy(pygame.sprite.Sprite):
    """Enemy class"""
    def __init__(self):
        self.icon = enemy_skin[0]
        self.position_x = random.randint(25, 700)
        self.position_y = random.randint(5, 10)
        self.position_x_change = 2
        self.position_y_change = 35
        self.step = 0 # Fly y-axis counter used for changes in direction x-direction
        self.step_direction = False
        self.adv_move_flag = False
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
            self.position_x += self.position_x_change
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
        self.font = pygame.font.Font("data/space_age.ttf", size)
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
    """Class for handling explosions"""
    def __init__(self):
        self.explosion = pygame.image.load('data/explosion.png')
        self.sound = mixer.Sound('data/explosion.wav')
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
        self.sound = mixer.Sound('data/package-sound.wav')
        self.range = 50
        self.type = 0
        self.agility = 1

    def update_skin(self):
        """Choose skin"""
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

    def open(self, ship, missile):
        """Modify values based on package type"""
        if self.type == 'hitpoints':
            ship.health += 1
        elif self.type == 'skin':
            ship.icon = pygame.image.load('data/aircraft.png')
            missile.sound = mixer.Sound('data/shoot2.wav')
            missile.icon = pygame.image.load('data/missile.png')
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
    txt_file = open('data/intro.txt', 'r')
    from_file = txt_file.readlines()
    text = []

    line_y_position = [10, 50, 50, 150, 150, 200, 250, 250, 350, 350, 400, 450, 550, 550]

    for index in from_file:
        text.append(index.strip()) # Delete new line characters

    intro_font = pygame.font.Font("data/BebasNeue-Regular.ttf", 22)

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
    clock.tick(25)
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
        number_of_enemies += 1

    while state:
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.KEYDOWN:
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

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.position_x > player.agility:
            player.position_x -= player.agility
        elif keys[pygame.K_RIGHT] and player.position_x < SCREEN_WIDTH - pygame.Surface.get_width(player.icon) - player.agility:
            player.position_x += player.agility
        elif keys[pygame.K_UP] and player.position_y > player.agility:
            player.position_y -= player.agility
        elif keys[pygame.K_DOWN] and player.position_y < SCREEN_HEIGHT - pygame.Surface.get_height(player.icon) - player.agility:
            player.position_y += player.agility
        elif keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            if not player_missile.state:
                player_missile.position_x = player.position_x + 16
                player_missile.position_y = player.position_y + 10
                player_missile.sound.play()
                player_missile.state = True

        # Enemy's move
        for i, _ in enumerate(enemies):
            if enemies[i].adv_move_flag:
                enemies[i].advanced_move(40, 1, 70)
            else:
                enemies[i].move()

        # Check player's missile hit
        for i, _ in enumerate(enemies):
            if player_missile.is_collision(enemies[i].position_x, enemies[i].position_y):
                enemies[i].health -= 1

                if enemies[i].health == 0:
                    score.value += 1
                    player_missile.state = False
                    explosion.sound.play()
                    explosion.splash(player_missile.position_x, player_missile.position_y)

                    if random.randint(0, 20) <= enemies[i].drop_rate:
                        package.append(Package())
                        package[-1].type = random.choice( \
                               ['hitpoints', 'skin', 'agility', 'missile_range', 'missile_speed'])
                        package[-1].update_skin()
                        package[-1].position_x = enemies[i].position_x
                        package[-1].position_y = enemies[i].position_y
                        package[-1].state = True
                        screen.blit(package[-1].icon, (package[-1].position_x, package[-1].position_y))

                    enemies[i] = Enemy()

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

        # Check if enemy leave the screen
        for i, _ in enumerate(enemies):
            if enemies[i].position_y > 550:
                player.health -= 1
                if player.health >= 1:
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    hitpoints.value = player.health
                else:
                    hitpoints.value = player.health
                    screen.blit(background, (0, 0))
                    game_over.draw_text(130, 200)
                    score.draw(320, 260)
                    play_again_txt.draw_text(100, 300)
                    pygame.display.update()
                    game_over_status = True

        # Player's collision with enemy
        for i, _ in enumerate(enemies):
            if player.is_collision(enemies[i].position_x, enemies[i].position_y):
                player.health -= 1
                if player.health >= 1:
                    explosion.sound.play()
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    player.position_x = 0
                    player.position_y = 536
                    hitpoints.value = player.health
                else:
                    hitpoints.value = player.health
                    screen.blit(background, (0, 0))
                    game_over.draw_text(130, 200)
                    score.draw(320, 260)
                    play_again_txt.draw_text(80, 500)
                    pygame.display.update()
                    game_over_status = True

        # Launch enemy missile
        if random.randint(0, 100) == 42:
            enemy_missile.append(Missile())
            enemy_missile[-1].icon = pygame.image.load('data/atomic-bomb.png')
            enemy_missile[-1].position_y_change = 3
            enemy_missile[-1].position_x = enemies[i].position_x + 32
            enemy_missile[-1].position_y = enemies[i].position_y + 32
            enemy_missile[-1].state = True
            screen.blit(enemy_missile[-1].icon, (enemy_missile[-1].position_x, enemy_missile[-1].position_y))

        # Fly enemy's missile
        for i, _ in enumerate(enemy_missile):
            if enemy_missile[i].state:
                screen.blit(enemy_missile[i].icon, (enemy_missile[i].position_x, enemy_missile[i].position_y))
                enemy_missile[i].position_y += enemy_missile[i].position_y_change

        # Fly the player's missile
        if player_missile.state:
            screen.blit(player_missile.icon, (player_missile.position_x, player_missile.position_y))
            player_missile.position_y -= player_missile.position_y_change

        # Fly the package
        for i, _ in enumerate(package):
            if package[i].state:
                package[i].position_y += package[i].agility
                screen.blit(package[i].icon, (package[i].position_x, package[i].position_y))

        # Open package
        for i, _ in enumerate(package):
            if package[i].is_collision(player.position_x, player.position_y):
                package[i].open(player, player_missile)
                package[i].sound.play()
                package[i].state = False
                hitpoints.value = player.health
                agility.value = player.agility
                missile_range_txt.value = player_missile.range
                missile_speed_txt.value = player_missile.position_y_change

        # Enemy missile hit player
        for i, _ in enumerate(enemy_missile):
            if enemy_missile[i].is_collision(player.position_x, player.position_y):
                player.health -= 1
                hitpoints.value = player.health
                if player.health > 0:
                    explosion.splash(enemy_missile[i].position_x, enemy_missile[i].position_y)
                    explosion.sound.play()
                    enemy_missile[i].state = False
                elif player.health == 0:
                    explosion.splash(enemy_missile[i].position_x, enemy_missile[i].position_y)
                    explosion.sound.play()
                    screen.blit(background, (0, 0))
                    game_over.draw_text(130, 200)
                    score.draw(320, 260)
                    play_again_txt.draw_text(80, 500)
                    pygame.display.update()
                    game_over_status = True

        #Enemy missile leave the screen
        for i, _ in enumerate(enemy_missile):
            if enemy_missile[i].position_y > SCREEN_HEIGHT:
                enemy_missile[i].state = False

        # Player missile leave the screen
        if player_missile.position_y < 0:
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

        score.draw(10, 10)
        player_txt.draw_text(10, 50)
        hitpoints.draw(10, 70)
        agility.draw(10, 90)
        missile_txt.draw_text(10, 120)
        missile_range_txt.draw(10, 140)
        missile_speed_txt.draw(10, 160)

        screen.blit(player.icon, (player.position_x, player.position_y))

        for i, _ in enumerate(enemies):
            screen.blit(enemies[i].icon, (enemies[i].position_x, enemies[i]. position_y))

        explosion.splash_last(explosion.position_x, explosion.position_y)
        pygame.display.update()

# Game sequence
intro(True)
main_loop(True)
