import pygame
import random
from mage import Mage
from character import Character

class TurnBase:
    def __init__(self, window, character_type):
        self.window = window
        self.window_width = self.window.get_width()
        self.window_height = self.window.get_height()
        self.header_height = self.window_height // 6
        self.footer_height = self.window_height // 5  # Footer banner height
        self.map_level2 = None
        self.boss_incoming_image = pygame.image.load("./assets/BossIncoming.png").convert_alpha()
        self.boss_incoming_image = pygame.transform.scale(self.boss_incoming_image, (self.window.get_width(), self.window.get_height()))
        self.enemy_image = pygame.image.load("./assets/level2_enemy.png").convert_alpha()
        self.enemy_image = pygame.transform.scale(self.enemy_image, (self.enemy_image.get_width()//1.5, self.enemy_image.get_height()//1.5))
        self.footer = pygame.image.load("./assets/level2_footer.png").convert_alpha()
        self.footer = pygame.transform.scale(self.footer, (self.window_width, 200))
        self.game_over_image = pygame.image.load("./assets/game_over.jpeg").convert_alpha()  # Load game over image
        self.game_over_image = pygame.transform.scale(self.game_over_image, (self.window_width, self.window_height))

        # Load level up background image
        self.level_up_background = pygame.image.load("./assets/level_up_background.png").convert_alpha()
        self.level_up_background = pygame.transform.scale(self.level_up_background, (self.window_width, self.window_height))

        self.next_level_image = pygame.image.load("./assets/next_level.png").convert_alpha()
        self.next_level_image = pygame.transform.scale(self.next_level_image, (self.window_width, self.window_height))

        self.level_up_image = pygame.image.load("./assets/level_up.png").convert_alpha()

        self.character_type = character_type
        if character_type == "Mage":
            self.player_image = pygame.image.load("./assets/wizard_character.png").convert_alpha()
            self.max_health = 100
        elif character_type == "Warrior":
            self.player_image = pygame.image.load("./assets/warrior_character.png").convert_alpha()
            self.max_health = 200
        elif character_type == "Rogue":
            self.player_image = pygame.image.load("./assets/rogue_character.png").convert_alpha()
            self.max_health = 150

        self.player_image = pygame.transform.scale(self.player_image, (self.player_image.get_width()//1.5, self.player_image.get_height()//1.5))

        
        # Load shield image
        self.shield_image = pygame.image.load("./assets/shield.png").convert_alpha()
        self.shield_image = pygame.transform.scale(self.shield_image, (self.player_image.get_width(), self.player_image.get_height()))

        self.health = 100
        self.enemy_health = 100
        self.enemy_special_counter = 0  # Counter for enemy special attack
        self.player_attack_count = 0  # Counter for player attacks
        self.font = pygame.font.Font(None, 48)  # Increased font size
        self.small_font = pygame.font.Font(None, 32)  # Smaller font size for special text
        self.turn = "player"  # Keep track of whose turn it is
        self.action_text = ""  # Text to display the current action
        self.shield_active = False  # Shield state

        self.round = 0
    
    def reset(self):
        self.health = self.max_health
        self.enemy_health = 100
        self.enemy_special_counter = 0
        self.player_attack_count = 0
        self.turn = "player"
        self.action_text = ""
        self.shield_active = False
        self.round += 1
        print(self.round)

    def next_round(self):
        if self.round == 1:
            self.map_level2 = pygame.image.load('./assets/boss_map.jpeg').convert_alpha()
            self.map_level2 = pygame.transform.scale(self.map_level2, (self.window.get_width(), self.window.get_height()))
        elif self.round == 2:
            self.map_level2 = pygame.image.load('./assets/level2.png').convert_alpha()
            self.map_level2 = pygame.transform.scale(self.map_level2, (self.window.get_width(), self.window.get_height()))
            self.enemy_image = pygame.image.load("./assets/boss2.png").convert_alpha()
            self.enemy_image = pygame.transform.scale(self.enemy_image, (self.enemy_image.get_width(), self.enemy_image.get_height()))
        elif self.round == 3:
            self.map_level2 = pygame.image.load('./assets/level3.png').convert_alpha()
            self.map_level2 = pygame.transform.scale(self.map_level2, (self.window.get_width(), self.window.get_height()))
            self.enemy_image = pygame.image.load("./assets/boss3.png").convert_alpha()
            self.enemy_image = pygame.transform.scale(self.enemy_image, (self.enemy_image.get_width()//1.5, self.enemy_image.get_height()//1.5))


    def draw_health_bar(self, x, y, health, max_health, character_name, bar_color):
        bar_width = 300
        bar_height = 40

        # Calculate health bar fill
        fill_width = (health / max_health) * bar_width

        # Background bar
        pygame.draw.rect(self.window, (255, 0, 0), (x, y, bar_width, bar_height))

        # Health fill
        pygame.draw.rect(self.window, bar_color, (x, y, fill_width, bar_height))

        # Draw the border for the health bar
        pygame.draw.rect(self.window, (0, 0, 0), (x, y, bar_width, bar_height), 3)

        # Render the character's name
        text = self.font.render(character_name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(x + bar_width // 2, y - 30))
        self.window.blit(text, text_rect)

        # Render the health text
        health_text = self.font.render(f"{health}/{max_health}", True, (0, 0, 0))
        health_text_rect = health_text.get_rect(center=(x + bar_width // 2, y + bar_height // 2))
        self.window.blit(health_text, health_text_rect)


    def draw_action_buttons(self):
        button_width = 150
        button_height = 50
        spacing = 20
        total_width = 4 * button_width + 3 * spacing
        start_x = (self.window_width - total_width) // 2
        start_y = self.window_height - self.footer_height + (self.footer_height - button_height) // 2

        buttons = ["Heal", "Attack", "Special", "Shield"]
        for i, button in enumerate(buttons):
            x = start_x + i * (button_width + spacing)
            y = start_y
            if button == "Special":
                if self.player_attack_count < 3:
                    color = (100, 100, 100)  # Dim grey
                    pygame.draw.rect(self.window, color, (x, y, button_width, button_height))
                    # Fill bar by 1/3 for each attack
                    fill_width = (self.player_attack_count / 3) * button_width
                    pygame.draw.rect(self.window, (0, 255, 0), (x, y, fill_width, button_height))
                else:
                    color = (0, 255, 0)  # Green
                    pygame.draw.rect(self.window, color, (x, y, button_width, button_height))
            else:
                color = (255, 255, 255)  # White
                pygame.draw.rect(self.window, color, (x, y, button_width, button_height))

            pygame.draw.rect(self.window, (0, 0, 0), (x, y, button_width, button_height), 2)  # Border

            text = self.font.render(button, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + button_width // 2, y + button_height // 2))
            self.window.blit(text, text_rect)

        return [(start_x + i * (button_width + spacing), start_y, button_width, button_height) for i in range(4)]

    def draw_enemy_special_bar(self, x, y, counter, max_count):
        bar_width = 30
        bar_height = 100

        # Calculate special bar fill
        fill_height = (counter / max_count) * bar_height

        # Background bar
        pygame.draw.rect(self.window, (255, 0, 0), (x, y, bar_width, bar_height))

        # Special fill
        pygame.draw.rect(self.window, (255, 255, 0), (x, y + bar_height - fill_height, bar_width, fill_height))

        # Draw the border for the special bar
        pygame.draw.rect(self.window, (0, 0, 0), (x, y, bar_width, bar_height), 3)

        special_text = self.small_font.render("Special", True, (255, 255, 255))
        special_text_rect = special_text.get_rect(center=(x + bar_width // 2, y - 20))
        self.window.blit(special_text, special_text_rect)

    def handle_player_action(self, action):
        if action == "Heal":
            self.health = min(self.max_health, self.health + 15)
        elif action == "Attack":
            self.enemy_health = max(0, self.enemy_health - 20)
            self.player_attack_count = min(3, self.player_attack_count + 1)  # Increment attack count
        elif action == "Special" and self.player_attack_count >= 3:
            self.enemy_health = max(0, self.enemy_health - 40)
            self.player_attack_count = 0  # Reset the attack count after using Special
        elif action == "Shield":
            self.shield_active = True  # Activate shield

        # Redraw the health bars after the player's action
        self.redraw_health_bars()

    def handle_enemy_action(self):
        action = random.choice(["Heal", "Attack", "Special"])
        if action == "Heal":
            self.enemy_health = min(100, self.enemy_health + 10)
            self.action_text = "Enemy turn: Heal - gains 10 health"
        elif action == "Attack":
            damage = 30 if self.enemy_special_counter < 5 else 20
            if self.shield_active:
                damage = max(0, damage - 10)  # Reduce damage if shield is active
                self.shield_active = False  # Deactivate shield after absorbing damage
            self.health = max(0, self.health - damage)
            self.enemy_special_counter = (self.enemy_special_counter + 1) % 5
            self.action_text = f"Enemy turn: Attack - deals {damage} damage"
        elif action == "Special":
            if self.enemy_special_counter == 0:
                damage = 50
                if self.shield_active:
                    damage = max(0, damage - 10)  # Reduce damage if shield is active
                    self.shield_active = False  # Deactivate shield after absorbing damage
                self.health = max(0, self.health - damage)
                self.action_text = f"Enemy turn: Special - deals {damage} damage"
            else:
                self.handle_enemy_action() 

        # Redraw the health bars after the enemy's action
        self.redraw_health_bars()

        self.window.blit(self.footer, (0, self.window_height - self.footer.get_height() * 0.9))
        turn_text = self.font.render(self.action_text, True, (255, 255, 255))
        turn_text_rect = turn_text.get_rect(center=(self.window_width // 2, self.window_height - self.footer_height // 1.2))
        self.window.blit(turn_text, turn_text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait for 2 seconds to show enemy action text


    def redraw_health_bars(self):
        self.draw_health_bar(50, self.header_height // 2, self.health, self.max_health, self.character_type, (0, 255, 0))
        self.draw_health_bar(self.window_width - 350, self.header_height // 2, self.enemy_health, 100, "Enemy", (255, 255, 0))


    def display_game_over(self):
        self.window.blit(self.game_over_image, (0, 0))
        button_width = 270
        button_height = 60
        button_x = (self.window_width - button_width) // 2
        button_y = self.window_height - button_height - 50

        pygame.draw.rect(self.window, (255, 255, 255), (button_x, button_y, button_width, button_height))
        pygame.draw.rect(self.window, (0, 0, 0), (button_x, button_y, button_width, button_height), 2)
        text = self.font.render("Restart Round", True, (0, 0, 0))
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        self.window.blit(text, text_rect)
        pygame.display.flip()

        return (button_x, button_y, button_width, button_height)

    def display_boss_defeated(self):
        # Clear the screen
        self.window.blit(self.footer, (0, self.window_height - self.footer.get_height()*0.9))

        # Display "Boss Defeated" text
        boss_defeated_text = self.font.render("Boss Defeated", True, (255, 255, 255))
        boss_defeated_text_rect = boss_defeated_text.get_rect(center=(self.window_width // 2, self.window_height - self.footer_height // 1.2))
        self.window.blit(boss_defeated_text, boss_defeated_text_rect)
        pygame.display.flip()

        pygame.time.wait(3000)  # Wait for 3 seconds

        # Display the level up background image for 5 seconds
        self.window.blit(self.level_up_background, (0, 0))
        self.window.blit(self.level_up_image, (self.window_width//2 - self.level_up_image.get_width()//2, 50))

        choose_upgrade_text = self.font.render("Choose an upgrade: ", True, (255, 255, 255))
        choose_upgrade_text_rect = choose_upgrade_text.get_rect(center=(self.window_width // 2, 370))
        self.window.blit(choose_upgrade_text, choose_upgrade_text_rect)
        pygame.display.flip()

        self.draw_level_up_buttons()

        self.window.blit(self.next_level_image, (0,0))
        pygame.display.flip()
        pygame.time.wait(5000)

        return 'game_map'


    
    def draw_level_up_buttons(self):
        self.level_up_buttons = {}
        button_width = 300
        button_height = 60
        spacing = 20
        total_width = 3 * button_width + 2 * spacing
        start_x = (self.window_width - total_width) // 2
        start_y = self.window_height // 2

        buttons = ["Health +50", "Damage +20", "Special Upgrade"]
        for i, button in enumerate(buttons):
            x = start_x + i * (button_width + spacing)
            y = start_y
            pygame.draw.rect(self.window, (255, 255, 255), (x, y, button_width, button_height))
            pygame.draw.rect(self.window, (0, 0, 0), (x, y, button_width, button_height), 2)  # Border

            text = self.font.render(button, True, (0, 0, 0))
            text_rect = text.get_rect(center=(x + button_width // 2, y + button_height // 2))
            self.window.blit(text, text_rect)

            self.level_up_buttons[button] = pygame.Rect(x, y, button_width, button_height)
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    for button, rect in self.level_up_buttons.items():
                        if rect.collidepoint(x, y):
                            self.apply_level_up_effect(button)
                            waiting_for_input = False


    def apply_level_up_effect(self, effect):
        if effect == "Health +50":
            self.max_health += 50
            self.health = self.max_health
        elif effect == "Damage +20":
            self.player_attack_count = 0  # Reset player attack count to avoid instant special attack
            self.damage_bonus = 20
        elif effect == "Special Upgrade":
            if isinstance(self.character_type, Mage):
                self.character_type.special_upgrade('Special Upgrade')

    def end_round(self):
        return self.round


    def run(self):
        self.reset()
        self.next_round()
        if self.enemy_health != 0:
            running = True
        else:
            running = False
            return 'game_map'

        # Display the boss incoming image for 3 seconds
        self.window.blit(self.boss_incoming_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds

        button_areas = []

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'menu'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'menu'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.health <= 0:
                        game_over_button = self.display_game_over()
                        if game_over_button[0] < pos[0] < game_over_button[0] + game_over_button[2] and game_over_button[1] < pos[1] < game_over_button[1] + game_over_button[3]:
                            self.reset()
                            return 'game_over'
                    if self.turn == "player":
                        for i, area in enumerate(button_areas):
                            if area[0] < pos[0] < area[0] + area[2] and area[1] < pos[1] < area[1] + area[3]:
                                action = ["Heal", "Attack", "Special", "Shield"][i]
                                if action != "Special" or (action == "Special" and self.player_attack_count >= 3):
                                    self.handle_player_action(action)
                                    if self.enemy_health == 0:
                                        self.display_boss_defeated()
                                        self.end_round()
                                        running = False
                                        return 'game_map'
                                    
                                    self.turn = "enemy"
                                    self.window.blit(self.footer, (0, self.window_height - self.footer.get_height() * 0.9))
                                    turn_text = self.font.render("Enemy's turn...", True, (255, 255, 255))
                                    turn_text_rect = turn_text.get_rect(center=(self.window_width // 2, self.window_height - self.footer_height // 1.2))
                                    self.window.blit(turn_text, turn_text_rect)
                                    pygame.display.flip()
                                    pygame.time.wait(1000)
                                    break

            if self.health <= 0:
                self.display_game_over()
                continue

            # Draw the boss map
            self.window.blit(self.map_level2, (0, 0))

            # Draw the player health bar on the left-hand side
            self.draw_health_bar(50, self.header_height // 2, self.health, self.max_health, self.character_type, (0, 255, 0))

            # Draw the enemy health bar on the right-hand side
            self.draw_health_bar(self.window_width - 350, self.header_height // 2, self.enemy_health, 100, "Enemy", (255, 255, 0))

            # Draw the player image below the banner
            if self.player_image:
                self.window.blit(self.player_image, (100, self.header_height))
                if self.shield_active:
                    self.window.blit(self.shield_image, (100, self.header_height))
                if self.round == 1:
                    self.window.blit(self.enemy_image, (800, self.header_height + 50))
                elif self.round == 2:
                    self.window.blit(self.enemy_image, (550, self.header_height + 20))
                elif self.round == 3:
                    self.window.blit(self.enemy_image, (570, self.header_height + 80))

            # Draw footer banner
            self.window.blit(self.footer, (0, self.window_height - self.footer.get_height() * 0.9))

            if self.turn == "player":
                # Draw action buttons and handle clicks
                self.action_text = "Your turn: Select an action"
                button_areas = self.draw_action_buttons()
            else:
                self.handle_enemy_action()
                self.turn = "player"

            # Draw the turn indicator
            turn_text = self.font.render(self.action_text, True, (255, 255, 255))
            turn_text_rect = turn_text.get_rect(center=(self.window_width // 2, self.window_height - self.footer_height // 1.2))
            self.window.blit(turn_text, turn_text_rect)

            # Draw enemy special bar
            self.draw_enemy_special_bar(self.window_width - 100, self.header_height + 50, self.enemy_special_counter, 5)

            pygame.display.flip()


        return 'game_map'

