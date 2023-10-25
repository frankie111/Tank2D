import pygame.image

from entities.Direction import Direction


class Player:
    def __init__(self, start_x, start_y, sprite_path="../resources/tank_sprite.png", scale=(100, 100)):
        self.velocity = 2
        self.rotation_angle = 0
        # load the original sprite
        self.original_sprite = pygame.image.load(sprite_path).convert_alpha()
        # Scale the sprite
        if scale:
            self.original_sprite = pygame.transform.scale(self.original_sprite, scale)

        self.sprite = self.original_sprite.copy()  # Ensure that we start with a scaled sprite
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.center = (start_x, start_y)

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)  # Draw the tank sprite in the pos of sprite_rect

    def draw_hitbox(self, screen):
        hitbox_color = (82, 5, 0)
        hitbox_rect = pygame.Rect(self.sprite_rect.left, self.sprite_rect.top, self.sprite_rect.width,
                                  self.sprite_rect.height)
        pygame.draw.rect(screen, hitbox_color, hitbox_rect, 2)

    def move(self, direction):
        if direction == Direction.RIGHT:
            self.sprite_rect.x += self.velocity

        if direction == Direction.LEFT:
            self.sprite_rect.x -= self.velocity

        if direction == Direction.UP:
            self.sprite_rect.y -= self.velocity

        if direction == Direction.DOWN:
            self.sprite_rect.y += self.velocity

    def rotate(self, angle):
        self.rotation_angle = angle
        self.sprite = pygame.transform.rotate(self.original_sprite, angle)
        self.sprite_rect = self.sprite.get_rect(center=self.sprite_rect.center)
