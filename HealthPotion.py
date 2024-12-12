#Author' name:- Rishi Patel
#Description:- The program defines the class health potion which basically is used to display the helth of snakes

import pygame
import sys
from pygame.locals import *
from random import randint
import time


# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1200, 900
FPS = 30
SNAKE_SIZE = 20
BUTTON_WIDTH, BUTTON_HEIGHT = 100, 50
POTION_RADIUS = 10
POTION_SPAWN_INTERVAL = 20  # seconds

# Directions
RIGHT = {'x': 1, 'y': 0}
LEFT = {'x': -1, 'y': 0}
UP = {'x': 0, 'y': -1}
DOWN = {'x': 0, 'y': 1}

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
PINK = (255, 192, 203)
GOLDEN_YELLOW = (255, 223, 0)
RED_ORANGE = (255, 69, 0)
LEMON_GREEN = (173, 255, 47)
GOLDEN_BOUNDARY = (255, 215, 0)

class HealthPotion:
    """
    Class which defines health potion of the snake
    """
    def __init__(self):
        self.position = self.spawn()

    @staticmethod
    def spawn():
        x = randint(0, WINDOW_WIDTH // SNAKE_SIZE - 1)
        y = randint(0, WINDOW_HEIGHT // SNAKE_SIZE - 1)
        return {'x': x, 'y': y}

    def draw(self, window):
        pygame.draw.circle(
            window,
            PINK,
            (self.position['x'] * SNAKE_SIZE + SNAKE_SIZE // 2, self.position['y'] * SNAKE_SIZE + SNAKE_SIZE // 2),
            POTION_RADIUS,
        )
