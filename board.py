#board.py
#functions related to drawing the chess board and pieces

import pygame
from config import ROWS, COLS, SQUARE_SIZE, WHITE, BROWN

class Board:
    def __init__(self, screen):
        self.screen = screen

    def draw_board(self, screen):
        for row in range(ROWS):
            for col in range(COLS):
                color = WHITE if (row + col) % 2 == 0 else BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))