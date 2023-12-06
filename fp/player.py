import pygame
import random

from game_parameters import *


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


def main():
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


if __name__ == "__main__":
    main()
