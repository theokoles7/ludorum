"""Game parser & argument definitions."""

__all__ = ["add_game_parser"]

from argparse                   import ArgumentParser, _SubParsersAction

from utils.arguments.game_args  import *

def add_game_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Add parser/arguments for running a game play process.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's sub-parser.
    """
    # Initialize parser
    _parser_:       ArgumentParser =    parent_subparser.add_parser(
        name =      "play-game",
        help =      "Execute game play process."
    )
    
    # Initialize sub-parser
    _subparser_:    _SubParsersAction = _parser_.add_subparsers(
        dest =      "game",
        help =      "Game being played."
    )
    
    # Add game arguments
    _parser_.add_argument(
        "--episodes",
        type =      int,
        default =   100,
        help =      """Episodes for which agent will play game. Defaults to 100."""
    )
    
    _parser_.add_argument(
        "--max-steps",
        type =      int,
        default =   100,
        help =      """Maximum amount of steps that agent is allowed to make within each game 
                    episode. Defaults to 100."""
    )
    
    # Add game parsers
    add_grid_world_parser(parent_subparser =    _subparser_)