import pygame
import random
from enemy import Enemy

class Skeleton(Enemy):
    def __init__(self, name, position, window):
        super().__init__("assets/skeleton.png", position, window)
        self.name = name

    def move(self):
        super().move()

    def draw(self):
        super().draw()
