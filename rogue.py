import pygame
import math
from character import Character

class Rogue(Character):
    def __init__(self, name, window):
        super().__init__(name, "Rogue", armor=0, hitpoints=200, damage=50)
        self.window = window

    def damage(self):
        return self.getDamage()

    def getHealth(self):
        return self.__hit_points
    