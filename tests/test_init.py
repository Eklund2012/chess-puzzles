import pygame
from init import Init

def test_game_initialization():
    game = Init()
    
    assert game.screen is not None  # Ensure screen is initialized
    assert game.chess_board is not None  # Ensure chess board is initialized
    assert game.chess_board.is_game_over() is False  # Ensure game starts properly
