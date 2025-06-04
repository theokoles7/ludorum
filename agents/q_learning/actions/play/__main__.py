"""# ludorum.agents.q_learning.actions.play.main"""

__all__ = ["main"]

from argparse                                   import Namespace
from logging                                    import Logger

from agents.q_learning.actions.play.processes   import *
from utilities                                  import get_child

def main(
    environment:    str,
    **kwargs
) -> None:
    """# Execute Q-Learning Game Play.

    ## Args:
        * environment   (str):  Environment in/with which agent will play.
    """
    # Initialize logger.
    _logger_:       Logger =            get_child(
                                            logger_name =   "q-learning.play.main"
                                        )
    
    # Define mapping of environment processes to their respective entry points.
    _actions_:  dict[str, callable] =   {
                                            "grid-world":   play_grid_world.main
                                        }
    
    try:# Execute action.
        _actions_[environment](**kwargs)
    
    except Exception as e:  _logger_.critical(f"Unexpected error caught: {e}", exc_info =   True)