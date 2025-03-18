import pygame
import chess
import chess.engine

from config import *
from init import Init  
from board import Board  
from menu import menu_screen

# Initialize the game components using Init
game = Init()
screen = game.screen
chess_board = game.chess_board
ai = game.ai  

selected_square = None  

def ai_move():
    """Handles AI's move if it's the AI's turn."""
    move = ai.get_best_move(chess_board)

    if move is None:  # Ensure AI found a valid move
        print("Error: AI did not find a valid move.")
        print("Current board state:\n", chess_board)
        return  # Prevent pushing None

    chess_board.push(move)

def get_square_from_pos(pos):
    """Converts mouse position to a chess square."""
    x, y = pos
    return chess.square(x // SQUARE_SIZE, 7 - (y // SQUARE_SIZE))

def update_display(board, theme):
    """Renders the chessboard and pieces."""
    screen.fill((0, 0, 0))
    board.draw_board(screen, theme)
    board.draw_pieces(screen, chess_board)
    board.highlight_moves(selected_square, chess_board, screen)
    board.highlight_check(chess_board, screen)
    if(board.highlight_checkmate(chess_board, screen)):
        return False
    board.highlight_selected_piece(selected_square, screen)
    pygame.display.flip()
    return True

def handle_player_input():
    """Handles mouse and keyboard input for player moves."""
    global selected_square

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False  # Exit game loop

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

    return True  # Continue game loop

def game_loop(game_mode, theme):
    """Manages the main game loop."""
    global selected_square
    running = True
    board = Board(screen)

    while running:
        running = update_display(board, theme)


        if chess_board.is_game_over():
            print("Game over!")
            break  # Stop the loop when the game ends
        if not chess_board.turn and game_mode == "Human vs AI":  # AI's turn
            ai_move()
        elif game_mode == "AI vs AI":
            ai_move()

        running = handle_player_input()

    pygame.quit()

def run_game():
    """Starts the game after menu selection."""
    difficulty, theme, game_mode = menu_screen()
    pygame.display.set_caption("Chess - Game: " + game_mode + " - " + theme + " - " + difficulty)
    ai.set_difficulty(DIFFICULTY[difficulty])  # Set AI difficulty

    try:
        game_loop(game_mode, theme)
    finally:
        ai.close()  # Ensure Stockfish is properly closed

if __name__ == "__main__":
    run_game()
