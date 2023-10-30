import pygame.image

from utils.Direction import Direction


class Player:
    def __init__(self, start_x, start_y, sprite_path="../resources/tank_sprite.png", scale=(29 * 4, 14 * 4)):
        self.velocity = 1.0
        self.rotation_angle = 0
        self.gun_length = 65
        # load the original sprite
        self.original_sprite = pygame.image.load(sprite_path)
        # Scale the sprite
        if scale:
            self.original_sprite = pygame.transform.scale(self.original_sprite, scale)

        self.sprite = self.original_sprite.copy()  # Ensure that we start with a scaled sprite
        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.center = (start_x, start_y)

        self.projectiles = []

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite_rect)  # Draw the tank sprite in the pos of sprite_rect
        for projectile in self.projectiles:
            projectile.draw(screen)

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

    def move_projectiles(self):
        for projectile in self.projectiles:
            projectile.move()

    def rotate_angle(self, angle):
        self.rotation_angle = angle
        self.sprite = pygame.transform.rotate(self.original_sprite, angle)
        self.sprite_rect = self.sprite.get_rect(center=self.sprite_rect.center)

    def rotate(self):
        self.sprite = pygame.transform.rotate(self.original_sprite, self.rotation_angle)
        self.sprite_rect = self.sprite.get_rect(center=self.sprite_rect.center)

    def create_projectile(self, proj):
        self.projectiles.append(proj)

    def destroy_projectile(self, proj):
        self.projectiles.remove(proj)

    def set_loc_rot(self, loc_rot):
        self.sprite_rect.x, self.sprite_rect.y, self.rotation_angle = loc_rot
