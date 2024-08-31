import math
import pygame
from config import WIDTH, HEIGHT, CAR_SIZE_X, CAR_SIZE_Y, BORDER_COLOR


class Car:
    # 830 920
    def __init__(self, start_position=(580, 755)):
        """
        Initialize a car object.

        :param start_position: Starting position of the car (x, y)
        """
        self.sprite = self._load_sprite()
        self.position = list(start_position)
        self.angle = 0
        self.speed = 0
        self.speed_set = False
        self.center = self._calculate_center()
        self.radars = []
        self.drawing_radars = []
        self.alive = True
        self.distance = 0
        self.time = 0

    def _load_sprite(self):
        """Load and scale the car sprite."""
        sprite = pygame.image.load("car.png").convert()
        return pygame.transform.scale(sprite, (CAR_SIZE_X, CAR_SIZE_Y))

    def _calculate_center(self):
        """Calculate the center of the car."""
        return [
            self.position[0] + CAR_SIZE_X / 2,
            self.position[1] + CAR_SIZE_Y / 2,
        ]

    def draw(self, screen):
        """Draw the car on the screen."""
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        screen.blit(rotated_sprite, self.position)
        self._draw_radars(screen)

    def _draw_radars(self, screen):
        """Draw the radars/sensors of the car."""
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)

    def check_collision(self, game_map):
        """Check if the car has collided with the border."""
        self.alive = True
        for point in self._get_corners():
            if game_map.get_at((int(point[0]), int(point[1]))) == BORDER_COLOR:
                self.alive = False
                break

    def _get_corners(self):
        """Calculate the four corners of the car."""
        length = 0.5 * CAR_SIZE_X
        cos = math.cos(math.radians(360 - self.angle))
        sin = math.sin(math.radians(360 - self.angle))

        corners = [
            (self.center[0] + cos * length, self.center[1] + sin * length),
            (self.center[0] - sin * length, self.center[1] + cos * length),
            (self.center[0] - cos * length, self.center[1] - sin * length),
            (self.center[0] + sin * length, self.center[1] - cos * length),
        ]
        return corners

    def check_radar(self, degree, game_map):
        """
        Check the distance from the car to the border for a given angle.

        :param degree: The angle to check
        :param game_map: The game map surface
        """
        length = 0
        x = int(
            self.center[0]
            + math.cos(math.radians(360 - (self.angle + degree))) * length
        )
        y = int(
            self.center[1]
            + math.sin(math.radians(360 - (self.angle + degree))) * length
        )

        while not game_map.get_at((x, y)) == BORDER_COLOR and length < 300:
            length += 1
            x = int(
                self.center[0]
                + math.cos(math.radians(360 - (self.angle + degree))) * length
            )
            y = int(
                self.center[1]
                + math.sin(math.radians(360 - (self.angle + degree))) * length
            )

        dist = int(
            math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2))
        )
        self.radars.append([(x, y), dist])

    def update(self, game_map):
        """Update the car's position and status."""
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        self._move()
        self._update_distance()
        self._update_center()
        self.check_collision(game_map)
        self._update_radars(game_map)

    def _move(self):
        """Move the car based on its current angle and speed."""
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        self.position[0] = max(min(self.position[0], WIDTH - 120), 20)
        self.position[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        self.position[1] = max(min(self.position[1], HEIGHT - 120), 20)

    def _update_distance(self):
        """Update the distance traveled and time passed."""
        self.distance += self.speed
        self.time += 1

    def _update_center(self):
        """Recalculate the center of the car."""
        self.center = self._calculate_center()

    def _update_radars(self, game_map):
        """Update all radar/sensor readings."""
        self.radars.clear()
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map)

    def get_data(self):
        """Get the car's sensor data."""
        radars = self.radars
        return [min(int(radar[1] / 30), 10) for radar in radars]

    def is_alive(self):
        """Check if the car is still alive."""
        return self.alive

    def get_reward(self):
        """Calculate the reward for the car's progress."""
        return self.distance / (CAR_SIZE_X / 2)
