import pygame
from config import *
from utils import *

def draw_menu_options(screen, selected_difficulty, selected_theme, selected_mode):
    """Draws menu options for difficulty, theme, and game mode."""
    screen.fill((30, 30, 30))

    draw_text(screen, "Select AI Difficulty:", (50, 50))
    draw_text(screen, "Select Board Theme:", (350, 50))
    draw_text(screen, "Select Game Mode:", (50, 300))

    # Draw Difficulty Options
    for i, diff in enumerate(DIFFICULTY.keys()):
        color = (0, 255, 0) if diff == selected_difficulty else (200, 200, 200)
        draw_text(screen, diff, (70, 100 + i * 40), 32, color)

    # Draw Theme Options
    for i, theme in enumerate(THEMES):
        color = (0, 255, 0) if theme == selected_theme else (200, 200, 200)
        draw_text(screen, theme, (370, 100 + i * 40), 32, color)

    # Draw Game Mode Options
    for i, mode in enumerate(GAME_MODES):
        color = (0, 255, 0) if mode == selected_mode else (200, 200, 200)
        draw_text(screen, mode, (70, 350 + i * 40), 32, color)

    screen.blit(pygame.image.load(f"images/wk.png"), (WIDTH - 200, HEIGHT - 200))  # Add logo

    # Draw Start Button
    pygame.draw.rect(screen, (100, 200, 100), START_BUTTON_RECT, border_radius=10)  # Rounded button
    draw_text(screen, "Start Game", (START_BUTTON_RECT.x + 15, START_BUTTON_RECT.y + 12), 32, (0, 0, 0))  # Center text
    # Draw Quit Button
    pygame.draw.rect(screen, (255, 0, 0), QUIT_BUTTON_RECT, border_radius=10)  # Rounded button
    draw_text(screen, "Quit", (QUIT_BUTTON_RECT.x + 40, QUIT_BUTTON_RECT.y + 12), 32, (0, 0, 0))  # Center text

def handle_menu_events(screen, selected_difficulty, selected_theme, selected_mode):
    """Handles user interactions in the menu screen."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            play_sound("sounds/select-menu.mp3")  # Play sound on click
            x, y = event.pos

            if START_BUTTON_RECT.collidepoint(x, y):  # Check if click is inside the button
                return False, selected_difficulty, selected_theme, selected_mode  
            elif QUIT_BUTTON_RECT.collidepoint(x, y):  # Check if click is inside the button
                pygame.quit()
                exit()
            # Check difficulty selection
            for i, diff in enumerate(DIFFICULTY.keys()):
                if 70 <= x <= 200 and 100 + i * 40 <= y <= 130 + i * 40:
                    selected_difficulty = diff

            # Check theme selection
            for i, theme in enumerate(THEMES):
                if 320 <= x <= 500 and 100 + i * 40 <= y <= 130 + i * 40:
                    selected_theme = theme  # Fixes incorrect Y-coordinates for theme selection

            # Check game mode selection
            for i, mode in enumerate(GAME_MODES):
                if 70 <= x <= 300 and 350 + i * 40 <= y <= 380 + i * 40:
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
        running, selected_difficulty, selected_theme, selected_mode = handle_menu_events(screen,
            selected_difficulty, selected_theme, selected_mode
        )


    return selected_difficulty, selected_theme, selected_mode
