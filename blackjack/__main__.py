from .models import Game

game = Game()

try:
    game.start()
except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt...")
