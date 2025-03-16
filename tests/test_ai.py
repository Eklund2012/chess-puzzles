import chess
from ai import ChessAI

def test_ai_best_move():
    ai = ChessAI(difficulty=1)
    board = chess.Board()
    move = ai.get_best_move(board)
    
    assert move is not None  # Ensure AI returns a move
    assert chess.Move.from_uci(str(move)) in board.legal_moves  # Move must be legal
