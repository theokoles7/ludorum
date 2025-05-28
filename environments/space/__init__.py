"""# ludorum.environments.space

This package defines various types of spaces used to simulate action/observation spaces of 
environments.
"""

__all__ =   [
                "BoxSpace",
                "DiscreteSpace",
                "Space"
            ]

from environments.space.__base__    import Space

from environments.space.box         import BoxSpace
from environments.space.discrete    import DiscreteSpace