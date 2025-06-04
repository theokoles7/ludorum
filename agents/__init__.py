"""# ludorum.agents

This package defines various types of reinforcement learning agents.

Agents can be categorized into different types based on their learning strategies, such as 
value-based, policy-based, and model-based methods. Each type has its own strengths and weaknesses, 
and the choice of agent depends on the specific requirements of the task and environment.
"""

__all__ =                   [
                                # Agent parser registration.
                                "register_agent_parsers",
                                
                                # Abstract Agent.
                                "Agent",
                                
                                # Agent classes.
                                "NeuralLogicMachine",
                                "QLearning",
                                
                                # Agent modules.
                                "nlm",
                                "q_learning"
                            ]

# Argument registration.
from agents.__args__        import  register_agent_parsers

# Abstract agent class.
from agents.__base__        import  Agent

# Agent classes.
from agents.nlm             import  NeuralLogicMachine
from agents.q_learning      import  QLearning

# Agent modules.
from agents                 import  (
                                        nlm,
                                        q_learning
                                    )