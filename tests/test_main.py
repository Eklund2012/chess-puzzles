import chess
from main import get_square_from_pos  # Example function

def test_get_square_from_pos():
    square = get_square_from_pos((100, 100))  # Assuming a standard 8x8 board
    assert isinstance(square, chess.Square)  # Check it returns a valid chess square
