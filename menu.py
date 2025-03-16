import pygame
from config import WIDTH, HEIGHT, DIFFICULTY, THEMES, GAME_MODES
from utils import draw_text 

def draw_menu_options(screen, selected_difficulty, selected_theme, selected_mode):
    """Draws menu options for difficulty, theme, and game mode."""
    screen.fill((30, 30, 30))
    draw_text(screen, "Select Difficulty:", (50, 50))
    draw_text(screen, "Select Theme:", (50, 200))
    draw_text(screen, "Select Game Mode:", (50, 350))

    for i, diff in enumerate(DIFFICULTY.keys()):
        color = (0, 255, 0) if diff == selected_difficulty else (200, 200, 200)
        draw_text(screen, diff, (70, 100 + i * 40), 32, color)

    for i, theme in enumerate(THEMES):
        color = (0, 255, 0) if theme == selected_theme else (200, 200, 200)
        draw_text(screen, theme, (70, 250 + i * 40), 32, color)

    for i, mode in enumerate(GAME_MODES):
        color = (0, 255, 0) if mode == selected_mode else (200, 200, 200)
        draw_text(screen, mode, (70, 400 + i * 40), 32, color)

    pygame.draw.rect(screen, (100, 200, 100), (300, 700, 150, 50))
    draw_text(screen, "Start Game", (320, 715))

def handle_menu_events(selected_difficulty, selected_theme, selected_mode):
    """Handles user interactions in the menu screen."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 300 <= x <= 450 and 700 <= y <= 750:
                return False, selected_difficulty, selected_theme, selected_mode  

            for i, diff in enumerate(DIFFICULTY.keys()):
                if 70 <= x <= 200 and 100 + i * 40 <= y <= 130 + i * 40:
                    selected_difficulty = diff

            for i, theme in enumerate(THEMES):
                if 70 <= x <= 200 and 250 + i * 40 <= y <= 280 + i * 40:
                    selected_theme = theme if theme == 'Light' else 'Dark'

            for i, mode in enumerate(GAME_MODES):
                if 70 <= x <= 300 and 400 + i * 40 <= y <= 430 + i * 40:
                    selected_mode = mode

    return True, selected_difficulty, selected_theme, selected_mode  

def menu_screen():
    """Displays the menu and returns selected options."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess - Main Menu")
    
    selected_difficulty = 'Medium'
    selected_theme = 'Light'
    selected_mode = 'Human vs AI'
    running = True

    while running:
        draw_menu_options(screen, selected_difficulty, selected_theme, selected_mode)
        pygame.display.flip()
        running, selected_difficulty, selected_theme, selected_mode = handle_menu_events(
            selected_difficulty, selected_theme, selected_mode
        )

    return selected_difficulty, selected_theme, selected_mode
