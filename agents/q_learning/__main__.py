"""# ludorum.agents.q_learning.main"""

from logging                    import Logger

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
    
    try:# Execute action.
        _logger_.debug("Executing Q-Learning action.")
    
    except Exception as e:  _logger_.critical(f"Unexpected error caught: {e}", exc_info = True)