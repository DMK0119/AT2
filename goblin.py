import pygame
import random
from enemy import Enemy

class Goblin(Enemy):
    def __init__(self, name, position, window):
        super().__init__("assets/goblin.png", position, window)
        self.name = name

    def move(self):
        # Move the goblin randomly within a specified range
        super().move()

    def draw(self):
        # Draw the goblin on the game window
        super().draw()
