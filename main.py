#main.py
import pygame
import chess
import chess.engine

from config import *
from init import Init  # Import the Init class
from board import Board  # Import the Board class
from menu import menu_screen

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

def get_square_from_pos(pos):
    x, y = pos
    return chess.square(x // SQUARE_SIZE, 7 - (y // SQUARE_SIZE))

def main():
    difficulty, theme, game_mode = menu_screen()
    print(f"Selected Difficulty: {difficulty}")
    print(f"Selected Theme: {theme}")
    print(f"Selected Game Mode: {game_mode}")
    
    global selected_square
    running = True
    while running:
        screen.fill((0, 0, 0))
        board.draw_board(screen)
        board.draw_pieces(screen, chess_board)
        board.highlight_moves(selected_square, chess_board, screen)
        board.highlight_check(chess_board, screen)
        board.highlight_checkmate(chess_board, screen)
        board.highlight_selected_piece(selected_square, screen)
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
