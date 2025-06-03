"""# ludorum.agents.nlm

This package implements the Neural Logic Machine proposed in the 2019 paper by Honghua Dong et. al.
"""

__all__ =   [
                # Agent class.
                "NeuralLogicMachine",
                
                # Agent components.
                "DimensionExpander",
                "DimensionPermutation",
                "DimensionReducer",
                "LinearLayer",
                "LogicLayer",
                "MLPLayer",
                
                # Main process.
                "main",
                
                # Parser registration.
                "register_nlm_parser"
            ]

# Agent class.
from agents.nlm.__base__            import NeuralLogicMachine

# Agent layer components.
from agents.nlm.layers.expander     import DimensionExpander
from agents.nlm.layers.permutation  import DimensionPermutation
from agents.nlm.layers.reducer      import DimensionReducer
from agents.nlm.layers.linear       import LinearLayer
from agents.nlm.layers.logic        import LogicLayer
from agents.nlm.layers.mlp          import MLPLayer

# Parser registration.
from agents.nlm.__args__            import register_nlm_parser

# Main process.
from agents.nlm.__main__            import main