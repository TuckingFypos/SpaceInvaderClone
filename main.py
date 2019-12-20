import math
import pygame
import random
from pygame import mixer


# Initializes Pygame
pygame.init()

# Sets screen size
screen = pygame.display.set_mode((400, 300))

# Loads the background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('battle.wav')
mixer.music.play(-1)

# Set title and icon
pygame.display.set_caption("Space Invaders")

# Player
playerImg = pygame.image.load('Player1.png')
playerX = 185
playerY = 250
playerX_change = 0.0
playerY_change = 0.0

# Enemy
enemyImg = pygame.image.load('Enemy1.png')
enemyX = random.randint(0, 365)
enemyY = random.randint(0, 68)
enemyX_change = 0.25
enemyY_change = 17

# Bullet
# States: 'ready' bullet is waiting off-screen // 'fire' bullet is being fired on screen
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 250
bulletY_change = .6
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 20)
textX = 7
textY = 7

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 50)


def show_score(x,y):
    score = font.render("Score: " + str(score_value), True,  (255, 255, 255))
    screen.blit(score, (textX, textY))

def game_over():
    over_text = font.render("GAME OVER: " + str(score_value), True,  (255, 255, 255))
    screen.blit(over_text, (160, 120))

def player(x,y):
    # Draws player on to the screen, removes other instances for "movement"
    screen.blit(playerImg, (x, y))

def enemy(x, y):
    # Draws enemy
    screen.blit(enemyImg, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x+8, y+5))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.hypot(enemyX - bulletX, enemyY - bulletY)
    if distance < 27:
        return True
    else:
        return False


# Builds main Game Loop
running = True
while running:

    # Load in the background
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -.3
            if event.key == pygame.K_RIGHT:
                playerX_change = .3
            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bullet_sound = mixer.Sound('fire.wav')
                bullet_sound.play()
                # Sets bullet origin to playerX
                bulletX = playerX
                fire_bullet(playerX, playerY)

        # Stops movement when key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0


    # Player Movement
    playerX += playerX_change

    # Enemy Movement
    enemyX += enemyX_change

    # Sets Up Screen Boundaries
    # Player
    if playerX <= 0:
        playerX = 0
    if playerX >= 366:
        playerX = 366

    # Enemy
    if enemyX <= 0:
        enemyX_change = 0.25
        enemyY += enemyY_change
    if enemyX >= 366:
        enemyX_change = -0.25
        enemyY += enemyY_change

    # Game Over
    if enemyY > 200:
        enemyY = 2000
        game_over()

    # Bullet movement
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 250
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Collision
    collision = isCollision(bulletX, bulletY, enemyX, enemyY)
    if collision:
        explosion_sound = mixer.Sound('explosion.wav')
        explosion_sound.play()
        bulletY = 250
        bullet_state = "ready"
        score_value += 1
        enemyX = random.randint(0, 365)
        enemyY = random.randint(0, 68)

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    show_score(textX, textY)

    pygame.display.update()
