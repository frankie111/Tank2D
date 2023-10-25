import math

import pygame

from entities.Direction import Direction
from entities.Player import Player
from logic.Canvas import Canvas


def get_angle(tank_position, mouse_position):
    x_dist = mouse_position[0] - tank_position[0]
    y_dist = mouse_position[1] - tank_position[1]
    angle = math.atan2(y_dist, x_dist)
    return -math.degrees(angle)


class Game:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, "Tank2D")
        self.player = Player(50, 100, self.canvas.get_canvas())

    def run(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_d]
                    and self.player.sprite_rect.right <= self.width - self.player.velocity):
                self.player.move(Direction.RIGHT)

            if (keys[pygame.K_a]
                    and self.player.sprite_rect.left >= self.player.velocity):
                self.player.move(Direction.LEFT)

            if (keys[pygame.K_w]
                    and self.player.sprite_rect.top >= self.player.velocity):
                self.player.move(Direction.UP)

            if (keys[pygame.K_s]
                    and self.player.sprite_rect.bottom <= self.height - self.player.velocity):
                self.player.move(Direction.DOWN)

            mouse_position = pygame.mouse.get_pos()
            angle = get_angle(self.player.sprite_rect, mouse_position)
            self.player.rotate(angle)

            self.canvas.draw_background()
            self.player.draw_hitbox(self.canvas.get_canvas())
            self.player.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()
