import pygame
from .electrox import ElectroxGame

def main():
    """
    Starts and runs the Electrox game.
    """
    # Initialize Pygame
    pygame.init()

    # Create an instance of ElectroxGame
    game = ElectroxGame(window_size="small")
    game.create_player("Player1")  # Create a player for testing

    # Run the game loop
    game.run_game()

if __name__ == "__main__":
    main()
