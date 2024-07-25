import pygame
from assets import GAME_ASSETS

class CharacterSelect:

    def __init__(self, window):
        """
        Initializes the CharacterSelect object.

        Args:
            window (pygame.Surface): The game window surface.
        """
        self.window = window
        self.font = pygame.font.Font(None, 36)  # Use a default font
        self.background_image = pygame.image.load(GAME_ASSETS['main_menu_background']).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.window.get_width(), self.window.get_height()))
        self.characters = {
            "Warrior": pygame.image.load(GAME_ASSETS['warrior_button']).convert_alpha(),
            "Mage": pygame.image.load(GAME_ASSETS['mage_button']).convert_alpha(),
            "Rogue": pygame.image.load(GAME_ASSETS['rogue_button']).convert_alpha()
        }
        self.character_buttons = self.setup_character_buttons()
        self.back_button = pygame.Rect(50, self.window.get_height() - 50 - 30, 100, 30)  # Positioned at bottom left

    def setup_character_buttons(self):
        """
        Sets up the character buttons.

        Returns:
            dict: A dictionary mapping character names to their button rectangles.
        """
        buttons = {}
        total_spacing = 40  # spacing between buttons and edges
        num_buttons = len(self.characters)
        available_width = self.window.get_width() - total_spacing * (num_buttons + 1)
        button_width = available_width // num_buttons
        max_height = self.window.get_height() // 2  # maximum button height

        x = total_spacing
        y = self.window.get_height() // 3 - max_height // 4  # position them a bit higher to make space for back button

        for character, image in self.characters.items():
            aspect_ratio = image.get_height() / image.get_width()
            button_height = int(button_width * aspect_ratio)
            button_height = min(button_height, max_height)  # Ensure button isn't too tall
            scaled_image = pygame.transform.scale(image, (button_width, button_height))
            buttons[character] = (scaled_image, pygame.Rect(x, y, button_width, button_height))
            x += button_width + total_spacing

        return buttons

    def run(self):
        running = True
        while running:
            self.window.blit(self.background_image, (0, 0))
            for character, (image, rect) in self.character_buttons.items():
                self.window.blit(image, rect)

            # Draw back button
            pygame.draw.rect(self.window, (200, 200, 200), self.back_button)  # Draw a grey button
            back_text = self.font.render('Back', True, (0, 0, 0))
            text_rect = back_text.get_rect(center=self.back_button.center)
            self.window.blit(back_text, text_rect)

            # text for choosing character
            text_colour = (254, 252, 199)
            text = self.font.render("Choose your character", True, text_colour)
            text_rect = text.get_rect(center=(self.window.get_width() / 2, 100))
            # draw rectangle background behind each text
            background_rect = pygame.Rect(text_rect.left - 5, text_rect.top - 3, text_rect.width + 10, text_rect.height + 5)
            background_colour = (0, 0, 0)
            pygame.draw.rect(self.window, background_colour, background_rect)
            self.window.blit(text, text_rect)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return None
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return 'back'
                    for character, (image, rect) in self.character_buttons.items():
                        if rect.collidepoint(event.pos):
                            print(character)
                            return character

        return None
