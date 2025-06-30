"""# ludorum.agents.base

This module provides the base class for all agents in the Lucidium framework.
"""

__all__ = ["Agent"]

from abc        import ABC, abstractmethod
from logging    import Logger
from typing     import Any

class Agent(ABC):
    """# Abstract Agent Class
    
    This class defines the base structure for an agent that can interact with an environment. It 
    requires the implementation of methods to choose actions, save models, and load models.
    
    ## Attributes:
        * action_space  (any):  Actions possible within environment.
        * state_space   (any):  Quantification of possible states in which the environment can be 
                                observed.
        
    ## Methods:
        * select_action(state: Any) -> Any:     Choose an action based on the current state of the 
                                                environment.
        * save_model(path: str)     -> None:    Save the agent's model to the specified path.
        * load_model(path: str)     -> None:    Load the agent's model from the specified path.
    """
    
    def __init__(self,
        action_space:   Any,
        state_space:    Any,
        **kwargs
    ):
        """# Initialize agent.

        ## Args:
            * action_space  (Any):  Actions possible within environment.
            * state_space   (Any):  Quantification of possible states in which the environment can 
                                    be observed.
        """
        # Declare logger member.
        self.__logger__:        Logger
        
        # Define action and state space dimensions.
        self._action_space_:    Any =   action_space
        self._state_space_:     Any =   state_space
        
    @abstractmethod
    def act(self,
        state:  Any
    ) -> any:
        """# Act.

        Agent action is the first critical step in any reinforcement learning loop.

        Given the current state of the environment, the agent decides on an action to perform.

        ## Args:
            * state (Any):  Current environment state.

        ## Returns:
            * Any:  Chosen action.
        """
        pass
    
    @abstractmethod
    def observe(self,
        new_state:  Any,
        reward:     float,
        done:       bool
    ) -> None:
        """# Observe.
        
        Agent observation is the third critical step in any reinforcement learning loop.
        
        After the agent has submitted its action, the environment will return the new state, 
        the reward, and a flag indicating if the agent has reached a terminal state. The 
        agent will use this information to update its parameters accordingly.

        ## Args:
            * new_state (Any):      State of environment after action was submitted.
            * reward    (float):    Reward yielded/penalty incurred by action submitted to 
                                    environment.
            * done      (bool):     Flag indicating if new state is terminal.
        """
        pass