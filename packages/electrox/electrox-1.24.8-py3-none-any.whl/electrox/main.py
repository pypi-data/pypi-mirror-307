import pygame
from .electrox import ElectroxGame

def main():
    game = ElectroxGame(name="Test Electrox Game", window_size="medium")
    game.create_player("player1")
    game.run_game()

if __name__ == "__main__":
    main()
