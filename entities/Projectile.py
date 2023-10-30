import pygame.image
from pygame import Vector2


class Projectile:
    def __init__(self, start_pos, heading: Vector2, sprite_path="../resources/projectile_sprite.png", scale=(16, 13)):
        self.velocity = 3.0
        self.heading = heading
        self.original_sprite = pygame.image.load(sprite_path)

        if scale:
            self.original_sprite = pygame.transform.scale(self.original_sprite, scale)

        self.sprite = self.original_sprite.copy()  # Ensure that we start with a scaled sprite
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.center = (start_pos[0], start_pos[1])

        # Rotate the sprite towards direction
        angle = self.heading.angle_to(Vector2(1, 0))
        self.sprite = pygame.transform.rotate(self.original_sprite, angle)
        self.sprite_rect = self.sprite.get_rect(center=self.sprite_rect.center)

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)

    def move(self):
        self.sprite_rect.x += self.heading.x * self.velocity
        self.sprite_rect.y += self.heading.y * self.velocity
