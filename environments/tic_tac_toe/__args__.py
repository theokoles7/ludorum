"""# ludorum.environments.tic_tac_toe.args

Argument definitions & parsing for Tic-Tac-Toe environment.
"""

__all__ = ["register_tic_tac_toe_parser"]

from argparse   import _ArgumentGroup, ArgumentParser, _SubParsersAction

def register_tic_tac_toe_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Tic-Tac-Toe Parser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's subparser object.
    """
    # Initialize parser
    _parser_:       ArgumentParser =    parent_subparser.add_parser(
        name =          "tic-tac-toe",
        help =          """Tic-Tac-Toe environment.""",
        description =   """Tic-Tac-Toe is a simple, discrete, grid-based environment where an agent 
                        takes turns (with an opponent) entering X's or O's in the grid. The goal is 
                        to get three marks in a row."""
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+
    
    # DIMENSIONS ===================================================================================
    
    _dimensions_:   _ArgumentGroup =    _parser_.add_argument_group("Dimensions")
    
    _dimensions_.add_argument(
        "--size",
        dest =      "size",
        type =      int,
        default =   3,
        help =      """The size of the (square) game grid. Defaults to 3."""
    )
    
    # REWARDS & PENALTIES ==========================================================================
    
    _rewards_:      _ArgumentGroup =    _parser_.add_argument_group("Rewards & Penalties")
    
    _rewards_.add_argument(
        "--win-reward", "--win",
        dest =      "win_reward",
        type =      float,
        default =   1.0,
        help =      """Reward yielded if agent wins game. Defaults to 1.0."""
    )
    
    _rewards_.add_argument(
        "--loss-penalty", "--loss",
        dest =      "loss_penalty",
        type =      float,
        default =   -1.0,
        help =      """Penalty incurred if agent loses game. Defaults to -1.0."""
    )
    
    _rewards_.add_argument(
        "--draw-penalty", "--draw",
        dest =      "draw_penalty",
        type =      float,
        default =   -0.5,
        help =      """Penalty incurred if game ends in a draw. Defaults to -0.5."""
    )
    
    _rewards_.add_argument(
        "--step-penalty", "--cost",
        dest =      "step_penalty",
        type =      float,
        default =   -0.1,
        help =      """Penalty incurred/cost of making a move during game."""
    )

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+