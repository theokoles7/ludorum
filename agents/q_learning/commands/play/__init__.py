"""# ludorum.agents.q_learning.commands.play

This package defines the Q-Learning agent's game play process.
"""

__all__ =   [
                # Entry point.
                "main",
                
                # Argument registration.
                "register_play_parsers"
            ]

# Entry point.
from agents.q_learning.commands.play.__main__   import main

# Argument registration.
from agents.q_learning.commands.play.__args__   import register_play_parser