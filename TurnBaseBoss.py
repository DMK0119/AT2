import pygame

class TurnBase:
    def __init__(self, window):
        self.window = window
        self.window_width = self.window.get_width()
        self.window_height = self.window.get_height()
        self.map_level2 = pygame.image.load("./assets/boss_map.jpeg").convert_alpha()
        self.map_level2 = pygame.transform.scale(self.map_level2, (self.window.get_width(), self.window.get_height()))
        self.boss_incoming_image = pygame.image.load("./assets/BossIncoming.png").convert_alpha()
        self.boss_incoming_image = pygame.transform.scale(self.boss_incoming_image, (self.window.get_width(), self.window.get_height()))

    def run(self):
        running = True

        # Display the boss incoming image for 5 seconds
        self.window.blit(self.boss_incoming_image, (0, 0))
        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 5 seconds

        # Switch to the boss map image
        self.window.blit(self.map_level2, (0, 0))
        pygame.display.flip()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'quit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'menu'

            # Any additional game logic for the boss map can go here

            pygame.display.flip()

        return 'menu'
