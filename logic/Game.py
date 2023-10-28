import math
from math import *

import pygame
from pygame import Vector2

from entities.Player import Player
from entities.Projectile import Projectile
from logic.Canvas import Canvas
from network.Network import Network
from utils.Direction import Direction


class Game:
    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, "Tank2D")
        self.player1 = Player(60, 300)
        self.player2 = Player(self.width - 60, 300)
        self.last_shot_time = 0
        self.shoot_cooldown = 50

    def run(self):
        clock = pygame.time.Clock()
        run = True

        while run:
            clock.tick(240)

            current_time = pygame.time.get_ticks()  # Get the current time in milliseconds

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if (keys[pygame.K_d]
                    and self.player1.sprite_rect.right <= self.width - self.player1.velocity):
                self.player1.move(Direction.RIGHT)

            if (keys[pygame.K_a]
                    and self.player1.sprite_rect.left >= self.player1.velocity):
                self.player1.move(Direction.LEFT)

            if (keys[pygame.K_w]
                    and self.player1.sprite_rect.top >= self.player1.velocity):
                self.player1.move(Direction.UP)

            if (keys[pygame.K_s]
                    and self.player1.sprite_rect.bottom <= self.height - self.player1.velocity):
                self.player1.move(Direction.DOWN)

            self.player1.move_projectiles()

            angle, heading = self.get_angle_heading()
            self.player1.rotate_angle(angle)

            if (pygame.mouse.get_pressed()[0]
                    and current_time - self.last_shot_time >= self.shoot_cooldown):
                proj_x = self.player1.sprite_rect.centerx + self.player1.gun_length * cos(radians(angle))
                proj_y = self.player1.sprite_rect.centery - self.player1.gun_length * sin(radians(angle))
                proj_pos = Vector2(proj_x, proj_y)
                # self.player.create_projectile(Projectile(start_pos=self.player.sprite_rect.center, heading=heading))
                self.player1.create_projectile(Projectile(start_pos=proj_pos, heading=heading))
                self.last_shot_time = current_time

            self.destroy_projectiles()
            self.compute_collisions()

            # Send Network stuff
            self.player2.sprite_rect.x, self.player2.sprite_rect.y, self.player2.rotation_angle = self.parse_data(self.send_data())
            self.player2.rotate()

            self.canvas.draw_background()
            self.player1.draw_hitbox(self.canvas.get_canvas())
            self.player1.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.player2.draw_hitbox(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def get_angle_heading(self):
        mouse_pos = pygame.mouse.get_pos()
        heading = (mouse_pos - Vector2(self.player1.sprite_rect.center)).normalize()
        angle = math.degrees(math.atan2(-heading.y, heading.x))
        return angle, heading

    def destroy_projectiles(self):
        for proj in self.player1.projectiles:
            if (proj.sprite_rect.x < 0
                    or proj.sprite_rect.x > self.width
                    or proj.sprite_rect.y < 0
                    or proj.sprite_rect.y > self.height):
                self.player1.destroy_projectile(proj)

    def compute_collisions(self):
        for proj in self.player1.projectiles:
            if proj.sprite_rect.colliderect(self.player2.sprite_rect):
                self.player1.destroy_projectile(proj)

    def send_data(self):
        data = f"{self.net.id}:{self.player1.sprite_rect.x},{self.player1.sprite_rect.y},{self.player1.rotation_angle}"
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1]), float(d[2])
        except:
            return 0, 0
