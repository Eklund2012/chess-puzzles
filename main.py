import pygame
import chess
import chess.engine

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 740, 900
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (238, 238, 210)
BROWN = (118, 150, 86)
HIGHLIGHT_COLOR = (186, 202, 68, 150)  # Semi-transparent highlight

# Load images
PIECES = {}
for piece in ["wp", "bp", "wr", "br", "wn", "bn", "wb", "bb", "wq", "bq", "wk", "bk"]:
    PIECES[piece] = pygame.transform.scale(pygame.image.load(f"images/{piece}.png"), (SQUARE_SIZE, SQUARE_SIZE))

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Game")

# Initialize chess board
chess_board = chess.Board()
selected_square = None

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

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

def main():
    global selected_square
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_board()
        highlight_moves()
        draw_pieces()
        highlight_check()
        highlight_checkmate()
        draw_undo_button()
        handle_undo_click(pygame.mouse.get_pos())
        highlight_selected_piece()
        pygame.display.flip()
        
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
