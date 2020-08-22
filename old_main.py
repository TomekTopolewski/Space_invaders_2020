import pygame, random, math
from pygame import mixer

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((800, 600))

# Caption and Icon
pygame.display.set_caption("Space Invaders 2020")
icon = pygame.image.load('tank-icon.png')
pygame.display.set_icon(icon)

# Now we have more enemies icon
enemies_icon = []
enemies_icon.append(pygame.image.load('spaceship.png'))
enemies_icon.append(pygame.image.load('spaceship2.png'))
enemies_icon.append(pygame.image.load('spaceship3.png'))
enemies_icon.append(pygame.image.load('spaceship4.png'))
enemies_icon.append(pygame.image.load('spaceship5.png'))
enemies_icon.append(pygame.image.load('spaceship6.png'))

# Create a list for storing enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6 #Number of enemies

# Based on number of enemies create a buch of spaceships
for i in range (num_of_enemies):
    enemyImg.append(enemies_icon[0]) # We start with basic enemies icon
    enemyX.append(random.randint(100, 700))
    enemyY.append(random.randint(0, 150))
    enemyX_change.append(4) # How fast in x-axis enemies will try to avoid your shoots
    enemyY_change.append(random.randint(15, 25)) # How fast in y-axis enemies will fly to you. Now ships can be faster or slower, but not much.

# Loading images
playerImg = []
playerImg.append(pygame.image.load('tank.png'))
playerImg.append(pygame.image.load('aircraft.png'))
background = pygame.image.load('background.png')
shootImg = pygame.image.load('fire.png')

# Load sounds
explosion_sound = mixer.Sound('explosion.wav')
shoot_sound = mixer.Sound('shoot.wav')
shoot_sound2 = mixer.Sound('shoot2.wav')

# Play background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Player default position
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Shoot
shootX = 0
shootY = 0
shootY_change = 10 # How fast a missle will fly
shoot_state = False #False mean no bullet are flying to the target
weapon_range = 20 # This value is used in isCollised function which check if missle hit target


# Score
score_value = 0
font = pygame.font.Font("space_age.ttf", 32)
scoreX = 10
scoreY = 10

# Game over text
game_over_font = pygame.font.Font("space_age.ttf", 72)


# Draw score text on the screen
def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

# Draw game over text on the screen
def game_over(x, y):
    game_over_text = game_over_font.render("Game over!", True, (47, 79, 79))
    screen.blit(game_over_text, (x, y))

# Draw player on the screen
def player(x, y, playerImg):
    screen.blit(playerImg, (x, y))

# Draw enemy on the screen
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Draw bullet ont the screen
def shoot(x, y):
    global shoot_state
    shoot_state = True
    screen.blit(shootImg, (x + 16, y + 10)) # Bullet will start from the middle of the player ship (x-axis) and 10 pixel in front of them (y-axis)

# Check collision
def isCollision(enemyX, enemyY, shootX, shootY):
    distance = math.sqrt(math.pow(enemyX - shootX, 2) + (math.pow(enemyY - shootY, 2))) # Calculating a distance between two points
    if distance < weapon_range and shoot_state == True: # By modifying weapon range you let statement return true more often
        return True
    else:  
        return False

# Main loop
running = True
while running:

    # Fill background with black
    screen.fill((0, 0, 0))

    #Fill background with image
    screen.blit(background, (0, 0))

    # Loop through the events, such as pressing a key
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -7 # Modyfing this value and values below, your tank will be faster (each key pressing will move him further)
            if event.key == pygame.K_RIGHT:
                playerX_change = 7
            if event.key == pygame.K_UP:
                playerY_change = -7
            if event.key == pygame.K_DOWN:
                playerY_change = 7
            if event.key == pygame.K_SPACE:
                if shoot_state == False: # You can only shoot when the bullet is not flying to target
                    if score_value > 50: # When you pass 50 points, you will get a new skin (code below) and the sound
                        shoot_sound2.play()
                    else:
                        shoot_sound.play()
                    shootX = playerX # Missle will be launch from the player postion
                    shootY = playerY
                    shoot(shootX, shootY)

        if event.type == pygame.KEYUP: # If you release the key the tank will stop moving, without this one key press will send tank to the edge of the screen
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerX_change = 0
                playerY_change = 0

    # Change the player position
    playerX += playerX_change # Based on what you pressed tank position will be draw by the function a couple of lines below this one
    playerY += playerY_change

    # Don't let the player espace the screen
    # Special cases for corners
    if playerY >= 536 and playerX == 736:
        playerX = 736
        playerY = 536
    elif playerY >= 536 and playerX == 0:
        playerX = 0
        playerY = 536
    elif playerY <= 0 and playerX == 736:
        playerX = 736
        playerY = 0
    elif playerY <=0 and playerX == 0:
        playerX = 0
        playerY = 0

    # General rules for not letting player to escape the screen
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    elif playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    # Enemies mouvment
    for i in range(num_of_enemies): #Since we have a couple of enemies, we have to loop through each one

        if enemyY[i] > 460: #If enemies cross this line (fly to you too close), gave will be over
            for j in range(num_of_enemies):
                enemyY[j] = 800 # Enemies will be draw of the screen when you loose
            game_over(130, 200) # Game over text is displayed
            break

        enemyX[i] += enemyX_change[i] # This line really move the enemies through each pass of the loop

        # Making sure that enemies won't cross the boundaries of the screen. 0-100 and 650-736 are places when they can change direction
        if enemyX[i] <= random.randint(0,100): # Now enemies can change direction more quickly, which will create game more difficult and unpredicted
            enemyX_change[i] = 4 # Enemy flying to the right
            enemyY[i] += enemyY_change[i] # Enemy will flying closer to you for every direction change
        elif enemyX[i] >= random.randint(650,736):
            enemyX_change[i] = -4 # Enemy flying to the left
            enemyY[i] += enemyY_change[i]

        # Checking if bullet hit the target
        # If isCollision function return True, we will play BOOM! sound, give you one point, let for another shoot and spot new enemy
        collision = isCollision(enemyX[i], enemyY[i], shootX, shootY)
        if collision:
            explosion_sound.play()
            shoot_state = False
            score_value += 1
            enemyX[i] = random.randint(50, 700) # Coordinates for a new enemy
            enemyY[i] = random.randint(0, 50)

            if score_value > 20 and score_value <= 40: # When you shoot N enemies next one will have a new skin
                enemyImg[i] = enemies_icon[1]
            elif score_value > 40 and score_value <= 60: 
                enemyImg[i] = enemies_icon[2]
            elif score_value > 60 and score_value <= 80:
                enemyImg[i] = enemies_icon[3]
            elif score_value > 80 and score_value <= 100:
                enemyImg[i] = enemies_icon[4]
            elif score_value > 100:
                enemyImg[i] = enemies_icon[5]
            else:
                enemyImg[i] = enemies_icon[0]   # Basic icon for enemy

        # Draw new position on the screen
        enemy(enemyX[i], enemyY[i], i)

    # Missle flying through the air until it hits the target or leave the screen
    if shoot_state == True:
        shoot(shootX, shootY)
        shootY -= shootY_change

    # Let shoot another missle when this one leave the screen
    if shootY <= 0:
        shoot_state = False

    # Draw player position on the screen
    if score_value > 50: # If player will reach 50 points it will get a new skin
        player(playerX, playerY, playerImg[1])
    else:
        player(playerX, playerY, playerImg[0])

    #Draw score in the left right corner
    show_score(scoreX, scoreY)

    # Update display every frame
    pygame.display.update()
