"""Drive application."""

from argparse   import Namespace
from logging    import Logger

from __args__   import parse_ludorum_arguments
from agents     import nlm
from commands   import *
from utilities  import BANNER, get_logger

if __name__ == "__main__":
    """Execute command."""
    
    # Parse Ludorum arguments.
    _arguments_:    Namespace =             parse_ludorum_arguments()
    
    # Initialize logger.
    _logger_:       Logger =                get_logger(
                                                logger_name =   "ludorum",
                                                logging_level = _arguments_.logging_level,
                                                logging_path =  _arguments_.logging_path
                                            )
    
    # Define mapping of commands to their respective entry points.
    _commands_:     dict[str, callable] =   {
                                                "nlm":  nlm.main
                                            }
    
    try:# Log banner
        _logger_.info(BANNER)
        
        # Execute command provided.
        _commands_[_arguments_.command](_arguments_)
    
    # Catch wildcard errors
    except Exception as e:  _logger_.critical(
                                f"Unexpected error caught: {e}",
                                exc_info = (_arguments_.logging_level == "DEBUG")
                            )
    
    # Exit gracefully
    finally:                _logger_.info("Exiting...")