"""# ludorum.agents.q_learning.main"""

from logging                    import Logger

from agents.q_learning.actions  import *
from utilities                  import get_child

def main(
    action: str,
    **kwargs
) -> None:
    """# Execute Q-Learning Action.

    ## Args:
        * action    (str):  Q-Learning action being executed.
    """
    # Initialize logger.
    _logger_:       Logger =            get_child(
                                            logger_name =   "q-learning.main"
                                        )
    
    # Define mapping of actions to their respective entry points.
    _actions_:  dict[str, callable] =   {
                                            "play": play.main
                                        }
    
    try:# Execute action.
        _actions_[action](**kwargs)
    
    except Exception as e:  _logger_.critical(f"Unexpected error caught: {e}", exc_info = True)