import pygame
import math
from character import Character

class Warrior(Character):
    def __init__(self, name, window):
        super().__init__(name, "Warrior", armor=0, hitpoints=200, damage=100)
        self.window = window
        self.position = [self.window.get_width() / 2, self.window.get_height() / 2]

    def damage(self):
        return self.getDamage()

    def getHealth(self):
        return self.__hit_points