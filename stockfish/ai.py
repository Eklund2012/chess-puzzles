# ai.py
import chess
import chess.engine

STOCKFISH_PATH = "stockfish/stockfish-windows-x86-64-avx2.exe"

class ChessAI:
    def __init__(self, difficulty=1):
        self.engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
        self.set_difficulty(difficulty)

    def set_difficulty(self, difficulty):
        """Set the difficulty level (Stockfish skill level)."""
        self.engine.configure({"Skill Level": difficulty})

    def get_best_move(self, board):
        """Let Stockfish decide the best move."""
        legal_moves = list(board.legal_moves)  # Get all legal moves
        if not legal_moves:
            return None  # No moves available (checkmate/stalemate)
        result = self.engine.play(board, chess.engine.Limit(time=0.5))
        return result.move

    def close(self):
        """Shut down the engine properly."""
        self.engine.quit()
