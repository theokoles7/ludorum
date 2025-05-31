"""Base Environment implementation."""

__all__ = ["Environment"]

from abc        import ABC
from logging    import Logger

class Environment(ABC):
    """Base Environment class."""
    
    def __init__(self, **kwargs):
        """Initialize base Environment object."""
        # Declare logger member.
        self.__logger__:        Logger
        
        # Declare attributes and their types.
        self._actions_:     dict[int, dict[str, str | tuple]]
        self._state_size_:  int
        
    def action_space(self) -> int:
        """# Provide size of environment's action space.

        ## Returns:
            * int:  Size of environment's action space.
        """
        # Return size of action space.
        return len(self._actions_)
    
    def state_space(self) -> tuple[int]:
        """# Provide dimensions of environment's state space.

        ## Returns:
            * tuple[int]: Dimensions of environment's state space.
        """
        # Return dimensions of state space.
        return self._state_size_