import pygame
import math
from character import Character

class Warrior(Character):
    def __init__(self, name, window, max_health):
        super().__init__(name, "Warrior", armor=0, damage=100, hitpoints=200)
        self.window = window
        self.position = [self.window.get_width() / 2, self.window.get_height() / 2]
        self.max_health = max_health
        self.shield_image = pygame.image.load('./assets/shield.png')
        self.shield_image = pygame.transform.scale(self.shield_image, (self.shield_image.get_width()//7, self.shield_image.get_height()//7))
        self.shield_active = False
        self.shield_duration = 5000  # Duration the shield is active in milliseconds
        self.shield_cooldown = 10000  # Cooldown time in milliseconds
        self.shield_timer = 0

    def damage(self):
        return self.getDamage()

    def getHealth(self):
        return self.getHit_points()  # Adjusted to match the method name in Character class

    def reset_health(self):
        self.current_health = self.max_health

    def activate_shield(self):
        if not self.shield_active and self.shield_timer <= 0:
            self.shield_active = True
            self.shield_timer = self.shield_duration
            print(f"{self.getName()} activated shield!")

    def update(self, delta_time):
        # Update shield timer
        if self.shield_active:
            self.shield_timer -= delta_time
            if self.shield_timer <= 0:
                self.shield_active = False
                self.shield_timer = self.shield_cooldown
                print(f"{self.getName()}'s shield is now on cooldown.")
        else:
            self.shield_timer -= delta_time

    def draw(self):
        if self.shield_active:
            shield_rect = self.shield_image.get_rect(center=(self.position[0], self.position[1]))
            self.window.blit(self.shield_image, shield_rect)

        # Draw warrior (placeholder for warrior drawing logic)
        pygame.draw.circle(self.window, (255, 0, 0), (int(self.position[0]), int(self.position[1])), 50)
