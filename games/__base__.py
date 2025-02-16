"""Base Environment implementation."""

__all__ = ["Environment"]

from logging    import Logger

class Environment():
    """Base Environment class."""
    
    def __init__(self):
        """Initialize base Environment object."""
        # Declare attributes and their types
        self.__logger__:        Logger
        self.__actions__:       dict[int, dict[str, str | tuple]]
        self.__state_size__:    tuple[int]
        
    def action_size(self) -> int:
        """# Provide size of environment's action space.

        ## Returns:
            * int:  Size of environment's action space.
        """
        # Return size of action space
        return len(self.__actions__)
    
    def state_size(self) -> tuple[int]:
        """# Provide dimensions of environment's state space.

        ## Returns:
            * tuple[int]: Dimensions of environment's state space.
        """
        # Return dimensions of state space
        return self.__state_size__