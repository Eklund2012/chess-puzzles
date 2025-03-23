# puzzle_mode.py
import pygame
import chess
import json
from utils import draw_text
from config import *
from board import Board  

def get_square_from_pos(pos):
    """Converts mouse position to a chess square."""
    x, y = pos
    return chess.square(x // SQUARE_SIZE, 7 - (y // SQUARE_SIZE))

def load_puzzles():
    """Loads puzzles from a JSON file."""
    with open("./puzzles/puzzles.json", "r") as f:
        return json.load(f)

def update_display_puzzle(screen, board, theme, chess_board, selected_square):
    """Renders the chessboard and pieces for puzzle mode."""
    screen.fill((0, 0, 0))
    board.draw_board(screen, theme)
    board.draw_pieces(screen, chess_board)
    board.highlight_moves(selected_square, chess_board, screen)
    board.highlight_check(chess_board, screen)
    
    if board.highlight_checkmate(chess_board, screen):
        return False

    board.highlight_selected_piece(selected_square, screen)
    pygame.display.flip()
    return True

def draw_puzzle_options(screen):
    """Draws the puzzle options on the screen."""
    screen.fill((30, 30, 30))
    draw_text(screen, "Puzzle Mode", (50, 50), 64)
    draw_text(screen, "Press 'Q' to quit", (50, 200), 32)
    draw_text(screen, "Press 'S' to start", (50, 250), 32)
    draw_text(screen, "Press 'H' during game for hints", (50, 300), 32)

def draw_puzzle_menu():
    """Draws the puzzle menu and waits for user interaction."""
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puzzle Mode - Menu")
    running = True
    while running:
        draw_puzzle_options(screen)
        pygame.display.flip()

        # Check for events to proceed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:  # Allow quitting from the menu
                    return False
                elif event.key == pygame.K_s:  # Any other key will proceed to the puzzle
                    running = False  # Exit the loop and start the puzzle mode
                    break  # Break out of the event loop

    return True# When the loop finishes, we exit and start the puzzle mode

def draw_feedback(screen, message, color=(255, 255, 255)):
    draw_text(screen, message, (WIDTH / 2 - 100, HEIGHT / 2), 72, color)
    pygame.display.flip()
    pygame.time.delay(1000)  # Pause for 1 second

def draw_puzzle_hint(screen, hint):
    """Displays the puzzle hint on the screen."""
    screen.fill((30, 30, 30))
    draw_text(screen, f"Hint: {hint}", (50, HEIGHT - 100), 28, (200, 200, 0))
    pygame.display.flip()
    pygame.time.delay(1000) 

def puzzle_mode(screen, chess_board, theme):
    """Runs the puzzle mode."""
    puzzle_index = 0
    puzzles = load_puzzles()
    board = Board(screen)

    if(not draw_puzzle_menu()):
        return False

    while puzzle_index < len(puzzles):
        print(f"Puzzle {puzzle_index + 1}/{len(puzzles)}")
        puzzle = puzzles[puzzle_index]
        chess_board.set_fen(puzzle["fen"])  # Set the board to the puzzle position
        solution_moves = [chess.Move.from_uci(move) for move in puzzle["solution"]]
        
        selected_square = None
        puzzle_solved = False  # Flag to track if puzzle is solved

        while not puzzle_solved:
            update_display_puzzle(screen, board, theme, chess_board, selected_square)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        print("Exiting puzzle mode.")
                        return False
                    elif event.key == pygame.K_h:
                        draw_puzzle_hint(screen, puzzle["hint"])
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    square = get_square_from_pos(pygame.mouse.get_pos())

                    if selected_square is None:
                        if chess_board.piece_at(square):
                            selected_square = square  # Select piece
                    elif selected_square == square:
                        selected_square = None  # Deselect if clicking the same piece
                    else:
                        move = chess.Move(selected_square, square)
                        if move in solution_moves:
                            draw_feedback(screen, "Correct!", (0, 255, 0))
                            puzzle_solved = True  # Puzzle solved, exit loop
                        else:
                            draw_feedback(screen, "Try again!", (255, 0, 0))
                        selected_square = None  # Reset selection after move attempt



        # Move to the next puzzle
        puzzle_index += 1  

    print("You completed all puzzles!")
    return False
