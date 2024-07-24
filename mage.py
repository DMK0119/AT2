import pygame
import math
from character import Character

class Mage(Character):
    def __init__(self, name, window, max_health):
        super().__init__(name, "Mage", armor=0, damage=30, hitpoints=100)
        self.window = window
        self.position = [self.window.get_width() / 2, self.window.get_height() / 2]
        self.orbs = []
        self.orbs_active = False
        self.orb_rotation_speed = 0.05  # Rotation speed for the orbs
        self.max_health = max_health
        self.current_health = max_health
        self.hit_cooldowns = {}  # Track cooldowns for enemies hit by orbs
        self.orb_damage = 50
        self.hit_cooldown_time = 60  # Cooldown time in frames
        self.orb_image = pygame.image.load('./assets/magic_orb.png').convert_alpha()
        self.orb_image = pygame.transform.scale(self.orb_image, (40, 40))  # Resize the orb image

    def damage(self):
        return self.getDamage()

    def getHealth(self):
        return self.__hit_points

    def init_orbs(self):
        # Create two orbs with initial angles and positions
        center = self.position
        return [
            {"angle": 0, "radius": 50, "damage": self.orb_damage, "position": (center[0] + 50, center[1])},
            {"angle": math.pi, "radius": 50, "damage": self.orb_damage, "position": (center[0] - 50, center[1])}
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
            if self.orbs_active:
                orb_position = (int(orb["position"][0] - self.orb_image.get_width() // 2),
                                int(orb["position"][1] - self.orb_image.get_height() // 2))
                self.window.blit(self.orb_image, orb_position)
            else:
                pygame.draw.circle(self.window, (128, 0, 128), (int(orb["position"][0]), int(orb["position"][1])), 20)

    def special_hit(self, enemies):
        if self.orbs_active:
            self.update_orbs()
            self.draw_orbs()
            self.check_orb_collisions(enemies)

    def check_orb_collisions(self, enemies):
        for orb in self.orbs:
            orb_rect = pygame.Rect(orb["position"][0] - 20, orb["position"][1] - 20, 40, 40)
            for enemy in enemies[:]:  # Use a slice to create a copy of the list for safe removal during iteration
                if self.can_hit(enemy):
                    enemy_rect = pygame.Rect(enemy.position[0], enemy.position[1], enemy.image.get_width(), enemy.image.get_height())
                    if orb_rect.colliderect(enemy_rect):
                        enemy.take_damage(orb["damage"])
                        self.hit_cooldowns[enemy] = pygame.time.get_ticks()  # Record the hit time
                        if enemy.getHealth() <= 0:  # Check if the enemy's health is 0 or less
                            enemies.remove(enemy)  # Remove the enemy from the list

    def can_hit(self, enemy):
        """Check if the enemy can be hit based on the cooldown."""
        now = pygame.time.get_ticks()
        if enemy in self.hit_cooldowns:
            last_hit_time = self.hit_cooldowns[enemy]
            if now - last_hit_time >= self.hit_cooldown_time * 1000 / 60:  # Convert frames to milliseconds
                return True
            else:
                return False
        return True

    def activate_orbs(self):
        if not self.orbs_active:
            self.orbs = self.init_orbs()
            self.orbs_active = True
            self.hit_cooldowns.clear()  # Clear the cooldowns when orbs are activated

    def deactivate_orbs(self):
        self.orbs_active = False
        self.orbs = []

    def reset_health(self):
        self.current_health = self.max_health

    def special_upgrade(self, effect):
        if effect == "Health +50":
            self.max_health += 50
            self.health = self.max_health
        elif effect == "Damage +20":
            self.player_attack_count = 0  # Reset player attack count to avoid instant special attack
            self.damage_bonus = 20
        elif effect == "Special Upgrade":
            self.orb_image = pygame.image.load('./assets/magic_orb2.png').convert_alpha()
            self.orb_image = pygame.transform.scale(self.orb_image, (40, 40))  # Resize the upgraded orb image
