"""Drive application."""

from json       import dumps

from commands   import *
from utilities  import ARGS, BANNER, LOGGER

if __name__ == "__main__":
    """Execute command."""
    
    try:# Log banner
        LOGGER.info(BANNER)
        
        # Match command
        match ARGS.command:
            
            # Play a game with an agent.
            case "play":    LOGGER.info(dumps(obj = play_game(**vars(ARGS)), indent = 2, default = str))
            
            # Render an environment visualization.
            case "render":  render_environment(**vars(ARGS))
            
            # Invalid command
            case _:         LOGGER.error(f"Invalid command provided: {ARGS.command}")
    
    # Catch wildcard errors
    except Exception as e:  LOGGER.critical(f"Unexpected error caught in main process: {e}", exc_info = True)
    
    # Exit gracefully
    finally:                LOGGER.info("Exiting...")