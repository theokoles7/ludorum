"""Execute game play process."""

__all__ = ["play_game"]

from logging    import Logger

from agents     import *
from games      import *
from utils      import LOGGER

def play_game(
    game:       str,
    agent:      str,
    episodes:   int =   100,
    max_steps:  int =   100,
    **kwargs
) -> dict:
    """# Execute game play process.

    ## Args:
        * game      (str):              Game being played.
        * agent     (str):              Agent to play game.
        * episodes  (int, optional):    Episodes for which agent will play game. Defaults to 100.
        * max_steps (int, optional):    Maximum amount of steps that agent is allowed to make within 
                                        each game episode. Defaults to 100.
                                        
    ## Returns:
        * dict: Game results.
    """
    # Initialize logger
    __logger__: Logger =    LOGGER.getChild("game-process")
    
    print(f"Play game: {locals()}")
    
    # Match game to initialize
    match game:
        
        # Initialize Grid-World
        case "grid-world":  environment:    GridWorld =         GridWorld(**kwargs)
        
        # Invalid game selection
        case _:                             raise ValueError(f"Invalid game selection: {game}")
        
    # Match agent to initialize
    match agent:
        
        # Initialize Q-Learning agent
        case "q-learning":  agent:          QLearningAgent =    QLearningAgent(
                                                                    state_size =    environment.state_size(),
                                                                    action_size =   environment.action_size(),
                                                                    **kwargs
                                                                )
        
        # Invalid agent selection
        case _:                             raise ValueError(f"Invalid agent selection: {agent}")
        
    # Play game & return results
    return agent._train_(
        environment =   environment,
        episodes =      episodes,
        max_steps =     max_steps,
        **kwargs
    )