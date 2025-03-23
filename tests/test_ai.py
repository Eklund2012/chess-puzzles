import chess_game
from stockfish.ai import ChessAI

def test_ai_best_move():
    ai = ChessAI(difficulty=1)
    board = chess_game.Board()
    move = ai.get_best_move(board)
    
    assert move is not None  # Ensure AI returns a move
    assert chess_game.Move.from_uci(str(move)) in board.legal_moves  # Move must be legal
