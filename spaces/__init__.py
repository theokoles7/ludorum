"""# ludorum.spaces

Defines various space definitions for actions and observations.
"""

__all__ =   [
                # Abstract space.
                "Space",
                
                # Composite space.
                "Composite",
                
                # Continuous spaces.
                "Continuous",
                "MultiContinuous",
                
                # Discrete spaces.
                "Discrete",
                "MultiDiscrete"
            ]

# Abstract space.
from spaces.__base__            import Space

# Composite space.
from spaces.composite           import Composite

# Continuous spaces.
from spaces.continuous          import Continuous
from spaces.multi_continuous    import MultiContinuous

# Discrete spaces.
from spaces.discrete            import Discrete
from spaces.multi_discrete      import MultiDiscrete