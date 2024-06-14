import pygame
import random

class Enemy:
    def __init__(self,image_path, position, window):
        # Load the enemy image from the specified image path
        self.image = pygame.image.load(image_path).convert_alpha()
        # Scale the enemy image to 0.75 times the original size
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.75), int(self.image.get_height() * 0.75)))
        # Set the initial position of the enemy
        self.position = position
        # Set the window where the enemy will be drawn
        self.window = window
        # Set the initial health of the enemy to 100
        self.health = 100
        self.target_position = self.get_new_target_position()

    def take_damage(self, damage):
        # Reduce the enemy's health by the specified damage amount
        self.health -= damage
        return self.health <= 0
        # Return True if the enemy's health is less than or equal to 0, indicating that it is defeated

    def draw_health_bar(self):
        max_health = 100
        bar_length = self.image.get_width()
        bar_height = 5
        health_ratio = self.health / max_health
        current_bar_length = bar_length * health_ratio

        red_colour = (255, 0, 0)
        green_colour = (0, 255, 0)

        health_bar_position = (self.position[0], self.position[1] - bar_height - 2)
        pygame.draw.rect(self.window, red_colour, (health_bar_position[0], health_bar_position[1], bar_length, bar_height))
        pygame.draw.rect(self.window, green_colour, (health_bar_position[0], health_bar_position[1], current_bar_length, bar_height))

    def draw(self):
        adjusted_position = [
            max(0, min(self.window.get_width() - self.image.get_width(), self.position[0])),
            max(0, min(self.window.get_height() - self.image.get_height(), self.position[1]))
        ]
        self.window.blit(self.image, adjusted_position)
        self.draw_health_bar()



    def get_new_target_position(self):
        max_x = self.window.get_width() - self.image.get_width()
        max_y = self.window.get_height() - self.image.get_height()
        return [random.randint(0, max_x), random.randint(0, max_y)]

    def move(self):
        speed = 1  # Adjust the speed of the enemy movement

        # Calculate the direction vector towards the target position
        direction_x = self.target_position[0] - self.position[0]
        direction_y = self.target_position[1] - self.position[1]

        # Calculate the distance to the target position
        distance = (direction_x ** 2 + direction_y ** 2) ** 0.5

        # If the enemy is close to the target, get a new target position
        if distance < speed:
            self.target_position = self.get_new_target_position()
        else:
            # Normalize the direction vector and move the enemy
            direction_x /= distance
            direction_y /= distance
            self.position[0] += direction_x * speed
            self.position[1] += direction_y * speed