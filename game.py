import pygame
from menu import MainMenu
from character_select import CharacterSelect
from map import Map
from TurnBaseBoss import TurnBase
from assets import load_assets, GAME_ASSETS
import sys

class Game:
    def __init__(self):
        pygame.init()
        load_assets()  # load the game image assets
        self.window = pygame.display.set_mode((1100, 800))
        self.menu = MainMenu(self.window)  # Create an instance of the MainMenu class
        self.character_select = CharacterSelect(self.window)  # Create an instance of the CharacterSelect class
        self.game_map = Map(self.window)  # Create an instance of the Map class
        self.state = 'menu'  # Set the initial state to 'menu'
        self.current_character = None  # To store the chosen character
        self.Level2 = None  # Initialize Level2 as None
        self.round = 0

    def reset_game(self):
        """
        Reset the game state.
        """
        if self.current_character:
            self.game_map.reset_game(self.round)  # Reset the game map with the current round
            self.game_map.load_player(self.current_character)  # Reload player with the same type
            self.state = 'game_map'  # Change the state back to 'game_map'
            self.game_map.next_round()  # Update the round-specific features in the map

    def run(self):
        clock=pygame.time.Clock()
        while True:
            clock.tick(100)
            if self.state == 'menu':  # If the state is 'menu'
                result = self.menu.run()  # Run the menu and get the result
                if result == 'Start Game':  # If the result is 'Start Game'
                    self.state = 'character_select'  # Change the state to 'character_select'
                elif result == 'Settings':  # If the result is 'Settings'
                    pass  # Settings handling would go here
                elif result == 'Exit':  # If the result is 'Exit'
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method

            elif self.state == 'character_select':  # If the state is 'character_select'
                selected_character = self.character_select.run()  # Run the character select screen and get the selected character
                if selected_character == 'back':  # If the selected character is 'back'
                    self.state = 'menu'  # Change the state to 'menu'
                elif selected_character:  # If a character sis selected
                    self.current_character = selected_character  # Set the current character to the selected character
                    self.game_map.load_player(selected_character)  # Load the selected character into the game map
                    self.Level2 = TurnBase(self.window, self.current_character)  # Initialize TurnBase with the selected character
                    self.state = 'game_map'  # Change the state to 'game_map'

            elif self.state == 'game_map':
                result = self.game_map.handle_events()
                if result == 'back':
                    self.state = 'character_select'
                elif result == 'quit':
                    pygame.quit()
                    return
                elif result == 'Level2':
                    self.round += 1
                    self.state = 'Level2'


                self.game_map.draw()

                if self.game_map.game_over:
                    button_rect = self.game_map.display_game_over()
                    self.state = 'game_over'

            elif self.state == 'Level2':
                result = self.Level2.run()
                if result == 'game_map':  # Check if the result is to return to the map
                    self.state = 'game_map'  # Set the state back to 'game_map'
                    self.game_map.reset_game(self.round)  # Reset the game when transitioning to Level2
                    self.game_map.draw()  # Draw the map again

            elif self.state == 'game_over':
                sys.exit()

            for event in pygame.event.get():  # Iterate over the events in the event queue
                if event.type == pygame.QUIT:  # If the event type is QUIT
                    pygame.quit()  # Quit pygame
                    return  # Exit the run method

if __name__ == "__main__":
    game = Game()  # Create an instance of the Game class
    game.run()  # Run the game
