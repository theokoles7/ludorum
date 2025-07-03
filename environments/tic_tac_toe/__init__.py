"""# ludorum.environments.tic_tac_toe

Tic-Tac-Toe environment package.
"""

__all__ =   [
                # Environment.
                "TicTacToe",
                
                # Argument parser registration.
                "register_tic_tac_toe_parser"
            ]

# Environment.
from environments.tic_tac_toe.__base__  import TicTacToe

# Argument parser registration.
from environments.tic_tac_toe.__args__  import register_tic_tac_toe_parser

# Register environment.
from environments.registry              import register_environment
register_environment(name = "tic-tac-toe", constructor = TicTacToe)