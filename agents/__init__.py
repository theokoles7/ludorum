"""# ludorum.agents

This package defines various types of reinforcement learning agents.

Agents can be categorized into different types based on their learning strategies, such as 
value-based, policy-based, and model-based methods. Each type has its own strengths and weaknesses, 
and the choice of agent depends on the specific requirements of the task and environment.
"""

__all__ =   [
                # Abstract Agent.
                "Agent",
                
                # Value-Based Agents.
                "QLearning"
            ]

from agents.__base__        import Agent

from agents.q_learning      import QLearning