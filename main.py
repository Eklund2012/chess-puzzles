#main.py

import pygame
import chess
import chess.engine

from config import WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE, WHITE, BROWN, HIGHLIGHT_COLOR, PIECE_NAMES, DARK_MODE, LIGHT_MODE
from init import Init  # Import the Init class
from board import Board  # Import the Board class

# Load images dynamically
PIECES = {piece: pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE)) for piece in PIECE_NAMES}


# Initialize the game components using Init
game = Init()
screen = game.screen
chess_board = game.chess_board
ai = game.ai  # AI instance

selected_square = None  # Keep track of the selected square

def ai_move():
    move = ai.get_best_move(chess_board)
    chess_board.push(move)

board = Board(screen)  # Initialize the Board
#functions related to drawing the chess board and pieces

def draw_pieces():
    board_fen = chess_board.board_fen().split()[0].replace("/", "")
    row, col = 0, 0
    for char in board_fen:
        if char.isdigit():
            col += int(char)
        else:
            piece = char.lower()
            color = "w" if char.isupper() else "b"
            screen.blit(PIECES[color + piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
            col += 1
        if col >= 8:
            col = 0
            row += 1

def highlight_moves():
    if selected_square is not None:
        for move in chess_board.legal_moves:
            if move.from_square == selected_square:
                row, col = divmod(move.to_square, 8)
                highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                highlight_surface.fill(HIGHLIGHT_COLOR)
                screen.blit(highlight_surface, (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE))

def get_square_from_pos(pos):
    x, y = pos
    return chess.square(x // SQUARE_SIZE, 7 - (y // SQUARE_SIZE))

def highlight_check():
    if chess_board.is_check():
        king_square = chess_board.king(chess_board.turn)
        row, col = divmod(king_square, 8)
        pygame.draw.rect(screen, (255, 0, 0, 150), (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

def highlight_checkmate():
    if chess_board.is_checkmate():
        font = pygame.font.Font(None, 36)
        text = font.render("Checkmate!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

def draw_undo_button():
    font = pygame.font.Font(None, 36)
    text = font.render("Undo", True, (0, 0, 0))
    pygame.draw.rect(screen, (200, 200, 200), (WIDTH - 100, 10, 80, 40))  # Button
    screen.blit(text, (WIDTH - 95, 20))

def handle_undo_click(pos):
    if pygame.mouse.get_pressed()[0] and WIDTH - 100 <= pos[0] <= WIDTH - 20 and 10 <= pos[1] <= 50:
        if chess_board.move_stack:
            chess_board.pop()

def highlight_selected_piece():
    if selected_square is not None:
        row, col = divmod(selected_square, 8)
        pygame.draw.rect(screen, (0, 255, 0, 150), (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

DIFFICULTY = {'Easy': 1, 'Medium': 3, 'Hard': 5}
GAME_MODES = ['Human vs AI', 'Human vs Human']

def draw_text(screen, text, pos, size=36, color=(255, 255, 255)):
    font = pygame.font.Font(None, size)
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, pos)

def menu_screen():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess - Main Menu")
    running = True
    selected_difficulty = 'Medium'
    selected_theme = LIGHT_MODE
    selected_mode = 'Human vs AI'
    
    while running:
        screen.fill((30, 30, 30))
        draw_text(screen, "Select Difficulty:", (50, 50))
        draw_text(screen, "Select Theme:", (50, 200))
        draw_text(screen, "Select Game Mode:", (50, 350))
        
        for i, diff in enumerate(DIFFICULTY.keys()):
            color = (0, 255, 0) if diff == selected_difficulty else (200, 200, 200)
            draw_text(screen, diff, (70, 100 + i * 40), 32, color)
        
        for i, mode in enumerate(GAME_MODES):
            color = (0, 255, 0) if mode == selected_mode else (200, 200, 200)
            draw_text(screen, mode, (70, 400 + i * 40), 32, color)
        
        pygame.draw.rect(screen, (100, 200, 100), (300, 700, 150, 50))
        draw_text(screen, "Start Game", (320, 715))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 300 <= x <= 450 and 700 <= y <= 750:
                    running = False
                for i, diff in enumerate(DIFFICULTY.keys()):
                    if 70 <= x <= 200 and 100 + i * 40 <= y <= 130 + i * 40:
                        selected_difficulty = diff
                for i, mode in enumerate(GAME_MODES):
                    if 70 <= x <= 300 and 400 + i * 40 <= y <= 430 + i * 40:
                        selected_mode = mode
    return selected_difficulty, selected_theme, selected_mode

def main():
    difficulty, theme, game_mode = menu_screen()
    print(f"Selected Difficulty: {difficulty}")
    print(f"Selected Theme: {theme}")
    print(f"Selected Game Mode: {game_mode}")
    # Start the chess game here
    global selected_square
    running = True
    while running:
        screen.fill((0, 0, 0))
        board.draw_board(screen)
        draw_pieces()
        highlight_moves()
        highlight_check()
        highlight_checkmate()
        draw_undo_button()
        handle_undo_click(pygame.mouse.get_pos())
        highlight_selected_piece()
        pygame.display.flip()

        if not chess_board.turn:  # If it's Black's turn (AI)
            ai_move()

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                square = get_square_from_pos(pygame.mouse.get_pos())
                if selected_square is None:
                    if chess_board.piece_at(square):
                        selected_square = square
                else:
                    move = chess.Move(selected_square, square)
                    if move in chess_board.legal_moves:
                        chess_board.push(move)
                    selected_square = None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if chess_board.move_stack:
                        chess_board.pop()

    pygame.quit()

if __name__ == "__main__":
    main()
