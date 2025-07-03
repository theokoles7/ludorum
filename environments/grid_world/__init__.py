"""# ludorum.environments.grid_world

Grid World environment package.
"""

__all__ =   [
                # Environment.
                "GridWorld",
                
                # Argument parse registration.
                "register_grid_world_parser"
            ]

# Environment.
from environments.grid_world.__base__   import GridWorld

# Argument parse registration.
from environments.grid_world.__args__   import register_grid_world_parser

# Register environment.
from environments.registry              import register_environment
register_environment(name = "grid-world", constructor = GridWorld)