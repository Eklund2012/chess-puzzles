#utils.py

import pygame

# Function to draw text on the screen at a specified position
def draw_text(screen, text, pos, size=36, color=(255, 255, 255)):
    # Load the default font with the specified size
    font = pygame.font.Font(None, size)

    # Render the text with the chosen font and color
    rendered_text = font.render(text, True, color)

    # Draw the rendered text at the specified position on the screen
    screen.blit(rendered_text, pos)