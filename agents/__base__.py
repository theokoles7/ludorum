"""Base agent implementation and structure."""

__all__ = ["Agent"]

from abc        import ABC, abstractmethod
from logging    import Logger

from numpy      import ndarray

class Agent(ABC):
    """Abstract agent class."""
    
    def __init__(self,
        action_space:       int,
        state_space:        tuple[int],
        **kwargs
    ):
        """# Initialize agent.

        ## Args:
            * action_space  (int):          Number of possible actions that the agent can take.
            * state_space   (tuple[int]):   Dimensions of the environment in which the agent will 
                                            act.
        """
        # Declare logger member.
        self.__logger__:        Logger
        
        # Define action and state space dimensions.
        self._action_space_:    int =           action_space
        self._state_space_:     tuple[int] =    state_space
        
    @abstractmethod
    def act(self,
        state:  ndarray
    ) -> int:
        """# Choose an action.
        
        The agent will choose an action based on the environment state provided.

        ## Args:
            * state (ndarray):  Current environment state.

        ## Returns:
            * int:  Chosen action.
        """
        pass
    
    @abstractmethod
    def save_model(self,
        path:   str
    ) -> None:
        """# Save agent's model.

        ## Args:
            * path  (str):  Path at which agent's model will be saved.
        """
        pass
    
    @abstractmethod
    def load_model(self,
        path:   str
    ) -> None:
        """# Load agent model.

        ## Args:
            * path  (str):  Path at which model save file can be located/loaded.
        """
        pass