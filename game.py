import pygame
import chess
import chess.engine
import asyncio

from config import *
from init import Init  
from board import Board  
from menu import menu_screen
from utils import draw_text
from puzzles.puzzle_mode import puzzle_mode
from utils import *
from simpleai import SimpleAI

# Initialize the game components using Init
game = Init()
screen = game.screen
chess_board = game.chess_board
#ai = game.ai  
ai = SimpleAI()

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
            pygame.quit()
            exit()
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
                if len(chess_board.move_stack) > 1:  
                    chess_board.pop()
                    chess_board.pop()  # Undo opponent’s move too
            elif event.key == pygame.K_q:
                print("test")
                return False
        

    return True  # Continue game loop

def game_over_screen(screen):
    """Displays a game over screen with options to replay or return to menu."""
    screen.fill((30, 30, 30))
    draw_text(screen, "Game Over", (WIDTH // 2 - 100, HEIGHT // 2 - 50), 48, (255, 0, 0))
    draw_text(screen, "Press R to Replay", (WIDTH // 2 - 120, HEIGHT // 2), 36, (0, 255, 0))
    draw_text(screen, "Press M to Return to Menu", (WIDTH // 2 - 160, HEIGHT // 2 + 40), 36, (0, 255, 0))
    pygame.display.flip()

def handle_game_over_input():
    """Handles user input on the game over screen."""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Exiting game.")
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return 'replay'  # Restart the game
                elif event.key == pygame.K_m:
                    return 'menu'  # Return to main menu          

def game_loop(game_mode, theme):
    print("Entered game loop!")  # <---- add this
    """Manages the main game loop asynchronously for Pygbag compatibility."""
    global selected_square
    running = True
    board = Board(screen)

    while running:
        running = update_display(board, theme)

        if chess_board.is_game_over():
            game_over_screen(screen)  # Display game over options
            game_over_choice = handle_game_over_input()

            if game_over_choice == 'replay':
                chess_board.reset()  # Reset board for replay
                return True  # Restart the game
            elif game_over_choice == 'menu':
                return False  # Return to menu

        if not chess_board.turn and game_mode == "Human vs AI":
            ai_move()
        elif game_mode == "AI vs AI":
            ai_move()
        elif game_mode == "Puzzle Mode":
            running = puzzle_mode(screen, chess_board, theme)
            print("Puzzle mode ended.")
            chess_board.reset()  # Reset board after puzzle mode
            return False

        running = handle_player_input()
        
    return False  # Ensure return to menu when exiting


async def run():
    print("Main started")  
    """Starts the game asynchronously for Pygbag."""
    replay_game = True
    difficulty, theme, game_mode = menu_screen()
    while True:
        if not replay_game:
            difficulty, theme, game_mode = menu_screen()  # Show menu before every game

        pygame.display.set_caption(f"Chess - Game: {game_mode} - {theme} - {difficulty}")
        ai.set_difficulty(DIFFICULTY[difficulty])  # Set AI difficulty
        
        play_sound("assets/sounds/board_start.mp3")  # Play sound when the board is drawn
        replay_game = game_loop(game_mode, theme)  # Await async function
        await asyncio.sleep(0)
        if not replay_game:
            continue  # Go back to the menu instead of closing the program
    




