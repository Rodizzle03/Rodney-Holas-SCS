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
