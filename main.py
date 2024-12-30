"""Drive application."""

from utils  import ARGS, BANNER, LOGGER

if __name__ == "__main__":
    """Execute command."""
    
    # Execute provided command
    try:
        
        # Log banner
        LOGGER.info(BANNER)
    
    # Catch wildcard errors
    except Exception as e:  LOGGER.critical(f"Unexpected error occurred: {e}")
    
    # Exit gracefully
    finally:                LOGGER.info("Exiting...")