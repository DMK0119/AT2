import pygame
import random
from enemy import Enemy

class Orc(Enemy):
    def __init__(self, name, position, window):
        # Load the orc image from the specified path
        super().__init__("assets/orc.png", position, window)
        self.name = name

    def move(self):
        # Move the orc randomly within a specified range
        super().move()

    def draw(self):
        # Draw the orc on the window at its current position
        super().draw()
