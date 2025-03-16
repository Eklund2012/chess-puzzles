#config.py

# Constants
WIDTH, HEIGHT = 740, 740
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (238, 238, 210)
BROWN = (118, 150, 86)
HIGHLIGHT_COLOR = (186, 202, 68, 150)

DARK_MODE = (50, 50, 50), (80, 80, 80)
LIGHT_MODE = WHITE, BROWN

PIECE_NAMES = ["wp", "bp", "wr", "br", "wn", "bn", "wb", "bb", "wq", "bq", "wk", "bk"]

DIFFICULTY = {'Easy': 1, 'Medium': 3, 'Hard': 5}
THEMES = ['Light', 'Dark']
GAME_MODES = ['Human vs AI', 'Human vs Human']
