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

if not pygame.mixer:
    print("Pygame mixer module not available")

class NoneSound:
    """Empty sound"""
    def play(self):
        """Play"""

def load(filename):
    "Loading files"
    if 'png' in filename or 'bmp' in filename or 'jpg' in filename:
        try:
            image = pygame.image.load(filename)
        except pygame.error:
            default = pygame.Surface((64, 64))
            pygame.draw.rect(default, \
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), \
                (0, 0, 64, 64))
            image = default
        return image
    elif 'wav' in filename or 'mp3' in filename:
        try:
            sound = mixer.Sound(filename)
        except FileNotFoundError:
            sound = NoneSound()
        return sound

pygame.init()
screen_params = (800, 600)
screen = pygame.display.set_mode((screen_params[0], screen_params[1]))
pygame.display.set_caption("Space Invaders 2020")
window_icon = load('data/tank-icon.png')
pygame.display.set_icon(window_icon)
clock = pygame.time.Clock()

try:
    background = pygame.image.load('data/background.png')
except pygame.error:
    background = pygame.Surface((screen_params[0], screen_params[1]))
    background.fill((0, 0, 0))

try:
    background_sound = mixer.music.load('data/background.wav')
except pygame.error:
    background_sound = False

if background_sound != False:
    mixer.music.play(-1)

enemy_skin = [load('data/spaceship.png'), \
                load('data/spaceship2.png'), \
                load('data/spaceship3.png'), \
                load('data/spaceship4.png'), \
                load('data/spaceship5.png'), \
                load('data/spaceship6.png'), \
                load('data/boss.png')]

package_icon = [load('data/aid-icon.png'), \
                load('data/aircraft-icon.png'), \
                load('data/reload-icon.png'), \
                load('data/thunder-icon.png')]

class Player(pygame.sprite.Sprite):
    """ Player class"""
    def __init__(self, icon, velocity, hitpoints):
        self.icon = icon
        self.position = [370, 480]
        self.velocity = velocity
        self.hitpoints = hitpoints

    def is_collision(self, position_x, position_y):
        """Check if player collide with enemy"""
        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < 35:
            return True
        else:
            return False

    def move(self):
        """Move"""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and self.position[0] > self.velocity:
            self.position[0] -= self.velocity
        elif keys[pygame.K_RIGHT] and self.position[0] < screen_params[0] - \
                                        pygame.Surface.get_width(self.icon) - self.velocity:
            self.position[0] += self.velocity
        elif keys[pygame.K_UP] and self.position[1] > self.velocity:
            self.position[1] -= self.velocity
        elif keys[pygame.K_DOWN] and self.position[1] < screen_params[1] - \
                                        pygame.Surface.get_height(self.icon) - self.velocity:
            self.position[1] += self.velocity

        screen.blit(self.icon, (self.position[0], self.position[1]))

    def shoot(self, player_missile, gun, is_upgraded):
        "Shoot"
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            if not gun.is_reloading:
                if is_upgraded:
                    player_missile.append(Missile(load('data/missile.png'), \
                                        load('data/shoot2.wav'), -10))
                else:
                    player_missile.append(Missile(load('data/fire.png'), \
                                        load('data/shoot.wav'), -10))

                launch_x = (pygame.Surface.get_width(self.icon) / 2) - \
                                        (pygame.Surface.get_width(player_missile[-1].icon) / 2)
                launch_y = (pygame.Surface.get_height(self.icon) / 2) - \
                                        (pygame.Surface.get_height(player_missile[-1].icon) / 2)

                player_missile[-1].position[0] = self.position[0] + launch_x
                player_missile[-1].position[1] = self.position[1] - launch_y
                player_missile[-1].sound.play()
                player_missile[-1].state = True
                gun.is_reloading = True

class Missile(pygame.sprite.Sprite):
    """Missile class"""
    def __init__(self, icon, sound, velocity):
        self.icon = icon
        self.sound = sound
        self.position = [0, 0]
        self.velocity = velocity
        self.state = False
        self.range = 40

    def is_collision(self, position_x, position_y):
        """Check if missile hit the target"""
        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False

    def move(self):
        """Move"""
        if self.state:
            screen.blit(self.icon, (int(self.position[0]), int(self.position[1])))
            self.position[1] += self.velocity

class Gun(pygame.sprite.Sprite):
    """Gun class"""
    def __init__(self):
        self.reload_step = 40
        self.reload_time = 0
        self.is_reloading = False

class Enemy(pygame.sprite.Sprite):
    """Enemy class"""
    def __init__(self):
        self.icon = enemy_skin[0]
        self.position = [random.randint(5, 730), random.randint(5, 10)]
        self.velocity = 2
        self.step = 0 # Fly y-axis counter used for changes in x-direction
        self.step_direction = False
        self.adv_move_flag = False
        self.hitpoints = 1
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
            self.hitpoints = 2
        elif score_value > 50:
            self.icon = enemy_skin[5]
            self.hitpoints = 2

    def move(self):
        """Enemy's move"""
        self.position[0] += self.velocity

        if self.position[0] <= 0:
            self.velocity = -self.velocity
            self.position[1] += self.velocity * 15
        elif self.position[0] >= screen_params[0] - pygame.Surface.get_width(self.icon):
            self.velocity = -self.velocity
            self.position[1] += -self.velocity * 15

    def advanced_move(self, velocity, step):
        """Enemy's advanced move"""
        self.velocity = velocity
        agility = 50

        if self.step == step and self.step_direction is False:
            self.position[0] += self.velocity * agility
            self.step = 0
            self.step_direction = True
        elif self.step == step and self.step_direction is True:
            self.position[0] += -self.velocity * agility
            self.step = 0
            self.step_direction = False

        if self.position[0] <= 0:
            self.position[0] += self.velocity * agility
            self.step = 0
        elif self.position[0] >= screen_params[0] - pygame.Surface.get_width(self.icon):
            self.position[0] -= self.velocity * agility
            self.step = 0

        if random.randint(0, 1) == 1: #Slow them a little
            self.position[1] += self.velocity

        self.step += 1

    def boss(self):
        """Boss"""
        self.drop_rate = 10
        self.icon = enemy_skin[6]
        self.hitpoints = 5
        self.adv_move_flag = True

    def shoot(self, enemy_missile):
        """Shoot"""
        if random.randint(0, 350) == 42:
            enemy_missile.append(Missile(load('data/atomic-bomb.png'), 0, 3,))

            launch_x = (pygame.Surface.get_width(self.icon) / 2) - \
                                        (pygame.Surface.get_width(enemy_missile[-1].icon) / 2)

            launch_y = (pygame.Surface.get_height(self.icon) / 2) - \
                                        (pygame.Surface.get_height(enemy_missile[-1].icon) / 2)

            enemy_missile[-1].position[0] = self.position[0] + launch_x
            enemy_missile[-1].position[1] = self.position[1] + launch_y
            enemy_missile[-1].state = True
            screen.blit(enemy_missile[-1].icon,\
                    (int(enemy_missile[-1].position[0]), int(enemy_missile[-1].position[1])))

class Text():
    """Text class"""
    def __init__(self, size, color, font_path):
        self.value = 0
        self.text = ""
        try:
            self.font = pygame.font.Font(font_path, size)
        except FileNotFoundError:
            self.font = pygame.font.Font(None, size)
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
        self.icon = load('data/explosion.png')
        self.sound = load('data/explosion.wav')
        self.position = [0, 0]
        self.last = 0

    def splash(self, position_x, position_y):
        """Draw exlosion splash"""
        self.last = 10
        self.position[0] = position_x
        self.position[1] = position_y
        screen.blit(self.icon, (int(position_x), int(position_y)))

    def splash_last(self, position_x, position_y):
        """Maintain explosion spalsh"""
        if self.last > 0:
            screen.blit(self.icon, (int(position_x), int(position_y)))
            self.last -= 1

class Package(pygame.sprite.Sprite):
    """Package class"""
    def __init__(self):
        self.position = [0, 0]
        self.velocity = 1
        self.state = False
        self.icon = 0
        self.sound = load('data/package-sound.wav')
        self.range = 50
        self.type = 0
        self.velocity = 1

    def update_skin(self):
        """Choose skin"""
        if self.type == 'hitpoints':
            self.icon = package_icon[0]
        elif self.type == 'skin':
            self.icon = package_icon[1]
        elif self.type == 'velocity':
            self.icon = package_icon[3]
        elif self.type == 'gun_reload':
            self.icon = package_icon[2]

    def open(self, ship, gun, is_upgraded):
        """Modify values based on package type"""
        if self.type == 'hitpoints':
            ship.hitpoints += 1
        elif self.type == 'skin':
            ship.icon = load('data/aircraft.png')
            is_upgraded = True
        elif self.type == 'velocity':
            ship.velocity += 1
        elif self.type == 'gun_reload':
            gun.reload_step += 5
        return is_upgraded

    def is_collision(self, position_x, position_y):
        """Check if player pick up a package"""
        distance = math.sqrt(math.pow(position_x - self.position[0], 2) + \
                            (math.pow(position_y - self.position[1], 2)))
        if distance < self.range and self.state:
            return True
        else:
            return False

    def move(self):
        """Move and draw package"""
        self.position[1] += self.velocity
        screen.blit(self.icon, (self.position[0], self.position[1]))

def intro(state):
    """Intro"""
    try:
        txt_file = open('data/intro.txt', 'r')
        from_file = txt_file.readlines()
    except FileNotFoundError:
        from_file = ["Can't load intro, press space to play anyway"]
    text = []

    line_y_position = [10, 50, 50, 150, 150, 200, 250, 250, 350, 350, 400, 450, 550, 550]

    for index in from_file:
        text.append(index.strip()) # Delete new line characters

    intro_txt = Text(22, (255, 255, 255), "data/BebasNeue-Regular.ttf")

    for index, _ in enumerate(text):
        render_line = intro_txt.font.render(text[index], True, intro_txt.color)
        screen.blit(render_line, (20, line_y_position[index]))

    pygame.display.update()
    while state:

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                state = False
                pygame.quit()
            if i.type == pygame.KEYDOWN:
                if i.key == pygame.K_SPACE:
                    state = False

def game_over(score):
    """Game over"""
    game_over_txt = Text(72, (47, 79, 79), 'data/space_age.ttf')
    game_over_txt.text = "Game Over!"

    play_again_txt = Text(32, (0, 0, 0), 'data/space_age.ttf')
    play_again_txt.text = "Press space to play again"

    screen.blit(background, (0, 0))
    game_over_txt.draw_text(130, 200)
    score.draw(320, 260)
    play_again_txt.draw_text(80, 500)
    pygame.display.update()
    game_over_status = True

    while game_over_status:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_over_status = False
                    main_loop(True)

def pause():
    """Pause"""
    pause_txt = Text(72, (47, 79, 79), 'data/space_age.ttf')
    pause_txt.text = "Pause"
    pause_txt.draw_text(265, 200)
    pygame.display.update()
    pause_status = True

    while pause_status:
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
            if _event.type == pygame.KEYDOWN:
                if _event.key == pygame.K_p:
                    pause_status = False

def main_loop(state):
    """Main loop"""
    clock.tick(25)

    player = Player(load('data/tank.png'), 6, 3)
    gun = Gun()
    explosion = Explosion()

    score = Text(32, (0, 0, 0), 'data/space_age.ttf')
    score.text = "Score: "

    hitpoints = Text(22, (0, 0, 0), 'data/space_age.ttf')
    hitpoints.text = "HP: "
    hitpoints.value = player.hitpoints

    package = []
    enemies = []
    enemy_missile = []
    player_missile = []
    number_of_enemies = 0
    is_upgraded = False

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
                    pause()

        # Player's move and shoot
        player.move()
        player.shoot(player_missile, gun, is_upgraded)

        # Enemy's move
        for i, _ in enumerate(enemies):
            if enemies[i].adv_move_flag:
                enemies[i].advanced_move(1, 70)
            else:
                enemies[i].move()
            screen.blit(enemies[i].icon, (enemies[i].position[0], enemies[i].position[1]))

        # Check player's missile hit
        for i, _ in enumerate(enemies):
            hit_point_x = enemies[i].position[0] + (pygame.Surface.get_width(enemies[i].icon) / 2)
            hit_point_y = enemies[i].position[1] + (pygame.Surface.get_height(enemies[i].icon) / 2)

            for _i, _ in enumerate(player_missile):
                if player_missile[_i].is_collision(hit_point_x, hit_point_y) and \
                                                            player_missile[_i].state:
                    enemies[i].hitpoints -= 1
                    if enemies[i].hitpoints == 0:
                        score.value += 1
                        player_missile[_i].state = False
                        explosion.sound.play()
                        explosion.splash(player_missile[_i].position[0], \
                                                            player_missile[_i].position[1])

                        if random.randint(0, 20) <= enemies[i].drop_rate:
                            package.append(Package())
                            package[-1].type = random.choice( \
                                ['hitpoints', 'skin', 'velocity', 'gun_reload'])
                            package[-1].update_skin()
                            package[-1].position[0] = enemies[i].position[0]
                            package[-1].position[1] = enemies[i].position[1]
                            package[-1].state = True
                            screen.blit(package[-1].icon, \
                                (package[-1].position[0], package[-1].position[1]))

                        enemies[i] = Enemy()

                        if score.value > 55 and score.value < 60:
                            enemies.append(Enemy())
                            enemies[-1].level(random.randint(0, 50))
                        elif score.value >= 60:
                            enemies[i].level(random.randint(0, 50))
                        else:
                            enemies[i].level(score.value)

                        if score.value > 65 and random.randint(0, 15) == 1:
                            enemies[i].boss()
                    else:
                        player_missile[_i].state = False
                        explosion.sound.play()
                        explosion.splash(player_missile[_i].position[0], \
                                                    player_missile[_i].position[1])

        # Check if enemy leave the screen
        for i, _ in enumerate(enemies):
            if enemies[i].position[1] > (screen_params[1] - \
                                    (pygame.Surface.get_height(player.icon) / 2)):
                player.hitpoints -= 1

                if player.hitpoints >= 1:
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    game_over(score)

        # Player's collision with enemy
        for i, _ in enumerate(enemies):
            if player.is_collision(enemies[i].position[0], enemies[i].position[1]):
                player.hitpoints -= 1

                if player.hitpoints >= 1:
                    explosion.sound.play()
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    player.position[0] = 0
                    player.position[1] = screen_params[1] - pygame.Surface.get_height(player.icon)
                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    game_over(score)

        # Enemy's shoot
        for i, _ in enumerate(enemies):
            enemies[i].shoot(enemy_missile)

        # Fly enemy's missile
        for i, _ in enumerate(enemy_missile):
            enemy_missile[i].move()

        # Fly the player's missile
        for i, _ in enumerate(player_missile):
            player_missile[i].move()

        # Fly the package
        for i, _ in enumerate(package):
            if package[i].state:
                package[i].move()

        # Open package
        for i, _ in enumerate(package):
            if package[i].is_collision(player.position[0], player.position[1]):
                is_upgraded = package[i].open(player, gun, is_upgraded)
                package[i].sound.play()
                package[i].state = False
                hitpoints.value = player.hitpoints

        # Enemy's missile hit player
        for i, _ in enumerate(enemy_missile):
            if enemy_missile[i].is_collision(player.position[0], player.position[1]):
                player.hitpoints -= 1
                hitpoints.value = player.hitpoints

                if player.hitpoints > 0:
                    explosion.splash(enemy_missile[i].position[0], enemy_missile[i].position[1])
                    explosion.sound.play()
                    enemy_missile[i].state = False
                elif player.hitpoints == 0:
                    explosion.splash(enemy_missile[i].position[0], enemy_missile[i].position[1])
                    explosion.sound.play()
                    game_over(score)

        # Enemy's missile leave the screen
        for i, _ in enumerate(enemy_missile):
            if enemy_missile[i].position[1] > screen_params[1]:
                enemy_missile[i].state = False

        # Player's missile leave the screen
        for i, _ in enumerate(player_missile):
            if player_missile[i].position[1] < -100:
                player_missile[i].state = False

        # Reload
        if gun.is_reloading:
            gun.reload_time += gun.reload_step

            if gun.reload_time >= 1000:
                gun.is_reloading = False
                gun.reload_time = 0

        score.draw(10, 10)
        hitpoints.draw(10, 30)
        explosion.splash_last(explosion.position[0], explosion.position[1])
        pygame.display.update()

intro(True)
main_loop(True)
