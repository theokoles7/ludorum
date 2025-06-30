"""# ludorum.agents

This package defines various RL agent classes.
"""

__all__ =   [   
                # Agent parser registration.
                "register_agent_parsers",
                
                # Abstract agent class.
                "Agent",
                
                # Concrete agent classes.
                "QLearning",
                
                # Agent modules.
                "q_learning"
            ]

# Argument registration.
from agents.__args__    import  register_agent_parsers

# Abstract agent class.
from agents.__base__    import  Agent

# Agent classes.
from agents.q_learning  import  QLearning

# Agent modules.
from agents             import  (
                                    q_learning
                                )