import pygame
import math
from character import Character

class Mage(Character):
    def __init__(self, name, window):
        super().__init__(name, "Mage", armor=0, hitpoints=100, damage=30)
        self.window = window
        self.position = [self.window.get_width() / 2, self.window.get_height() / 2]
        self.orbs = []
        self.orbs_active = False
        self.orb_rotation_speed = 0.01  # Rotation speed for the orbs

    def damage(self):
        return self.getDamage()

    def getHealth(self):
        return self.__hit_points

    def init_orbs(self):
        # Create two orbs with initial angles and positions
        center = self.position
        return [
            {"angle": 0, "radius": 50, "damage": 10, "position": (center[0] + 50, center[1])},
            {"angle": math.pi, "radius": 50, "damage": 10, "position": (center[0] - 50, center[1])}
        ]

    def update_orbs(self):
        for orb in self.orbs:
            orb["angle"] += self.orb_rotation_speed
            orb["position"] = (
                self.position[0] + orb["radius"] * math.cos(orb["angle"]),
                self.position[1] + orb["radius"] * math.sin(orb["angle"])
            )

    def draw_orbs(self):
        for orb in self.orbs:
            pygame.draw.circle(self.window, (128, 0, 128), (int(orb["position"][0]), int(orb["position"][1])), 20)

    def special_hit(self, enemies):
        if self.orbs_active:
            self.update_orbs()
            self.draw_orbs()
            self.check_orb_collisions(enemies)

    def check_orb_collisions(self, enemies):
        for orb in self.orbs:
            orb_rect = pygame.Rect(orb["position"][0] - 20, orb["position"][1] - 20, 40, 40)
            for enemy in enemies:
                enemy_rect = pygame.Rect(enemy.position[0], enemy.position[1], enemy.image.get_width(), enemy.image.get_height())
                if orb_rect.colliderect(enemy_rect):
                    enemy.take_damage(orb["damage"])

    def activate_orbs(self):
        if not self.orbs_active:
            self.orbs = self.init_orbs()
            self.orbs_active = True

    def deactivate_orbs(self):
        self.orbs_active = False
        self.orbs = []
