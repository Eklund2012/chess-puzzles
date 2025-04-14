import random

class SimpleAI:
    def __init__(self, difficulty=1):
        self.difficulty = difficulty  # You can use this for smarter AI later

    def get_best_move(self, board):
        moves = list(board.legal_moves)
        if moves:
            return random.choice(moves)
        return None
    
    def set_difficulty(self, difficulty):
        # This simple AI does not have different difficulty levels
        pass

