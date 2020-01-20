import pygame
from pygame import mixer
import random
import math

# Initialize the pygame to access all the methods of pygame
pygame.init()

# create a screen and add background
screen = pygame.display.set_mode((800, 600))  # width, height
background = pygame.image.load('background.png')

# set Title and Icon
pygame.display.set_caption('Space Invaders')  # set Title of window
icon = pygame.image.load('ufo.png')  # load image into icon
pygame.display.set_icon(icon)  # add icon into title

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 for loop

# Player
playerImage = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# enemy
enemyImage = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

number_of_enemies = 6

for i in range(number_of_enemies):
    enemyImage.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(3)
    enemyY_change.append(20)

# bullet
bulletImage = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = -20
bullet_state = "ready"  # you can see the bullet on the screen

# Score
score_value = 0
score_X = 10
score_Y = 10

font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)  # create font of text


def show_score(x, y):
    # make score then put it into screen
    score = font.render('Score : ' + str(score_value), True,
                        (255, 255, 255))  # what should be displayed, True = it will show on screen, on which color
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render('GAME OVER', True, (255, 255, 255))
    screen.blit(over_font, (200, 250))


def player(x, y):
    screen.blit(playerImage, (x, y))  # blit = to draw -> draw the image on the screen


def enemy(x, y, i):
    screen.blit(enemyImage[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImage,
                (x + 16, y + 10))  # calculation make sure that the bullet appears on the center of the spaceship


def isCollision(enemyX, enemyY, bulletX, bulletY):
    # at a certain distance, a collision will happen
    distance = math.sqrt(
        math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))  # create a distance with the coordinates
    if distance < 27:
        return True
    else:
        return False


# create a loop to stop the screen disappear
# event: anything which happen inside the window
# Game loop: make sure that the game is always running and the window isn't closed
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_h:  # Problem: das Programm geht immer nach rechts
                playerX_change = -5
            if event.key == pygame.K_RIGHT or event.key == pygame.K_l:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # get the current X coordinate of the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0.0

    # RGB color = set color of the screen
    # screen.fill([255,253,208])
    screen.blit(background, (0, 0))

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    playerX += playerX_change

    # set some enemys' features
    for i in range(number_of_enemies):

        # Game Over

        if enemyY[i] > 200:
            for j in range(number_of_enemies):
                enemyY[i] = 2000
            game_over_text()
            break
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
        enemyX[i] += enemyX_change[i]
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 800)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # collision

    # enemyY += enemyY_change #mit dem Befehl läuft der Feind in zick zack modus,
    # ohne läuft er paparall zur x achse bis zur ende der zeile dann wird y um 5 erhöht
    # print(str(enemyY) + " " + str(enemyX))
    # print(enemyY_change)

    # bullet movement
    # 1. check the state of our bullet
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY += bulletY_change
        # 2. reload the bullet
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    player(playerX, playerY)
    show_score(score_X, score_Y)
    pygame.display.update()  # update the screen
