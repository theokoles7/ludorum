"""Execute game play process."""

__all__ = ["play_game"]

from json       import dump
from logging    import Logger
from os         import makedirs

from agents     import *
from games      import Environment, load_game
from utils      import LOGGER, TIMESTAMP

def play_game(
    game:           str,
    agent:          str,
    episodes:       int =   100,
    max_steps:      int =   100,
    output_path:    str =   "output",
    **kwargs
) -> dict:
    """# Execute game play process.

    ## Args:
        * game          (str):              Game being played.
        * agent         (str):              Agent to play game.
        * episodes      (int, optional):    Episodes for which agent will play game. Defaults to 
                                            100.
        * max_steps     (int, optional):    Maximum amount of steps that agent is allowed to make 
                                            within each game episode. Defaults to 100.
        * output_path   (str, optional):    Path at which game report will be written. Defaults to 
                                            "./output/".
                                        
    ## Returns:
        * dict: Game results.
    """
    # Initialize logger
    __logger__:     Logger =    LOGGER.getChild("game-process")

    # Log action
    __logger__.info(f"Commencing game (Game: {game}, Agent: {agent})")
    
    # Define job's output path
    _output_path_:  str =       f"""{output_path}/game-reports/{agent}/{game}/{TIMESTAMP}"""

    # Ensure output path exists
    makedirs(name = _output_path_, exist_ok = True)

    # Load game
    environment:    Environment =   load_game(game = game, **kwargs)
    
    # Match agent to initialize
    match agent:
        
        # Initialize Q-Learning agent
        case "q-learning":  agent:          QLearningAgent =    QLearningAgent(
                                                                    state_size =    environment.state_size(),
                                                                    action_size =   environment.action_size(),
                                                                    **kwargs
                                                                )
        
        # Cases for Double Q-learning, SARSA, Expected SARSA
        case "double q-learning":  agent:          QLearningAgent =    QLearningAgent(
                                                                    state_size =    environment.state_size(),
                                                                    action_size =   environment.action_size(),
                                                                    **kwargs
                                                                )

        case "sarsa":  agent:          QLearningAgent =    QLearningAgent(
                                                                    state_size =    environment.state_size(),
                                                                    action_size =   environment.action_size(),
                                                                    **kwargs
                                                                )

        case "expected-sarsa":  agent:          QLearningAgent =    QLearningAgent(
                                                                    state_size =    environment.state_size(),
                                                                    action_size =   environment.action_size(),
                                                                    **kwargs
                                                                )
        
        # Invalid agent selection
        case _:                             raise ValueError(f"Invalid agent selection: {agent}")
        
    # Play game 
    game_results:   dict =  agent._train_(
                                environment =   environment,
                                episodes =      episodes,
                                max_steps =     max_steps,
                                **kwargs
                            )

    # Save game report
    dump(
        obj =       game_results,
        fp =        open(
                        file  = f"{_output_path_}/game_report.json",
                        mode =  "w"
                    ),
        indent =    2,
        default =   str)

    # Return game results
    return game_results