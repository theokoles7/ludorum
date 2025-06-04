"""# ludorum.environments.grid_world

This package implements the Grid World environment.
"""

__all__ =   [
                # Environment class.
                "GridWorld",
                
                # Parser registration.
                "register_grid_world_parser"
]

# Environment class.
from environments.grid_world.__args__   import register_grid_world_parser

# Environment class.
from environments.grid_world.__base__   import GridWorld