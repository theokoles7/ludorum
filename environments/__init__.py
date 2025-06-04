"""# ludorum.environments

This package defines various types of reinforcement learning environments, focusing on games.

Game environments can be categorized into different categories based on their action and state space 
definitions, such as discrete or continuous, as well as how many agents/players the game requires, 
etc. Each category has its own unique features for which testing an agent may be more preferable.
"""

__all__ =   [
                # Environment parser registration.
                "register_environment_parsers",
                
                # Abstract Environment.
                "Environment",
                
                # Environment classes.
                "GridWorld",
                
                # Environment modules.
                "grid_world"
            ]

# Argument registration.
from environments.__args__      import  register_environment_parsers

# Abstract environment class.
from environments.__base__      import  Environment

# Environment classes.
from environments.grid_world    import  GridWorld

# Environment modules.
from environments               import  (
                                            grid_world
                                        )