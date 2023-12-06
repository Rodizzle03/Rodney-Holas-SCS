import pygame
import random
import sys
import player
from game_parameters import *
import utilities
import bullet
import pygame.mixer
import time
from math import atan2, pi

# Initialize Pygame
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("../fp/assets/sounds/Halo.mp3")
pygame.mixer.music.play()
# Set the desired duration in seconds
duration = 30  # for example, play for 10 seconds
# Wait for the specified duration
time.sleep(duration)
# Stop the music
pygame.mixer.music.stop()

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Staring Game")

# Load sound effects
ghost_hurt = pygame.mixer.Sound('../fp/assets/sounds/ghost_die.mp3')
hurt = pygame.mixer.Sound('../fp/assets/sounds/oof.mp3')
life_icon = pygame.image.load('../fp/assets/sprites/stickman.png').convert()
bullet_sounds = pygame.mixer.Sound('../fp/assets/sounds/lazer.mp3')
end_game = pygame.mixer.Sound('../fp/assets/sounds/Gameover.mp3')
life_icon.set_colorkey((0, 0, 0))
clock = pygame.time.Clock()


def draw_background(screen, platforms):
    grave_yard = pygame.image.load("../fp/assets/sprites/graveyard.png").convert()
    platforms_image = pygame.image.load("../fp/assets/sprites/platform.png").convert()
    platforms_image.set_colorkey((0, 0, 0))

    for x in range(0, screen_width, tile_size):
        for y in range(0, screen_height, tile_size):
            screen.blit(grave_yard, (x, y))

    for platform in platforms:
        screen.blit(platforms_image, platform)

    platforms.draw(screen)


def main1():
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Add new platforms randomly
        if random.randint(0, 100) < 5:
            x = random.randint(0, screen_width - tile_size)
            y = screen_height - tile_size * 2 + 20
            platform = Platform(x, y)
            platforms.add(platform)
            all_sprites.add(platform)

        # Remove platforms randomly
        if random.randint(0, 100) < 2 and len(platforms) > 0:
            platform_to_remove = random.choice(platforms.sprites())
            platforms.remove(platform_to_remove)
            all_sprites.remove(platform_to_remove)

        player.update()

        draw_background(screen, platforms)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(20)


if __name__ == "__main1__":
    main1()


    class Platform(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.image.load("../fp/assets/sprites/platform.png").convert()
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y


    class Player(pygame.sprite.Sprite):
        def __init__(self, x, y, platforms):
            super().__init__()
            self.image = pygame.image.load("../fp/assets/sprites/stickman.png").convert()
            self.image.set_colorkey((0, 0, 0))
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.y_velocity = 0
            self.on_ground = False
            self.platforms = platforms

        def jump(self):
            if self.on_ground:
                self.y_velocity = -PLAYER_JUMP

        def update(self):
            self.y_velocity += GRAVITY
            self.rect.y += self.y_velocity

            # Check for collisions with platforms
            collisions = pygame.sprite.spritecollide(self, self.platforms, False)

            # If there's a collision, set the player on top of the platform
            if collisions:
                self.on_ground = True
                self.rect.y = collisions[0].rect.y - self.rect.height
                self.y_velocity = 0
            else:
                self.on_ground = False


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('../fp/assets/sprites/ghost.png').convert()
        self.image = pygame.transform.flip(self.image, True, False)
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
        self.rect.center = (x, y)

    def update(self, direction):
        self.x += self.speed * cos(direction)
        self.rect.x = self.x
        self.y += self.speed * sin(direction)
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.image, self.rect)


enemies = pygame.sprite.Group()

# Main loop
running = True
background = screen.copy()
draw_background(background, platforms)


def draw_welcome(screen):
    # draw the title at the top center of the screen
    game_font = pygame.font.Font("../fp/assets/fonts/Black_Crayon.ttf", 64)
    text = game_font.render("Welcome to Phantom Pursuit", True, (0, 255, 0))
    screen.blit(text, (screen_width / 2 - text.get_width() / 2, screen_height / 2 - text.get_height() / 2))


draw_mess = True
pygame.mixer.music.load("../fp/assets/sounds/Monster.mp3")
pygame.mixer.music.play(-1)

# Method 1
if draw_mess:
    # draw the background
    screen.blit(background, (0, 0))

    # welcome message
    draw_welcome(screen)

    # Update the display
    pygame.display.flip()
    time.sleep(5)

# add enemies and player
add_enemies(6)
player = Player(screen_width / 2, screen_height)

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
            if event.key == pygame.K_SPACE:
                player.move.jump()
            elif event.event == pygame.MOUSEDOWN:
                if pygame.mouse.get_pressed()[0]:
                    # pos = player.rect.midright
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    angle = -atan2(mouse_y - player.y, mouse_x - player.x)
                    add_bullets(1, player.rect.center, angle)
                    pygame.mixer.Sound.play(bullet_sounds)

    # update game objects
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

    result = pygame.sprite.spritecollide(player, enemies, True)
    if result:
        lives -= len(result)
        # play hurt sound
        pygame.mixer.Sound.play(hurt)
        # add new fish
        add_enemies(len(result))

    for enemy in enemies:
        if enemy.rect.x < - enemy.rect.width:
            enemies.remove(enemy)
            add_enemies(1)

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

    # draw the background
    screen.blit(background, (0, 0))

    # draw game object
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