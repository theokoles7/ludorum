"""Drive application."""

from json       import dumps

from commands   import play_game
from utils      import ARGS, BANNER, LOGGER

if __name__ == "__main__":
    """Execute command."""
    
    try:# Log banner
        LOGGER.info(BANNER)
        
        # Match command
        match ARGS.command:
            
            # Commence game play
            case "play-game":   LOGGER.info(dumps(obj = play_game(**vars(ARGS)), indent = 2, default = str))
            
            # Invalid command
            case _:             LOGGER.error(f"Invalid command provided: {ARGS.command}")
    
    # Catch wildcard errors
    except Exception as e:  LOGGER.critical(f"Unexpected error caught in main process: {e}", exc_info = True)
    
    # Exit gracefully
    finally:                LOGGER.info("Exiting...")