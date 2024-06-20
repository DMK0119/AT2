import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Turn-Based Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
gold = (255, 215, 0)

# Define fonts
font = pygame.font.SysFont('Consolas', 30)

# Button class
class Button:
    def __init__(self, text, pos, size):
        self.text = text
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)
        self.color = gold

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)
        text_surface = font.render(self.text, True, black)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Define player and enemy actions
actions = ["attack", "heal", "level up", "special ability"]

# Initialize turn variable
turn = 0

# Create buttons
buttons = [
    Button("Attack", (50, 500, 150, 50)),
    Button("Heal", (250, 500, 150, 50)),
    Button("Level Up", (450, 500, 150, 50)),
    Button("Special Ability", (650, 500, 150, 50))
]

# Main game loop
running = True
while running:
    window.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            for button in buttons:
                if button.is_clicked(pos) and turn % 2 == 0:
                    print(f"Player uses {button.text}")
                    turn += 1

    # Enemy turn
    if turn % 2 == 1:
        action = random.choice(actions)
        print(f"Enemy uses {action}")
        turn += 1

    # Draw buttons
    for button in buttons:
        button.draw(window)

    pygame.display.flip()
    pygame.time.wait(100)  # Small delay to make it easier to see the turns change

pygame.quit()
