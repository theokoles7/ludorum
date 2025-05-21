"""Play a game with an agent."""

from agents         import *
from environments   import *

def play_game(
    environment:    str,
    agent:          str,
    episodes:       int =   100,
    max_steps:      int =   100,
    **kwargs
) -> dict:
    """# Execute an agent's episodic game play on an environment.

    ## Args:
        * environment   (str):              Environment with which agent will interact.
        * agent         (str):              Agent playing the game.
        * episodes      (int, optional):    Episodes for which game play will repeat.
        * max_steps     (int, optional):    Maximum number of interactions that the agent will be 
                                            allowed to make with the environment during each 
                                            episode.

    ## Returns:
        * dict: Game play results.
    """
    # Match environment.
    match environment:
        
        # Grid World
        case "grid-world":  _environment_:  Environment =   GridWorld(**kwargs)
        
        # Invalid environment selection.
        case _:             raise ValueError(f"Invalid environment selection: {environment}")
        
    # Match agent.
    match agent:
        
        case "q-learning":  _agent_:        Agent =         QLearning(
                                                                action_space =  _environment_.action_space(),
                                                                state_space =   _environment_.state_space(),
                                                                **kwargs
                                                            )
        
        # Invalid agent selection.
        case _:             raise ValueError(f"Invalid agent selection: {agent}")
        
    # Return game play results.
    return _agent_._train_(
        environment =   _environment_,
        episodes =      episodes,
        max_steps =     max_steps
    )