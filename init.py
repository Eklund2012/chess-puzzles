#init.py

import pygame
import chess

from config import WIDTH, HEIGHT
from simpleai import SimpleAI 


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
        print("Pygame initialized")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Chess Game")
        self.chess_board = chess.Board()
        self.selected_square = None
        self.ai = SimpleAI(difficulty=5)
