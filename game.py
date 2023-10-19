import math

import pygame

from Canvas import Canvas
from Player import Player
from network import Network


def get_angle(tank_position, mouse_position):
    x_diff = mouse_position[0] - tank_position[0]
    y_diff = mouse_position[1] - tank_position[1]
    return math.atan2(y_diff, x_diff)


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.player = Player(50, 100)
        self.player2 = Player(self.width - 50, 100)
        self.canvas = Canvas(self.width, self.height, "Tank2D")

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

            if keys[pygame.K_d]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_a]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_w]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_s]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)

            mouse_position = pygame.mouse.get_pos()
            angle = get_angle(self.player.sprite_rect.center, mouse_position)
            self.player.rotate(-angle)  # Note: the negative sign is used to rotate in the correct direction.

            # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.canvas.update()

        pygame.quit()

    def send_data(self):
        """
        Send position and rotation to server
        :return: None
        """
        # Assuming you've added a get_rotation() method to the Player class
        rotation = self.player.get_rotation()
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y) + "," + str(rotation)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0, 0
