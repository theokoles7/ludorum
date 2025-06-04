"""# ludorum.agents.q_learning

This package implements the Q-Learning agent proposed in the 1992 paper by Watkins & Dayan.
"""

__all__ =   [
                # Agent class.
                "QLearning",
                
                # Main process.
                "main",
                
                # Parser registration.
                "register_q_learning_parser"
            ]

# Parser registration.
from agents.q_learning.__args__ import register_q_learning_parser

# Agent class.
from agents.q_learning.__base__ import QLearning

# Main process.
from agents.q_learning.__main__ import main