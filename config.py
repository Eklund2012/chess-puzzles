import pygame

# Screen Dimensions
WIDTH, HEIGHT = 740, 740
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS


HIGHLIGHT_COLOR = (186, 202, 68, 150)

# Theme Colors
DARK_MODE = ((50, 50, 50), (80, 80, 80))  # Dark board squares
LIGHT_MODE = (238, 238, 210), (118, 150, 86)  # Light board squares

# Dictionary Mapping Themes to Colors
THEME_COLORS = {
    'Light': ((238, 238, 210), (118, 150, 86)),  # Classic white-green
    'Dark': ((50, 50, 50), (80, 80, 80)),  # Dark mode
    'Classic Wood': ((222, 184, 135), (139, 69, 19)),  # Wooden brown theme
    'Blue Lagoon': ((173, 216, 230), (25, 25, 112)),  # Light blue & Midnight blue
    'Green Forest': ((144, 238, 144), (34, 139, 34)),  # Green shades
    'Red Velvet': ((255, 192, 203), (139, 0, 0)),  # Pink & Dark Red
    'Cyberpunk Neon': ((255, 255, 0), (75, 0, 130)),  # Yellow & Indigo
    'Marble': ((220, 220, 220), (105, 105, 105)),  # Light & Dark Gray
    'Ocean Wave': ((135, 206, 250), (0, 51, 102))  # Sky Blue & Dark Navy
}

# Piece Images List
PIECE_NAMES = [
    "wp", "bp", "wr", "br", "wn", "bn", 
    "wb", "bb", "wq", "bq", "wk", "bk"
]

# Game Settings
DIFFICULTY = {
    'Easy': 1,
    'Medium': 3,
    'Hard': 5
}

THEMES = ['Light', 'Dark', 'Classic Wood', 'Blue Lagoon', 'Green Forest', 'Red Velvet', 'Cyberpunk Neon', 'Marble', 'Ocean Wave']
GAME_MODES = ['Human vs AI',
              'Human vs Human',
              'AI vs AI']

# Button Rectangles
BUTTON_RECT = pygame.Rect(300, 700, 150, 50)  # Start Game button
