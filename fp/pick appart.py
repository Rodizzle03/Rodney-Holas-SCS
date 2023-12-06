import pygame
import sys
from fish import fishes
from enemy import enemies
from player import Player
from game_parameters import *
from utilities import draw_background, add_fish, add_enemies, add_bullets
from final1.bullet import bullets
import pygame.mixer
import time
from math import atan2

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("../assets/sounds/Boston.mp3")
pygame.mixer.music.play(-1)

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Adding Enemies")

# Load sound effects
chomp = pygame.mixer.Sound('../assets/sounds/chomp.wav')
hurt = pygame.mixer.Sound('../assets/sounds/moan.mp3')
bubbles = pygame.mixer.Sound('../assets/sounds/bubbles.wav')
life_icon = pygame.image.load('../assets/sprites/orange_fish_alt.png').convert()
bullet_sounds = pygame.mixer.Sound('../assets/sounds/Bell.mp3')
life_icon.set_colorkey((0, 0, 0))
clock = pygame.time.Clock()

# Main loop
running = True
background = screen.copy()
draw_background(background)

# add fish, enemies, and player
add_fish(10)
add_enemies(6)
player = Player(screen_width / 2, screen_height / 2)

# Initialize score and custom font to display it
score = 0
lives = NUM_LIVES
score_font = pygame.font.Font('../assets/fonts/Black_Crayon.ttf', 48)


def draw_welcome(screen):
    # draw the title at the top center of the screen
    game_font = pygame.font.Font("../assets/fonts/Black_Crayon.ttf", 64)
    text = game_font.render("Welcome to Chomp", True, (155, 155, 255))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))


draw_mess = True

# Method 1
if draw_mess:
    # draw the background
    screen.blit(background, (0, 0))

    # welcome message
    draw_welcome(screen)

    # Update the display
    pygame.display.flip()
    time.sleep(5)

while lives > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # control player with arrow keys
        player.stop()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.move_up()
            if event.key == pygame.K_DOWN:
                player.move_down()
            if event.key == pygame.K_LEFT:
                player.move_left()
            if event.key == pygame.K_RIGHT:
                player.move_right()

            # if event.key == pygame.K_SPACE:
            # pos = player.rect.midright
            # add_bullets(1, pos, angle)
            # pygame.mixer.Sound.play(bullet_sounds)

            # add mouse event https://www.pygame.org/docs/ref/mouse.html
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                # pos = player.rect.midright
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = -atan2(mouse_y - player.y, mouse_x - player.x)
                add_bullets(1, player.rect.center, angle)
                print("hello")
                pygame.mixer.Sound.play(bullet_sounds)

    # update game objects
    fishes.update()
    player.update()
    bullets.update()

    # update each enemy direction
    for enemy in enemies:
        direction = atan2(player.y - enemy.y, player.x - enemy.x)
        enemy.update(direction)

    # make sure player does not exit the screen
    if player.rect.x <= 0:
        player.x = 0
    elif player.rect.x >= screen.get_rect().width - player.rect.width:
        player.x = screen.get_rect().width - player.rect.width
    elif player.rect.y <= 0:
        player.y = 0
    elif player.rect.y >= screen.get_rect().height - player.rect.height:
        player.y = screen.get_rect().height - player.rect.height

    # check for collisions between player and fish
    # update score and remove fish if there is a collision
    # use group collision detection
    result = pygame.sprite.spritecollide(player, fishes, True)
    if result:
        score += len(result)
        # play chomp sound
        pygame.mixer.Sound.play(chomp)
        # add new fish
        add_fish(len(result))

    # check for collisions between player and enemy fish
    # remove fish if there is a collision and reduce the
    # number of lives
    result = pygame.sprite.spritecollide(player, enemies, True)
    if result:
        lives -= len(result)
        # play chomp sound
        # pygame.mixer.Sound.play(hurt)
        # add new fish
        add_enemies(len(result))

    # if any fish have moved off the left side of the screen, remove them
    # and add a new fish off the right side of the screen
    for fish in fishes:
        if fish.rect.x < -fish.rect.width:
            fishes.remove(fish)
            add_fish(1)

    # if any enemies have moved off the left side of the screen, remove them
    # and add a new enemy off the right side of the screen
    for enemy in enemies:
        if enemy.rect.x < - enemy.rect.width:
            enemies.remove(enemy)
            add_enemies(1)

    # if any fish have moved off the left side of the screen, remove them
    # and add a new fish off the right side of the screen
    for bullet in bullets:
        if bullet.rect.x > screen_width:
            bullets.remove(bullet)

        for enemy in enemies:
            bullet_enemy = pygame.sprite.spritecollide(bullet, enemies, True)
            if bullet_enemy:  # enemy is killed?
                score += len(bullet_enemy)  # increment score is you shoot an enemy
                enemies.remove(enemy)  # remove the enemy killed
                add_enemies(1)  # add new enemy to the game
                bullets.remove(bullet)
                # pos = player.rect.midright
                # add_bullets(1, pos)

        for fish in fishes:
            bullet_fish = pygame.sprite.spritecollide(bullet, fishes, True)
            if bullet_fish:
                score -= len(bullet_fish)  # decrease score if you shoot a friend
                fishes.remove(fish)
                add_fish(1)
                bullets.remove(bullet)
                # pos = player.rect.midright
                # add_bullets(1, pos)

    # draw the background
    screen.blit(background, (0, 0))

    # draw game objects
    fishes.draw(screen)
    enemies.draw(screen)
    player.draw(screen)

    for bullet in bullets:
        bullet.draw_bullet(screen)

    # draw the score in the upper left corner
    message = score_font.render(f"{score}", True, (255, 69, 0))
    screen.blit(message, (screen_width - message.get_width() - 10, 0))

    # draw the lives in the lower left corner
    for i in range(lives):
        screen.blit(life_icon, (i * tile_size, screen_height - tile_size))

    # Update the display
    pygame.display.flip()

    # Limit the frame rate
    clock.tick(60)

screen.blit(background, (0, 0))

# show a game over message
message = score_font.render('Game Over', True, (0, 0, 0))
screen.blit(message, (screen_width / 2 - message.get_width() / 2,
                      screen_height / 2 - message.get_height() / 2))
# show the final1 score
score_text = score_font.render(f'Score: {score}', True, (0, 0, 0))
screen.blit(score_text, (screen_width / 2 - score_text.get_width() / 2,
                         screen_height / 2 + message.get_height()))
pygame.display.flip()

# play game over sound effect
pygame.mixer.Sound.play(bubbles)

# wait for user to exit the game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Quit Pygame
            pygame.quit()
            sys.exit()
