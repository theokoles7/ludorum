"""# ludorum.environments

This package defines various RL environments.
"""

__all__ =   [
                # Abstract environment class.
                "Environment",
                
                # Concrete environment classes.
                "GridWorld",
                
                # Argument parser registration.
                "register_environment_parsers"
            ]

# Abstract environment class.
from environments.__base__      import Environment

# Concerete environment classes.
from environments.grid_world    import GridWorld

# Argument parser registration.
from environments.__args__      import register_environment_parsers