import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()
# Create the screen
screen = pygame.display.set_mode((800, 600))
# adding background image to the game window
background = pygame.image.load("background.png")
# background sound
mixer.music.load("background.wav")
mixer.music.play(-1)  # -1 plays the music in infinite loop until the game is quit
# Adding title and icon to the game window
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(icon)
# Player image
playerImg = pygame.image.load("fighterplane.png")
playerX = 370
playerY = 480
playerX_change = 0

# Enemy image
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
numofenemy = 10
for i in range(numofenemy):
    enemyImg.append(pygame.image.load("alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(50.0)

# Bullet image
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 30.0
bullet_state = "ready"  # ready state means that it cannot be seen on the screen and

# fire state represents that the bullet is currently moving
score = 0
font = pygame.font.Font("freesansbold.ttf", 32)
textX = 10
textY = 10
# game over text
gameoverfont = pygame.font.Font("freesansbold.ttf", 64)


def showScore(x, y):
    scoreValue = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(scoreValue, (x, y))


def gameOver():
    over_text = gameoverfont.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def firebullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if dist < 27:
        return True


# Game loop Making the screen open until someone hits close button
running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Created a gaming screen and it closes only when the close button is pressed
        # to check if a key is pressed (keystroke) then to check if it is a left or right key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -10
            if event.key == pygame.K_RIGHT:
                playerX_change = 10
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    firebullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0.0

    playerX += playerX_change
    # adding a boundary to the game window
    if playerX < 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
    # enemy movement
    for i in range(numofenemy):
        # game over module
        if enemyY[i] > 440:
            for j in range(numofenemy):
                enemyY[j] = 2000
            gameOver()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = 6
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -6
            enemyY[i] += enemyY_change[i]
        # collision detection
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score += 10
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)
        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    showScore(textX, textY)
    pygame.display.update()  # important line. It keeps the display screen to get updated continuously
