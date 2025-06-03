"""# ludorum.agents

This package defines various types of reinforcement learning agents.

Agents can be categorized into different types based on their learning strategies, such as 
value-based, policy-based, and model-based methods. Each type has its own strengths and weaknesses, 
and the choice of agent depends on the specific requirements of the task and environment.
"""

__all__ =                   [
                                # Agent parser registration.
                                "register_agent_parsers",
                                
                                # Agent Loader.
                                "load_agent",
                                
                                # Abstract Agent.
                                "Agent",
                                
                                # Value-Based Agents.
                                "QLearning"
                            ]

from agents.__args__        import register_agent_parsers
from agents.__base__        import Agent

from agents.nlm             import *
from agents.q_learning      import QLearning


# Define agent loader function.
def load_agent(
    agent:          str,
    action_space:   any,
    state_space:    any,
    **kwargs
) -> Agent:
    """# Load Agent
    
    Initialize and provide agent based on selection and parameters.

    ## Args:
        * agent         (str):  Agent selection. For a full list of options, refer to ludorum.agents 
                                package or documentation.
        * action_space  (int):  Number of possible actions that the agent can take.
        * state_space   (int):  Dimensions of the environment in which the agent will act.

    ## Returns:
        * Agent:    Initialized agent, based on selection and keyword arguments.
    """
    from logging            import Logger
    
    from utilities          import get_child
    
    # Initialize logger.
    __logger__: Logger =    get_child("agent-loader")
    
    # Log action for debugging.
    __logger__.debug(f"Loading agent: {agent} ({kwargs})")
    
    # Match agent selection.
    match agent:
        
        # Q-Learning
        case "q-learning":  return  QLearning(
                                        action_space =  action_space,
                                        state_space =   state_space,
                                        **kwargs
                                    )
        
        # Invalid agent selection.
        case _:             raise ValueError(f"Invalid agent selected: {agent}")