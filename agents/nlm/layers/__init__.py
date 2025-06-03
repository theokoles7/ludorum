"""# ludorum.agents.nlm.layers

This package defines the various layer components of the Neural Logic Machine.
"""

__all__ =   [
                "DimensionExpander",
                "DimensionPermutation",
                "DimensionReducer",
                "LinearLayer",
                "LogicLayer",
                "MLPLayer"
            ]

from agents.nlm.layers.expander     import DimensionExpander
from agents.nlm.layers.permutation  import DimensionPermutation
from agents.nlm.layers.reducer      import DimensionReducer
from agents.nlm.layers.linear       import LinearLayer
from agents.nlm.layers.logic        import LogicLayer
from agents.nlm.layers.mlp          import MLPLayer