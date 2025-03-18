#board.py
#functions related to drawing the chess board and pieces

import pygame
from config import *


class Board:
    def __init__(self, screen):
        self.screen = screen
        self.PIECES = {
            piece: pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))
            for piece in PIECE_NAMES
        }
        
    def draw_board(self, screen, theme):
        light_color, dark_color = THEME_COLORS.get(theme, LIGHT_MODE)  # Default to LIGHT_MODE
        for row in range(ROWS):
            for col in range(COLS):
                color = light_color if (row + col) % 2 == 0 else dark_color
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def draw_pieces(self, screen, chess_board):
        board_fen = chess_board.board_fen().split()[0].replace("/", "")
        row, col = 0, 0
        for char in board_fen:
            if char.isdigit():
                col += int(char)
            else:
                piece = char.lower()
                color = "w" if char.isupper() else "b"
                screen.blit(self.PIECES[color + piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                col += 1
            if col >= 8:
                col = 0
                row += 1
            
    def highlight_moves(self, selected_square, chess_board, screen):
        if selected_square is not None:
            for move in chess_board.legal_moves:
                if move.from_square == selected_square:
                    row, col = divmod(move.to_square, 8)
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill(HIGHLIGHT_COLOR)
                    screen.blit(highlight_surface, (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE))

    def highlight_check(self, chess_board, screen):
        if chess_board.is_check():
            king_square = chess_board.king(chess_board.turn)
            row, col = divmod(king_square, 8)
            pygame.draw.rect(screen, (255, 0, 0, 150), (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
    
    def highlight_checkmate(self, chess_board, screen):
        if chess_board.is_checkmate():
            font = pygame.font.Font(None, 36)
            text = font.render("Checkmate!", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            return True
        return False

    def highlight_selected_piece(self, selected_square, screen):
        if selected_square is not None:
            row, col = divmod(selected_square, 8)
            pygame.draw.rect(screen, (0, 255, 0, 150), (col * SQUARE_SIZE, (7 - row) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)