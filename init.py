#init.py

import pygame
import chess

from config import WIDTH, HEIGHT
from ai import ChessAI


class Init:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.chess_board = chess.Board()
        self.selected_square = None
        self.ai = ChessAI(difficulty=5)