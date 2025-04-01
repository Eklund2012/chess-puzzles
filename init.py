#init.py

import pygame
import chess

from config import WIDTH, HEIGHT
from stockfish.ai import ChessAI


class Init:
    def __init__(self):
        """
        Initializes the game setup:
        - Initializes Pygame
        - Sets up the game screen with specified dimensions
        - Initializes the chess board using the 'chess' library
        - Sets up the AI with a predefined difficulty
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.chess_board = chess.Board()
        self.selected_square = None
        self.ai = ChessAI(difficulty=5)