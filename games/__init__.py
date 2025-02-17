__all__ = ["Blackjack", "Checkers", "Chess", "Environment", "Go", "GridWorld", "load_game", "Sudoku", "TicTacToe"]

from games.__base__     import Environment

from games.blackjack    import Blackjack
from games.checkers     import Checkers
from games.chess        import Chess
from games.go           import Go
from games.grid_world   import GridWorld
from games.sudoku       import Sudoku
from games.tic_tac_toe  import TicTacToe

def load_game(
    game:   str,
    **kwargs
) -> Environment:
    # Import logging utilities
    from logging    import Logger

    from utils      import LOGGER

    # Initialize logger
    __logger__: Logger =    LOGGER.getChild("game-loader")

    # Log action for debugging
    __logger__.debug(f"Loading game {locals()}")

    # Match game selection
    match game:

        # Blackjack
        case "blackjack":   return Blackjack(**kwargs)

        # Checkers
        case "checkers":    return Checkers(**kwargs)

        # Chess
        case "chess":       return Chess(**kwargs)

        # Go
        case "go":          return Go(**kwargs)

        # Grid World
        case "grid-world":  return GridWorld(**kwargs)

        # Sudoku
        case "sudoku":      return Sudoku(**kwargs)

        # Tic-Tac-Toe
        case "tictactoe":   return TicTacToe(**kwargs)

        # Invalid selection
        case _:             raise ValueError(f"Invalid game selection: {game}")