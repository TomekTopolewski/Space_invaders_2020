"""Space Invaders 2020
Based on a great tutorial "Python game development course" by freeCodeCamp.org.
Icons made by smalllikeart from www.flaticon.com
Background made by vectorpouch from www.freepik.com
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

def load_image(filename):
    "Loading images"
    try:
        image = pygame.image.load(filename)
    except pygame.error:
        default = pygame.Surface((64, 64))
        pygame.draw.rect(default, \
                (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), \
                (0, 0, 64, 64))
        image = default
    return image

def load_sound(filename):
    """Loading sounds"""
    try:
        sound = mixer.Sound(filename)
    except FileNotFoundError:
        sound = NoneSound()
    return sound

def load_music(filename):
    """Load background music"""
    try:
        music = mixer.music.load(filename)
    except pygame.error:
        music = False
    return music

pygame.mixer.pre_init(0, 0, 16, 0)
pygame.init()
screen_params = (827, 900)
screen = pygame.display.set_mode((screen_params[0], screen_params[1]))
pygame.display.set_caption("Space Invaders 2020")
window_icon = load_image('data/icons/aircraft-icon.png')
pygame.display.set_icon(window_icon)
clock = pygame.time.Clock()

try:
    background = [pygame.image.load('data/images/background_001.jpg')]
except pygame.error:
    background = pygame.Surface((screen_params[0], screen_params[1]))
    background.fill((0, 0, 0))

if load_music('data/sound/background.wav') is not False:
    mixer.music.play(-1)

enemy_skin = [load_image('data/icons/enemy_001.png'), \
                load_image('data/icons/enemy_002.png'), \
                load_image('data/icons/enemy_003.png'), \
                load_image('data/icons/enemy_004.png'), \
                load_image('data/icons/enemy_005.png'), \
                load_image('data/icons/enemy_006.png'), \
                load_image('data/icons/enemy_007.png')]

package_icon = [load_image('data/icons/box_003.png'), \
                load_image('data/icons/box_004.png'), \
                load_image('data/icons/box_001.png'), \
                load_image('data/icons/box_002.png')]

class Player(pygame.sprite.Sprite):
    """ Player class"""
    def __init__(self, velocity, hitpoints):
        self.icon = [load_image('data/icons/player_001.png'), \
                    load_image('data/icons/player_001-left.png'), \
                    load_image('data/icons/player_001-right.png')]
        self.position = [370, 480]
        self.velocity = velocity
        self.hitpoints = hitpoints
        self.reload_step = 10
        self.reload_time = 0
        self.is_reloading = False

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
        # I'm not proud of it, but it works.
        # I hope that I will find another way to control the player's move.
        if keys[pygame.K_LEFT] and self.position[0] > self.velocity:
            self.position[0] -= self.velocity
            screen.blit(self.icon[1], (self.position[0], self.position[1]))

            if keys[pygame.K_UP] and self.position[1] > self.velocity:
                self.position[1] -= self.velocity

            if keys[pygame.K_DOWN] and self.position[1] < screen_params[1] - \
                                        pygame.Surface.get_height(self.icon[0]) - self.velocity:
                self.position[1] += self.velocity

        elif keys[pygame.K_RIGHT] and self.position[0] < screen_params[0] - \
                                        pygame.Surface.get_width(self.icon[0]) - self.velocity:
            self.position[0] += self.velocity
            screen.blit(self.icon[2], (self.position[0], self.position[1]))

            if keys[pygame.K_UP] and self.position[1] > self.velocity:
                self.position[1] -= self.velocity

            if keys[pygame.K_DOWN] and self.position[1] < screen_params[1] - \
                                        pygame.Surface.get_height(self.icon[0]) - self.velocity:
                self.position[1] += self.velocity

        elif keys[pygame.K_UP] and self.position[1] > self.velocity:
            self.position[1] -= self.velocity
            screen.blit(self.icon[0], (self.position[0], self.position[1]))

        elif keys[pygame.K_DOWN] and self.position[1] < screen_params[1] - \
                                        pygame.Surface.get_height(self.icon[0]) - self.velocity:
            self.position[1] += self.velocity
            screen.blit(self.icon[0], (self.position[0], self.position[1]))
        else:
            screen.blit(self.icon[0], (self.position[0], self.position[1]))

    def shoot(self, player_missile, is_upgraded):
        "Shoot"
        keys = pygame.key.get_pressed()

        if keys[pygame.K_SPACE] or keys[pygame.K_LSHIFT]:
            if not self.is_reloading:
                if is_upgraded:
                    player_missile.append(Missile(load_image('data/icons/missile_001.png'), \
                                        load_sound('data/sound/shoot2.wav'), -10))
                else:
                    player_missile.append(Missile(load_image('data/icons/missile_002.png'), \
                                        load_sound('data/sound/shoot.wav'), -10))

                launch_x = (pygame.Surface.get_width(self.icon[0]) / 2) - \
                                        (pygame.Surface.get_width(player_missile[-1].icon) / 2)
                launch_y = (pygame.Surface.get_height(self.icon[0]) / 2) - \
                                        (pygame.Surface.get_height(player_missile[-1].icon) / 2)

                player_missile[-1].position[0] = self.position[0] + launch_x
                player_missile[-1].position[1] = self.position[1] - launch_y
                player_missile[-1].sound.play()
                player_missile[-1].state = True
                self.is_reloading = True

    def reload(self, time):
        """Reload"""
        self.reload_time += self.reload_step

        if self.reload_time >= time:
            self.is_reloading = False
            self.reload_time = 0

class Missile(pygame.sprite.Sprite):
    """Missile class"""
    def __init__(self, icon, sound, velocity):
        self.icon = icon
        self.sound = sound
        self.position = [0, 0]
        self.velocity = velocity
        self.state = False
        self.range = 45

    def is_collision(self, position_x, position_y):
        """Check if missile hit the target"""
        hit_x = self.position[0] + (pygame.Surface.get_width(self.icon) / 2)

        distance = math.sqrt(math.pow(position_x - hit_x, 2) + \
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

class Enemy(pygame.sprite.Sprite):
    """Enemy class"""
    def __init__(self):
        self.icon = enemy_skin[0]
        self.position = [random.randint(5, screen_params[0]- 100), random.randint(0, 10)]
        self.velocity = 2
        self.step = 0 # Fly y-axis counter used for changes in x-direction
        self.step_direction = False
        self.adv_move_flag = False
        self.hitpoints = 2
        self.drop_rate = 1
        self.cell = pygame.Surface.get_width(self.icon) / self.hitpoints
        self.reload_step = 1
        self.reload_time = 0
        self.is_reloading = False

    def level(self, score_value):
        "Progress mechanism"
        if score_value > 10 and score_value <= 20:
            self.icon = enemy_skin[1]
            self.adv_move_flag = True
        elif score_value > 20 and score_value <= 30:
            self.icon = enemy_skin[2]
            self.adv_move_flag = True
        elif score_value > 30 and score_value <= 40:
            self.icon = enemy_skin[3]
            self.adv_move_flag = True
        elif score_value > 40 and score_value <= 50:
            self.icon = enemy_skin[4]
            self.adv_move_flag = True
        elif score_value > 50 and score_value <= 60:
            self.icon = enemy_skin[5]
            self.adv_move_flag = True
        elif score_value > 60:
            self.icon = enemy_skin[random.randint(0, 5)]
            self.adv_move_flag = True

    def move(self):
        """Enemy's move"""
        self.position[0] += self.velocity

        if self.position[0] <= 0:
            self.velocity = -self.velocity
            self.position[1] += self.velocity * 15
        elif self.position[0] >= screen_params[0] - pygame.Surface.get_width(self.icon):
            self.velocity = -self.velocity
            self.position[1] += -self.velocity * 15

        screen.blit(self.icon, (self.position[0], self.position[1]))

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
        screen.blit(self.icon, (self.position[0], self.position[1]))

    def boss(self):
        """Boss"""
        self.drop_rate = 10
        self.icon = enemy_skin[6]
        self.hitpoints = 5
        self.cell = pygame.Surface.get_width(self.icon) / self.hitpoints
        self.adv_move_flag = True

    def shoot(self, enemy_missile):
        """Shoot"""
        if not self.is_reloading and random.randint(0, 150) == 5:
            self.is_reloading = True
            enemy_missile.append(Missile(load_image('data/icons/missile_003.png'), 0, 3))

            launch_x = (pygame.Surface.get_width(self.icon) / 2) - \
                                        (pygame.Surface.get_width(enemy_missile[-1].icon) / 2)

            launch_y = (pygame.Surface.get_height(self.icon) / 2) - \
                                        (pygame.Surface.get_height(enemy_missile[-1].icon) / 2)

            enemy_missile[-1].position[0] = self.position[0] + launch_x
            enemy_missile[-1].position[1] = self.position[1] + launch_y
            enemy_missile[-1].state = True
            screen.blit(enemy_missile[-1].icon,\
                    (int(enemy_missile[-1].position[0]), int(enemy_missile[-1].position[1])))

    def draw_hp(self):
        """Draw hitpoints bar"""
        surface = pygame.Surface((pygame.Surface.get_width(self.icon), 4))
        pygame.draw.rect(surface, (255, 80, 80), (0, 0, pygame.Surface.get_width(self.icon), 4))
        pygame.draw.rect(surface, (0, 255, 0), (0, 0, int(self.cell * self.hitpoints), 4))
        screen.blit(surface, (self.position[0], self.position[1] - 5))

    def reload(self, time):
        """Reload"""
        self.reload_time += self.reload_step

        if self.reload_time >= time:
            self.is_reloading = False
            self.reload_time = 0

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
        self.icon = load_image('data/icons/explosion.png')
        self.sound = load_sound('data/sound/explosion.wav')
        self.position = [0, 0]
        self.last = 0
        self.state = False

    def splash(self, position_x, position_y):
        """Draw exlosion splash"""
        self.last = 10
        self.state = True
        self.position[0] = position_x
        self.position[1] = position_y
        self.sound.play()
        screen.blit(self.icon, (int(position_x), int(position_y)))

    def splash_last(self, position_x, position_y):
        """Maintain explosion spalsh"""
        if self.last > 0:
            screen.blit(self.icon, (int(position_x), int(position_y)))
            self.last -= 1
        else:
            self.state = False

class Package(pygame.sprite.Sprite):
    """Package class"""
    def __init__(self):
        self.position = [0, 0]
        self.velocity = 1
        self.state = False
        self.icon = 0
        self.sound = load_sound('data/sound/package-sound.wav')
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

    def open(self, player, is_upgraded):
        """Modify values based on package type"""
        if self.type == 'hitpoints':
            player.hitpoints += 1
        elif self.type == 'skin':
            player.icon[0] = load_image('data/icons/player_002.png')
            player.icon[1] = load_image('data/icons/player_002-left.png')
            player.icon[2] = load_image('data/icons/player_002-right.png')
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

    def move(self):
        """Move and draw package"""
        self.position[1] += self.velocity
        screen.blit(self.icon, (self.position[0], self.position[1]))

def intro(state):
    """Intro"""
    try:
        txt_file = open('ReadMe.txt', 'r')
        from_file = txt_file.readlines()
    except FileNotFoundError:
        from_file = ["Can't load intro, press space to play anyway"]
    text = []

    line_y_position = [10, 60, 90, 120, 150, 210, 240, 270, 320]

    for index in from_file:
        text.append(index.strip()) # Delete new line characters

    intro_txt = Text(22, (255, 255, 255), "data/fonts/BebasNeue-Regular.ttf")

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
    game_over_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    game_over_txt.text = "Game Over!"

    play_again_txt = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    play_again_txt.text = "Press space to play again"

    screen.blit(background[0], (0, 0))

    game_over_txt.draw_text(140, 120)
    score.draw(300, 180)
    play_again_txt.draw_text(80, 720)
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
    pause_txt = Text(72, (255, 255, 255), 'data/fonts/space_age.ttf')
    pause_txt.text = "Pause"
    pause_txt.draw_text(250, 200)
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
    clock.tick(23)

    player = Player(7, 3)

    score = Text(32, (255, 255, 255), 'data/fonts/space_age.ttf')
    score.text = "Score: "

    hitpoints = Text(22, (255, 255, 255), 'data/fonts/space_age.ttf')
    hitpoints.text = "HP: "
    hitpoints.value = player.hitpoints

    package = []
    enemies = []
    enemy_missile = []
    player_missile = []
    explosion = []
    number_of_enemies = 0
    is_upgraded = False

    while number_of_enemies < 5:
        enemies.append(Enemy())
        number_of_enemies += 1

    while state:
        screen.blit(background[0], (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                state = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause()

        # Player's move, shoot and reload
        player.move()
        player.shoot(player_missile, is_upgraded)

        if player.is_reloading:
            player.reload(500)

        # Loop through the enemy list and do various tasks
        for i, _ in enumerate(enemies):
            # Move
            if enemies[i].adv_move_flag:
                enemies[i].advanced_move(1, 70)
            else:
                enemies[i].move()

            # Check screen leave
            if enemies[i].position[1] > (screen_params[1] - \
                                    (pygame.Surface.get_height(player.icon[0]) / 2)):
                player.hitpoints -= 1

                if player.hitpoints >= 1:
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    state = False
                    game_over(score)

            # Draw hitpoints bar
            enemies[i].draw_hp()

            # Shoot
            enemies[i].shoot(enemy_missile)

            # Reload the gun
            if enemies[i].is_reloading:
                enemies[i].reload(150)

            # Check collision with the player
            if player.is_collision(enemies[i].position[0], enemies[i].position[1]):
                player.hitpoints -= 1

                if player.hitpoints >= 1:
                    explosion.append(Explosion())
                    explosion[-1].splash(enemies[i].position[0], enemies[i].position[1])
                    enemies[i] = Enemy()
                    enemies[i].level(score.value)
                    player.position[0] = 0
                    player.position[1] = screen_params[1] - \
                                        pygame.Surface.get_height(player.icon[0])
                    hitpoints.value = player.hitpoints
                else:
                    hitpoints.value = player.hitpoints
                    state = False
                    game_over(score)

        # Loop through the enemy's missile list and do various tasks
        for i, _ in enumerate(enemy_missile):
            # Fly
            enemy_missile[i].move()

            # Check screen leave
            if enemy_missile[i].position[1] > screen_params[1]:
                enemy_missile[i].state = False

            # Check the player's ship hit
            hit_x = player.position[0] + (pygame.Surface.get_width(player.icon[0]) / 2)
            hit_y = player.position[1] + (pygame.Surface.get_height(player.icon[0]) / 2)

            if enemy_missile[i].state and enemy_missile[i].is_collision(hit_x, hit_y):
                player.hitpoints -= 1
                hitpoints.value = player.hitpoints

                if player.hitpoints > 0:
                    explosion.append(Explosion())
                    explosion[-1].splash(enemy_missile[i].position[0], enemy_missile[i].position[1])
                    enemy_missile[i].state = False

                elif player.hitpoints == 0:
                    explosion.append(Explosion())
                    explosion[-1].splash(enemy_missile[i].position[0], enemy_missile[i].position[1])
                    state = False
                    game_over(score)

            # Remove unnecessary objects
            if not enemy_missile[i].state:
                enemy_missile.pop(i)

        # Loop through the player's missile list and do various tasks
        for i, _ in enumerate(player_missile):
            # Move
            player_missile[i].move()

            # Check leave
            if player_missile[i].position[1] < -32:
                player_missile[i].state = False

            # Check collision with the enemy's missile
            if player_missile[i].state:
                hit_x = player_missile[i].position[0] + \
                                    (pygame.Surface.get_width(player_missile[i].icon) / 2)
                hit_y = player_missile[i].position[1] + \
                                    (pygame.Surface.get_height(player_missile[i].icon) / 2)

                for _i, _ in enumerate(enemy_missile):
                    if enemy_missile[_i].is_collision(hit_x, hit_y) and \
                                                            enemy_missile[_i].state:
                        enemy_missile[_i].state = False
                        explosion.append(Explosion())
                        explosion[-1].splash(enemy_missile[_i].position[0], \
                                                        enemy_missile[_i].position[1])
                        enemy_missile.pop(_i)

            # Check enemy's ship hit
            if player_missile[i].state:
                for _i, _ in enumerate(enemies):
                    hit_x = enemies[_i].position[0] + \
                                                (pygame.Surface.get_width(enemies[_i].icon) / 2)
                    hit_y = enemies[_i].position[1] + \
                                                (pygame.Surface.get_height(enemies[_i].icon) / 2)

                    if player_missile[i].is_collision(hit_x, hit_y):
                        enemies[_i].hitpoints -= 1

                        if enemies[_i].hitpoints == 0:
                            score.value += 1
                            player_missile[i].state = False
                            explosion.append(Explosion())
                            explosion[-1].splash(player_missile[i].position[0], \
                                                                player_missile[i].position[1])

                            if random.randint(0, 10) <= enemies[_i].drop_rate:
                                package.append(Package())
                                package[-1].type = random.choice( \
                                    ['hitpoints', 'skin', 'velocity', 'gun_reload'])
                                package[-1].update_skin()
                                package[-1].position[0] = enemies[_i].position[0]
                                package[-1].position[1] = enemies[_i].position[1]
                                package[-1].state = True
                                screen.blit(package[-1].icon, \
                                    (package[-1].position[0], package[-1].position[1]))

                            enemies[_i] = Enemy()
                            enemies[_i].level(score.value)
                        else:
                            explosion.append(Explosion())
                            explosion[-1].splash(player_missile[i].position[0], \
                                                        player_missile[i].position[1])
                            player_missile[i].state = False

            # Remove unnecessary objects
            if not player_missile[i].state:
                player_missile.pop(i)

        # Fly and open the package
        for i, _ in enumerate(package):
            if package[i].state:
                package[i].move()

            if package[i].is_collision(player.position[0], player.position[1]):
                is_upgraded = package[i].open(player, is_upgraded)
                package[i].sound.play()
                package[i].state = False
                hitpoints.value = player.hitpoints

        # Spot boss
        if random.randint(0, 3000) == 666:
            enemies.append(Enemy())
            enemies[-1].boss()

        # Draw explosion splash
        for i, _ in enumerate(explosion):
            explosion[i].splash_last(explosion[i].position[0], explosion[i].position[1])

            if not explosion[i].state:
                explosion.pop(i)

        score.draw(10, 10)
        hitpoints.draw(10, 30)
        pygame.display.update()

intro(True)
main_loop(True)
