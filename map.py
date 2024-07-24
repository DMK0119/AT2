import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from rogue import Rogue
from warrior import Warrior
from skeleton import Skeleton
from mage import Mage
import sys

class Map:
    def __init__(self, window):
        self.window = window
        self.map_image = pygame.image.load(GAME_ASSETS["dungeon_map"]).convert_alpha()
        self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))
        self.player_images = {
            'Warrior': pygame.image.load(GAME_ASSETS['warrior']).convert_alpha(),
            'Mage': pygame.image.load(GAME_ASSETS['mage']).convert_alpha(),
            'Rogue': pygame.image.load(GAME_ASSETS["rogue"]).convert_alpha()
        }
        self.player_type = None
        self.player_position = [self.window.get_width() / 2, self.window.get_height() / 2]

        # Create enemies with image paths
        self.enemies = [
            Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
            Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
            Skeleton(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window),
        ]


        self.game_over_image = pygame.image.load("./assets/game_over.jpeg").convert_alpha()  # Load game over image
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.window.get_width(), self.window.get_height()))

        self.in_combat = False
        self.current_enemy = None
        self.blue_orb = None
        self.world = 0
        self.game_over = False
        self.special_hit_active = False
        self.clock = pygame.time.Clock()

        self.special_button_rect = pygame.Rect(50, 700, 250, 50)
        self.special_button_color = (0, 255, 0)
        self.special_button_cooldown = 600  # 10 seconds at 60 FPS
        self.special_button_timer = 0

        self.round = 0

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.SysFont('Consolas', 30)

        # Define max_health for each character type
        self.max_health = {
            'Warrior': 200,
            'Mage': 100,
            'Rogue': 150
        }

    def load_player(self, character_type, name='Player'):
        self.player_type = character_type
        self.player_image = self.player_images.get(character_type)
        if self.player_image:
            self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.15), int(self.player_image.get_height() * 0.15)))
            if character_type == 'Rogue':
                self.player = Rogue(name, self.window, self.max_health[character_type])
            elif character_type == 'Mage':
                self.player = Mage(name, self.window, self.max_health[character_type])
            elif character_type == 'Warrior':
                self.player = Warrior(name, self.window, self.max_health[character_type])
        else:
            raise ValueError(f"Invalid character type: {character_type}. Cannot load player.")
        
    def next_round(self):
        self.round += 1
        if self.round == 1:
            self.map_image = pygame.image.load('./assets/level2.png').convert()
            self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))  # Adjust size as needed
        elif self.round == 2:
            self.map_image = pygame.image.load('./assets/level3.png').convert()
            self.map_image = pygame.transform.scale(self.map_image, (self.window.get_width(), self.window.get_height()))  # Adjust size as needed

        
    def reset_player_health(self):
        """
        Reset the player's health to its maximum value based on character type.
        """
        if isinstance(self.player, Warrior):
            self.player.reset_health()  # Reset health for Warrior class
        elif isinstance(self.player, Mage):
            self.player.reset_health()  # Reset health for Mage class
        elif isinstance(self.player, Rogue):
            self.player.reset_health()  # Reset health for Rogue class

    def reset_game(self, round):
        """
        Reset the game state and add more enemies based on the current round.
        """
        self.player_position = [self.window.get_width() / 2, self.window.get_height() / 2]
        
        # Base enemies plus additional ones for each round
        self.enemies = [
            Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
            Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
            Skeleton(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window)
        ]

        # Add more enemies based on the round
        for _ in range(round):  # Use self.round instead of 'round'
            self.enemies.append(
                Enemy(GAME_ASSETS["goblin"], [random.randint(50, self.window.get_width() - 150), random.randint(50, self.window.get_height() - 150)], self.window)
            )
            self.enemies.append(
                Enemy(GAME_ASSETS["orc"], [random.randint(50, self.window.get_width() - 150), random.randint(50, self.window.get_height() - 150)], self.window)
            )

        self.in_combat = False
        self.current_enemy = None
        self.blue_orb = None
        self.game_over = False
        self.special_hit_active = False
        self.clock = pygame.time.Clock()

        self.special_button_rect = pygame.Rect(50, 700, 250, 50)
        self.special_button_color = (0, 255, 0)
        self.special_button_cooldown = 600  # 10 seconds at 60 FPS
        self.special_button_timer = 0

        if self.player_type:
            self.load_player(self.player_type)  # Load player without resetting health
            self.state = 'game_map'  # Change the state back to 'game_map'

    def check_for_combat(self):
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False

    def health_bar(self):
        if isinstance(self.player, Warrior):
            max_health = self.max_health['Warrior']
            character_name = "Warrior"
        elif isinstance(self.player, Mage):
            max_health = self.max_health['Mage']
            character_name = "Mage"
        elif isinstance(self.player, Rogue):
            max_health = self.max_health['Rogue']
            character_name = "Rogue"
        else:
            return

        current_health = self.player.getHit_points()

        bar_length = 200
        bar_height = 20

        if current_health < 0:
            current_health = 0
        elif current_health > max_health:
            current_health = max_health

        health_ratio = current_health / max_health
        current_bar_length = bar_length * health_ratio

        red_colour = (255, 0, 0)
        green_colour = (0, 255, 0)
        white_colour = (255, 255, 255)

        pygame.draw.rect(self.window, white_colour, (100 - 5, 100 - 5, bar_length + 10, bar_height + 10))
        pygame.draw.rect(self.window, red_colour, (100, 100, bar_length, bar_height))
        pygame.draw.rect(self.window, green_colour, (100, 100, current_bar_length, bar_height))

        health_text = self.font.render(f"{current_health}/{max_health}", True, (255, 255, 255))
        self.window.blit(health_text, (100 + bar_length + 15, 100))

        name_text = self.font.render(character_name, True, (255, 255, 255))
        name_text_rect = name_text.get_rect(center=(100 + bar_length // 2, 100 - 30))
        self.window.blit(name_text, name_text_rect)


    def handle_combat(self):
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(10, self.player.getDamage())
            enemy_defeated = self.current_enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")

            if enemy_defeated:
                print("Enemy defeated!")
                if self.current_enemy in self.enemies:
                    self.enemies.remove(self.current_enemy)
                self.in_combat = False
                self.current_enemy = None

                # Check if all enemies are defeated
                if not self.enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(5, 10)
                self.player.take_damage(enemy_damage)
                remaining_health = self.player.getHit_points()
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                print(f"Player remaining health {remaining_health}")
                self.health_bar()

                # Optionally handle player death or game over condition here

            if self.player.getHit_points() <= 0:
                self.player.setHit_points(0)  # Ensure hit points don't go negative
                self.game_over = True
                self.display_game_over()
                return 'game_over'


    def handle_special_hit(self):
        if self.special_hit_active:
            if isinstance(self.player, Mage):
                self.player.position = self.player_position
                self.player.special_hit(self.enemies)
                if not self.enemies:  # Check if enemies list is empty after special hit
                    self.spawn_blue_orb()
            elif isinstance(self.player, Warrior):
                self.player.position = self.player_position
                self.player.activate_shield()



    def spawn_blue_orb(self):
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            print("YOU WIN")
            return True
        return False
    


    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_rect = self.game_over_button()
                if (button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and
                        button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]):
                    return 'game_over'

        keys = pygame.key.get_pressed()
        move_speed = 5

        new_x = self.player_position[0]
        new_y = self.player_position[1]

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            new_x -= move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            new_x += move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            new_y -= move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            new_y += move_speed

        player_width, player_height = self.player_image.get_width(), self.player_image.get_height()
        window_width, window_height = self.window.get_width(), self.window.get_height()

        if new_x < 0:
            new_x = 0
        elif new_x > window_width - player_width:
            new_x = window_width - player_width

        if new_y < 0:
            new_y = 0
        elif new_y > window_height - player_height:
            new_y = window_height - player_height

        self.player_position = [new_x, new_y]

        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()
        self.handle_special_hit()

        if self.blue_orb and self.check_orb_collision():
            print("BOSS INCOMING")
            self.reset_game(self.round)  # Reset game when blue orb is collected
            self.next_round()
            return 'Level2'

        return None

    def activate_special_hit(self):
        if self.special_button_cooldown == 0:
            self.special_hit_active = True
            if isinstance(self.player, Mage):
                self.player.activate_orbs()
            elif isinstance(self.player, Warrior):
                self.player.activate_shield()
            self.special_button_cooldown = 600


    def update_special_button(self):
        if self.special_button_cooldown > 0:
            self.special_button_cooldown -= 1
            self.special_button_timer = self.special_button_cooldown // 60
            cooldown_ratio = self.special_button_cooldown / 600
            red_value = int(255 * cooldown_ratio)
            green_value = int(255 * (1 - cooldown_ratio))
            self.special_button_color = (red_value, green_value, 0)
        else:
            self.special_button_color = (0, 255, 0)
            self.special_hit_active = True
            if isinstance(self.player, Mage):
                self.player.activate_orbs()
            elif isinstance(self.player, Warrior):
                self.player.activate_shield()


    def draw_special_button(self):
        pygame.draw.rect(self.window, self.special_button_color, self.special_button_rect)

        if self.special_button_cooldown > 0:
            text = str(self.special_button_timer).rjust(3)
        else:
            text = 'Special Ready'

        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.special_button_rect.center)
        self.window.blit(text_surface, text_rect)
    

    def display_game_over(self):
        self.window.blit(self.game_over_image, (0, 0))
        button_rect = self.game_over_button()  # Get button coordinates
        pygame.display.flip()

        while True:  # Loop to wait for the player to click the button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return 'quit'
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if (button_rect[0] <= mouse_pos[0] <= button_rect[0] + button_rect[2] and
                            button_rect[1] <= mouse_pos[1] <= button_rect[1] + button_rect[3]):
                        return 'main_menu'  # Break the loop and return to main menu


    def game_over_button(self):
        button_width = 270
        button_height = 60
        button_x = (self.window.get_width() - button_width) // 2
        button_y = self.window.get_height() - button_height - 50

        pygame.draw.rect(self.window, (255, 255, 255), (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.window, (0, 0, 0), (button_x, button_y, button_width, button_height), 2)
        text = self.font.render("Quit Game", True, (0, 0, 0))  # Change the button text to "Quit Game"
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.window.blit(text, text_rect)
        pygame.display.flip()

        return (button_x, button_y, button_width, button_height)
    
    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        
        # Draw the shield if active
        if isinstance(self.player, Warrior) and self.player.shield_active:
            shield_rect = self.player.shield_image.get_rect(center=(self.player_position[0], self.player_position[1]))
            self.window.blit(self.player.shield_image, shield_rect)
        
        # Draw the player character
        player_rect = self.player_image.get_rect(center=(self.player_position[0], self.player_position[1]))
        self.window.blit(self.player_image, player_rect)
        
        for enemy in self.enemies:
            enemy.move()
            enemy.draw()
        
        self.health_bar()
        
        if self.blue_orb:
            self.window.blit(self.blue_orb, self.orb_position)
        
        if self.special_hit_active:
            self.handle_special_hit()
        
        self.update_special_button()
        self.draw_special_button()
        
        # Draw the level header
        level_text = f"Level: {self.round + 1}"
        level_surface = self.font.render(level_text, True, (255, 255, 255))
        level_rect = level_surface.get_rect(center=(self.window.get_width() / 2, 30))
        self.window.blit(level_surface, level_rect)
        
        pygame.display.flip()


