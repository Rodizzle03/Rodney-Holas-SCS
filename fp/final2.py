# Credit: coding_lifestyle_4u for main parts of code

import pygame
import random
import math
from pygame import mixer

pygame.init()
mixer.init()

mixer.music.load('../fp/assets/sounds/Halo.mp3')
mixer.music.play(-1)

# Set up the screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Cowboy Shooter")
icon = pygame.image.load('../fp/assets/sprites/spaceship.png')
pygame.display.set_icon(icon)

# Load images and sounds
background = pygame.image.load('../fp/assets/sprites/space.png')
spaceshiping = pygame.image.load('../fp/assets/sprites/spaceship.png')
spaceshiping2 = pygame.image.load('../fp/assets/sprites/spaceship2.png')
aliening = pygame.image.load('../fp/assets/sprites/ufo.png')
bulleting = pygame.image.load('../fp/assets/sprites/bullet.png')

# Fonts
font = pygame.font.SysFont('Arial', 32, 'bold')
font_gameover = pygame.font.SysFont('Arial', 64, 'bold')

# Sounds
laser_sound = mixer.Sound('../fp/assets/sounds/lazer.mp3')
explosion_sound = mixer.Sound('../fp/assets/sounds/explode.mp3')

# Game variables
spaceshipX = 370
spaceshipY = 480
changeX = 0

spaceship2X = 370
spaceship2Y = 480
change2X = 0

num_of_aliens = 12
alienX = [random.randint(0, 736) for _ in range(num_of_aliens)]
alienY = [random.randint(30, 150) for _ in range(num_of_aliens)]
alienspeedX = [-0.25 for _ in range(num_of_aliens)]
alienspeedY = [30 for _ in range(num_of_aliens)]

alien2X = [random.randint(0, 736) for _ in range(num_of_aliens)]
alien2Y = [random.randint(20, 150) for _ in range(num_of_aliens)]
alienspeed2X = [1 for _ in range(num_of_aliens)]
alienspeed2Y = [20 for _ in range(num_of_aliens)]

bulletX = 386
bulletY = 450
check = False

bullet2X = 386
bullet2Y = 450
check2 = False

score = 0
score2 = 0

level = 1  # Initial level
max_score_per_level = 20  # Number of points needed to advance to the next level
winning_score = 100  # Number of points needed to win the game

running = True
game_active = False  # Variable to control if the game is active or in the menu
num_players = 1  # Default number of players


# Functions
def score_text():
    img = font.render(f'Player 1 Score: {score} | Level: {level}', True, 'white')
    if num_players == 2:
        img2 = font.render(f'Player 2 Score: {score2} | Level: {level}', True, 'white')
        screen.blit(img2, (10, 40))
    screen.blit(img, (10, 10))


def gameover():
    img_gm = font_gameover.render('GAME OVER', True, 'white')
    screen.blit(img_gm, (200, 250))


def winning_screen():
    img_win = font_gameover.render('YOU WIN!', True, 'white')
    screen.blit(img_win, (250, 250))


def main_menu():
    menu_font = pygame.font.SysFont('Arial', 64, 'bold')
    title_text = menu_font.render('Space Cowboy Shooter', True, 'white')
    start_text = font.render('Press 1 for 1 Player\nPress 2 for 2 Players\nPress SPACE to start', True, 'white')

    screen.blit(title_text, (150, 200))
    screen.blit(start_text, (50, 350))

    pygame.display.update()


def reset_game():
    global spaceshipX, spaceshipY, spaceship2X, spaceship2Y
    global bulletX, bulletY, check, bullet2X, bullet2Y, check2
    global score, score2, level, game_active

    spaceshipX = 370
    spaceshipY = 480
    changeX = 0

    spaceship2X = 370
    spaceship2Y = 480
    change2X = 0

    bulletX = 386
    bulletY = 450
    check = False

    bullet2X = 386
    bullet2Y = 450
    check2 = False

    score = 0
    score2 = 0

    level = 1
    game_active = False


# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_active:  # If the game is not active, check for key input in the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    num_players = 1
                elif event.key == pygame.K_2:
                    num_players = 2
                elif event.key == pygame.K_SPACE:
                    game_active = True

    if game_active:
        if game_active:
            screen.blit(background, (0, 0))

            keys = pygame.key.get_pressed()

            # Player 1 controls
            if keys[pygame.K_a]:
                spaceshipX -= 0.5
                # Bound the spaceship within the left edge of the screen
                spaceshipX = max(spaceshipX, 0)
            if keys[pygame.K_d]:
                spaceshipX += 0.5
                # Bound the spaceship within the right edge of the screen
                spaceshipX = min(spaceshipX, 800 - 64)  # Assuming the width of the spaceship is 64

            # Player 2 controls (if applicable)
            if num_players == 2:
                if keys[pygame.K_LEFT]:
                    spaceship2X -= 0.5
                    # Bound the spaceship within the left edge of the screen
                    spaceship2X = max(spaceship2X, 0)
                if keys[pygame.K_RIGHT]:
                    spaceship2X += 0.5
                    # Bound the spaceship within the right edge of the screen
                    spaceship2X = min(spaceship2X, 800 - 64)  # Assuming the width of the spaceship is 64

        if keys[pygame.K_a]:
            spaceshipX -= 0.5
        if keys[pygame.K_d]:
            spaceshipX += 0.5
        if keys[pygame.K_SPACE]:
            if not check:
                check = True
                bulletX = spaceshipX + 16
                laser_sound.set_volume(0.1)
                laser_sound.play()

        if num_players == 2:
            if keys[pygame.K_LEFT]:
                spaceship2X -= 0.5
            if keys[pygame.K_RIGHT]:
                spaceship2X += 0.5
            if pygame.mouse.get_pressed()[0]:  # Left Mouse for shooting
                if not check2:
                    check2 = True
                    bullet2X = spaceship2X + 16
                    laser_sound.set_volume(0.1)
                    laser_sound.play()

        for i in range(num_of_aliens):
            if alienY[i] > 420:
                for j in range(num_of_aliens):
                    alienY[j] = 2000
                gameover()
                break

            alienX[i] += alienspeedX[i]
            if alienX[i] <= 0:
                alienspeedX[i] = 0.25
                alienY[i] += alienspeedY[i]
            if alienX[i] >= 736:
                alienspeedX[i] = -0.25
                alienY[i] += alienspeedY[i]

            distance = math.sqrt(math.pow(bulletX - alienX[i], 2) + math.pow(bulletY - alienY[i], 2))
            if distance < 27:
                explosion_sound.set_volume(1)
                explosion_sound.play()
                check = False
                alienX[i] = random.randint(0, 736)
                alienY[i] = random.randint(30, 150)
                score += 1

                # Check if the player has won
                if score >= winning_score or score2 >= winning_score:
                    winning_screen()
                    winner = mixer.Sound('../fp/assets/sounds/win.mp3')
                    winner.play()
                    reset_game()

                # Check if the player has reached the required score for the next level
                elif score >= level * max_score_per_level:
                    level += 1
                    # Increase the difficulty by modifying game variables
                    # You can adjust these values to make the game harder
                    alienspeedX = [-1 * level for _ in range(num_of_aliens)]
                    alienspeedY = [2 * level for _ in range(num_of_aliens)]

            screen.blit(aliening, (alienX[i], alienY[i]))

            if num_players == 2:
                if alien2Y[i] > 420:
                    for j in range(num_of_aliens):
                        alien2Y[j] = 2000
                    gameover()
                    break

                alien2X[i] += alienspeed2X[i]
                if alien2X[i] <= 0:
                    alienspeed2X[i] = 0.25
                    alien2Y[i] += alienspeed2Y[i]
                if alien2X[i] >= 736:
                    alienspeed2X[i] = -0.25
                    alien2Y[i] += alienspeed2Y[i]

                distance2 = math.sqrt(math.pow(bullet2X - alien2X[i], 2) + math.pow(bullet2Y - alien2Y[i], 2))
                if distance2 < 27:
                    explosion_sound.set_volume(1)
                    explosion_sound.play()
                    check2 = False
                    alien2X[i] = random.randint(0, 736)
                    alien2Y[i] = random.randint(30, 150)
                    score2 += 1

                    # Check if the player has won
                    if score2 >= winning_score:
                        game_active = False
                        winning_screen()
                        winner = mixer.Sound('../fp/assets/sounds/win.mp3')
                        winner.play()
                        reset_game()

                    # Check if the player has reached the required score for the next level
                    elif score2 >= level * max_score_per_level:
                        level += 1
                        # Increase the difficulty by modifying game variables
                        # You can adjust these values to make the game harder
                        alienspeed2X = [1 * level for _ in range(num_of_aliens)]
                        alienspeed2Y = [5 * level for _ in range(num_of_aliens)]

                screen.blit(aliening, (alien2X[i], alien2Y[i]))

        if bulletY <= 0:
            bulletY = 490
            check = False
        if check:
            screen.blit(bulleting, (bulletX, bulletY))
            bulletY -= 2

        if num_players == 2:
            if bullet2Y <= 0:
                bullet2Y = 490
                check2 = False
            if check2:
                screen.blit(bulleting, (bullet2X, bullet2Y))
                bullet2Y -= 2

        screen.blit(spaceshiping, (spaceshipX, spaceshipY))
        if num_players == 2:
            screen.blit(spaceshiping2, (spaceship2X, spaceship2Y))  # Draw second spaceship
        score_text()
    else:
        main_menu()

    pygame.display.update()
