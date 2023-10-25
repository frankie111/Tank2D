import math

import pygame.image

from entities.Direction import Direction


class Player:
    def __init__(self, start_x, start_y, sprite_path="../resources/tank_sprite.png", scale=(100, 100)):
        self.x = start_x
        self.y = start_y
        self.velocity = 2
        self.rotation_angle = 0
        # load the original sprite
        self.original_sprite = pygame.image.load(sprite_path)
        # Scale the sprite
        if scale:
            self.original_sprite = pygame.transform.scale(self.original_sprite, scale)

        self.sprite = self.original_sprite.copy()  # Ensure that we start with a scaled sprite
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.center = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect.topleft)  # Draw the tank sprite in the pos of sprite_rect

    def draw_hitbox(self, screen):
        
    def move(self, direction):
        if direction == Direction.RIGHT:
            self.x += self.velocity

        if direction == Direction.LEFT:
            self.x -= self.velocity

        if direction == Direction.UP:
            self.y -= self.velocity

        if direction == Direction.DOWN:
            self.y += self.velocity

        self.sprite_rect.center = (self.x, self.y)

    def rotate(self, angle):
        self.rotation_angle = angle
        self.sprite = pygame.transform.rotate(self.original_sprite, math.degrees(angle))
        self.sprite_rect = self.sprite.get_rect(center=self.sprite_rect.center)

    def get_left(self):
        return self.x - self.sprite_rect.width / 2

    def get_right(self):
        return self.x + self.sprite_rect.width / 2

    def get_top(self):
        return self.y - self.sprite_rect.height / 2

    def get_bottom(self):
        return self.y + self.sprite_rect.height / 2
