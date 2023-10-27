import math

import pygame
from pygame import Vector2

from entities.Direction import Direction
from entities.Player import Player
from entities.Projectile import Projectile
from logic.Canvas import Canvas


class Game:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, "Tank2D")
        self.player = Player(400, 300)
        self.last_shot_time = 0
        self.shoot_cooldown = 500

    def run(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(60)

            current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

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

            self.player.move_projectiles()

            angle = self.get_angle()
            self.player.rotate(angle)

            if (pygame.mouse.get_pressed()[0]
                    and current_time - self.last_shot_time >= self.shoot_cooldown):
                # get direction vector
                heading = self.angle_to_vector(angle)
                self.player.create_projectile(Projectile(start_pos=self.player.sprite_rect.center, heading=heading))
                self.last_shot_time = current_time

            self.canvas.draw_background()
            self.player.draw_hitbox(self.canvas.get_canvas())
            self.player.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def get_angle(self):
        mouse_pos = pygame.mouse.get_pos()
        x_dist = mouse_pos[0] - self.player.sprite_rect.center[0]
        y_dist = -(mouse_pos[1] - self.player.sprite_rect.center[1])
        return math.degrees(math.atan2(y_dist, x_dist))

    @staticmethod
    def angle_to_vector(angle):
        return Vector2(math.cos(math.radians(angle)), -math.sin(math.radians(angle)))
