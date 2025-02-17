__all__ = ["Environment", "GridWorld", "load_game"]

from games.__base__     import Environment

from games.grid_world   import GridWorld

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

        # Grid World
        case "grid-world":  return GridWorld(**kwargs)

        # Invalid selection
        case _:             raise ValueError(f"Invalid game selection: {game}")