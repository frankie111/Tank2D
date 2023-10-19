import pygame


class Player:
    def __init__(self, start_x, start_y, sprite_path='tank_sprite.png', scale=(100, 100)):
        self.x = start_x
        self.y = start_y
        self.velocity = 2

        # Load the sprite
        self.sprite = pygame.image.load(sprite_path)

        # Scale the sprite if scale parameter is provided
        if scale:
            self.sprite = pygame.transform.scale(self.sprite, scale)

        self.sprite_rect = self.sprite.get_rect()
        self.sprite_rect.center = (self.x, self.y)

    def draw(self, g):
        # Draw the tank sprite on the screen
        g.blit(self.sprite, self.sprite_rect.topleft)

    def move(self, direction):
        """
        :param direction: 0 - 3 (right, left, up, down)
        :return: None
        """

        if direction == 0:
            self.x += self.velocity
        elif direction == 1:
            self.x -= self.velocity
        elif direction == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity

        # Update the sprite's position
        self.sprite_rect.center = (self.x, self.y)
