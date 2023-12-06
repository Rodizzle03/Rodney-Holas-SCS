import pygame
import random

from game_parameters import *

pygame.init()

screen_width, screen_height = 800, 600
tile_size = 40

screen = pygame.display.set_mode((screen_width, screen_height))

def draw_background(screen, platforms):
    grave_yard = pygame.image.load("../assets/sprites/graveyard.png").convert()
    platforms_image = pygame.image.load("../assets/sprites/platform.png").convert()
    platforms_image.set_colorkey((0, 0, 0))

    for x in range(0, screen_width, tile_size):
        for y in range(0, screen_height, tile_size):
            screen.blit(grave_yard, (x, y))

    for platform in platforms:
        screen.blit(platforms_image, platform)

def main():
    clock = pygame.time.Clock()
    platforms = []

    player = pygame.Rect(50, screen_height - tile_size * 3, tile_size, tile_size)
    player_speed = 5
    jump_height = -15
    gravity = 1
    is_jumping = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < screen_width:
            player.x += player_speed

        # Jumping
        if not is_jumping:
            if keys[pygame.K_SPACE]:
                is_jumping = True
        else:
            player.y += gravity
            if player.y > screen_height - tile_size * 2:
                player.y = screen_height - tile_size * 2
                is_jumping = False

        # Add new platforms randomly
        if random.randint(0, 100) < 10:
            x = random.randint(0, screen_width - tile_size)
            y = screen_height - tile_size * 2 + 20
            platforms.append(pygame.Rect(x, y, tile_size, tile_size))

        # Remove platforms randomly
        if random.randint(0, 100) < 5 and len(platforms) > 0:
            platforms.pop(random.randint(0, len(platforms) - 1))

        # Check for collisions with platforms
        for platform in platforms:
            if player.colliderect(platform) and not is_jumping:
                player.y = platform.y - tile_size * 2
                is_jumping = False

        # Update player position
        player.y += gravity
        draw_background(screen, platforms)
        pygame.draw.rect(screen, (255, 0, 0), player)
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()