"""# ludorum.commands.play"""

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
    # Load environment.
    _environment_:  Environment =   load_environment(
                                        environment =   environment,
                                        **kwargs
                                    )
        
    # Load agent.
    _agent_:        Agent =         load_agent(
                                        agent =         agent,
                                        action_space =  _environment_.action_space(),
                                        state_space =   _environment_.state_space(),
                                        **kwargs
                                    )
        
    # Return game play results.
    return _agent_._train_(
        environment =   _environment_,
        episodes =      episodes,
        max_steps =     max_steps
    )