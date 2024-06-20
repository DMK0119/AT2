from character import Character
from rogue import Rogue
from skeleton import Skeleton
import random
import pygame
from assets import GAME_ASSETS
from enemy import Enemy
from mage import Mage



class Map:
    def __init__(self, window):
        """
        Initialize the Map class.

        Args:
            window (pygame.Surface): The game window surface.
            """
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
        self.enemies = [
            Enemy(GAME_ASSETS["goblin"], [50, 50], self.window),
            Enemy(GAME_ASSETS["orc"], [self.window.get_width() - 120, 50], self.window),
            Enemy(GAME_ASSETS["skeleton"], [50, self.window.get_height() - 120], self.window),
            Skeleton(GAME_ASSETS["skeleton"], [self.window.get_width() - 120, self.window.get_height() - 120], self.window),
        ]
        self.in_combat = False  # Ensure this attribute is defined in the constructor
        self.current_enemy = None
        self.blue_orb = None
        self.world = 0
        self.game_over = False      
        self.special_hit_active = False  
        self.clock = pygame.time.Clock()  # Pygame clock to manage time

        self.special_button_rect = pygame.Rect(50, 700, 250, 50)
        self.special_button_color = (0, 255, 0)
        self.special_button_cooldown = 600  # 10 seconds at 60 FPS
        self.special_button_timer = 0

        # Initialize font
        pygame.font.init()
        self.font = pygame.font.SysFont('Consolas', 30)

        '''self.window_width = self.window.get_width()
        self.window_height = self.window.get_height()
        
        self.boss_incoming_image = pygame.image.load("./assets/BossIncoming.png").convert_alpha()
        self.boss_incoming_image = pygame.transform.scale(self.boss_incoming_image, (self.window_width, self.window_height))
        
        self.boss_map_image = pygame.image.load("./assets/boss_map.jpeg").convert_alpha()
        self.boss_map_image = pygame.transform.scale(self.boss_map_image, (self.window_width, self.window_height))'''


    def load_player(self, character_type, name = 'Player'):
        """
        Load the player character.

        Args:
            character_type (str): The type of character to load.
        """
        self.player_type = character_type
        self.player_image = self.player_images[character_type]
        self.player_image = pygame.transform.scale(self.player_image, (int(self.player_image.get_width() * 0.15), int(self.player_image.get_height() * 0.15)))

        if character_type == 'Rogue':
            self.player = Rogue(name)
        if character_type == 'Mage':
            self.player = Mage(name, self.window)



    def check_for_combat(self):
        """
        Check if the player is in combat with any enemy.

        Returns:
            bool: True if the player is in combat, False otherwise.
        """
        for enemy in self.enemies:
            if pygame.math.Vector2(enemy.position).distance_to(self.player_position) < 50:
                self.in_combat = True
                self.current_enemy = enemy
                return True
        return False

    def health_bar(self):
        max_health = 100
        current_health = self.player.getHit_points()
        
        bar_length = 200  # Total length of the health bar
        bar_height = 20  # Height of the health bar
        
        health_ratio = current_health / max_health
        current_bar_length = bar_length * health_ratio
        
        red_colour = (255, 0, 0)
        green_colour = (0, 255, 0)
        white_colour = (255,255,255)
        pygame.draw.rect(self.window, white_colour, (100-5, 100-5, bar_length+10, bar_height+10))
        # Draw the red background bar (max health)
        pygame.draw.rect(self.window, red_colour, (100, 100, bar_length, bar_height))
        # Draw the green foreground bar (current health)
        pygame.draw.rect(self.window, green_colour, (100, 100, current_bar_length, bar_height))

    def handle_combat(self):
        """
        Handle combat between the player and the current enemy.
        """
        if self.in_combat and self.current_enemy:
            player_damage = random.randint(10, self.player.damage())
            enemy_defeated = self.current_enemy.take_damage(player_damage)
            print(f"Player attacks! Deals {player_damage} damage to the enemy.")
            if enemy_defeated:
                print("Enemy defeated!")
                self.enemies.remove(self.current_enemy)
                self.in_combat = False
                self.current_enemy = None
                if not self.enemies:
                    self.spawn_blue_orb()
            else:
                enemy_damage = random.randint(5, 10)
                self.player.take_damage(enemy_damage)
                remaining_health = self.player.getHit_points()
                print(f"Enemy attacks back! Deals {enemy_damage} damage to the player.")
                print(f"Player remaining health {remaining_health}")
                self.health_bar()
                # Assume player has a method to take damage
                # self.player.take_damage(enemy_damage)



    def handle_special_hit(self):
        if self.special_hit_active and isinstance(self.player, Mage):
            self.player.position = self.player_position  # Update the player's position
            self.player.special_hit(self.enemies)

    def spawn_blue_orb(self):
        """
        Spawn the blue orb in the center of the map.
        """
        self.blue_orb = pygame.image.load(GAME_ASSETS["blue_orb"]).convert_alpha()
        self.blue_orb = pygame.transform.scale(self.blue_orb, (50, 50))
        self.orb_position = [self.window.get_width() / 2 - 25, self.window.get_height() / 2 - 25]

    def check_orb_collision(self):
        """
        Check if the player has collided with the blue orb.

        Returns:
            bool: True if the player has collided with the blue orb, False otherwise.
        """
        if self.blue_orb and pygame.math.Vector2(self.orb_position).distance_to(self.player_position) < 25:
            print("YOU WIN")  # This can be modified to a more visual display if needed.
            return True
        return False

    def handle_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 'quit'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.special_button_rect.collidepoint(event.pos):
                    self.activate_special_hit()


        keys = pygame.key.get_pressed()
        move_speed = 2
        if keys[pygame.K_LEFT]:
            self.player_position[0] -= move_speed
        if keys[pygame.K_RIGHT]:
            self.player_position[0] += move_speed
        if keys[pygame.K_UP]:
            self.player_position[1] -= move_speed
        if keys[pygame.K_DOWN]:
            self.player_position[1] += move_speed
        if keys[pygame.K_SPACE]:
            self.activate_special_hit()



        if not self.in_combat:
            if self.check_for_combat():
                return
        self.handle_combat()
        self.handle_special_hit()

        if self.blue_orb and self.check_orb_collision():
            print("BOSS INCOMING")
            
        '''self.window.blit(self.boss_incoming_image, (0, 0))
            pygame.display.flip()
            pygame.time.wait(5000) # Display for 5 seconds
            
            self.window.blit(self.boss_map_image, (0, 0))
            pygame.display.flip()
            self.blue_orb = None ''' # Optionally reset the orb to prevent repeated calls
        
        
    def activate_special_hit(self):
        if self.special_button_cooldown == 0:
            self.special_hit_active = True
            if isinstance(self.player, Mage):
                self.player.activate_orbs()
            self.special_button_cooldown = 600  # 10 seconds at 60 FPS

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

    def draw_special_button(self):
        pygame.draw.rect(self.window, self.special_button_color, self.special_button_rect)

        if self.special_button_cooldown > 0:
            text = str(self.special_button_timer).rjust(3)
        else:
            text = 'Special Ready'

        text_surface = self.font.render(text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.special_button_rect.center)
        self.window.blit(text_surface, text_rect)

    def draw(self):
        self.window.fill((0, 0, 0))
        self.window.blit(self.map_image, (0, 0))
        self.window.blit(self.player_image, (self.player_position[0], self.player_position[1]))
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
        pygame.display.flip()
