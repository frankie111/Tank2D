import math
from math import *

import pygame
from pygame import Vector2, Vector3

from entities.Bullet import Bullet
from entities.Player import Player
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
        self.shoot_cooldown = 400
        self.bullet_data = ""

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

            self.player1.move_bullets()
            self.player2.move_bullets()

            angle, heading = self.get_angle_heading()
            self.player1.rotate_angle(angle)

            if (pygame.mouse.get_pressed()[0]
                    and current_time - self.last_shot_time >= self.shoot_cooldown):
                bull_x = self.player1.sprite_rect.centerx + self.player1.gun_length * cos(radians(angle))
                bull_y = self.player1.sprite_rect.centery - self.player1.gun_length * sin(radians(angle))
                bull_pos = Vector2(bull_x, bull_y)
                bullet = Bullet(start_pos=bull_pos, heading=heading)
                self.player1.create_bullet(bullet)
                self.bullet_data += bullet.to_loc_head_str()
                self.last_shot_time = current_time

            self.destroy_bullets()
            self.compute_collisions()

            # Send Network stuff
            player_loc_rot, bullets = self.parse_data(self.send_data())
            self.player2.create_projectiles(bullets)
            self.player2.set_loc_rot(player_loc_rot)
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

    def destroy_bullets(self):
        for bullet in self.player1.bullets:
            if (bullet.sprite_rect.x < 0
                    or bullet.sprite_rect.x > self.width
                    or bullet.sprite_rect.y < 0
                    or bullet.sprite_rect.y > self.height):
                self.player1.destroy_projectile(bullet)

    def compute_collisions(self):
        for bullet in self.player1.bullets:
            if bullet.sprite_rect.colliderect(self.player2.sprite_rect):
                self.player1.destroy_projectile(bullet)

    def send_data(self):
        data = f"{self.net.id}:{self.player1.sprite_rect.x},{self.player1.sprite_rect.y},{self.player1.rotation_angle};"
        data += self.bullet_data
        reply = self.net.send(data)
        self.bullet_data = ""
        return reply

    @staticmethod
    def parse_data(data):
        try:
            data = data.split(":")[1]
            object_data = data.split(";")
            player_data = object_data[0].split(",")
            bullets = []
            for bullet_data in object_data[1:]:
                if bullet_data != "":
                    bullet_data = bullet_data.split(",")
                    bullets.append(Bullet(start_pos=Vector2(int(bullet_data[0]), int(bullet_data[1])),
                                          heading=Vector2(float(bullet_data[2]), float(bullet_data[3]))))

            player_loc_rot = Vector3(int(player_data[0]), int(player_data[1]), float(player_data[2]))
            return player_loc_rot, bullets
        except:
            return None
