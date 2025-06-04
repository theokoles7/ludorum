"""# ludorum.agents.nlm

This package implements the Neural Logic Machine proposed in the 2019 paper by Honghua Dong et. al.
"""

__all__ =   [
                # Agent class.
                "NeuralLogicMachine",
                
                # Agent layers.
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

# Parser registration.
from agents.nlm.__args__    import register_nlm_parser

# Agent class.
from agents.nlm.__base__    import NeuralLogicMachine

# Main process.
from agents.nlm.__main__    import main

# Agent layer components.
from agents.nlm.layers      import *