"""Argument definitions and parsing for playing a game."""

from argparse                                   import ArgumentParser, _SubParsersAction

from utilities.arguments.environment_parsers    import *

def add_play_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Add play command arguments to parent's subparser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's subparser object.
    """
    # Initialize Grid World game parser
    _parser_:       ArgumentParser =    parent_subparser.add_parser(
        name =      "play",
        help =      """Execute an agent's episodic game play on an environment."""
    )
    
    _subparser_:    _SubParsersAction = _parser_.add_subparsers(
        dest =      "environment",
        help =      """Environment with which agent will interact."""
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+
    
    _parser_.add_argument(
        "--episodes",
        type =      int,
        default =   100,
        help =      """Episodes for which game play will repeat."""
    )
    
    _parser_.add_argument(
        "--max-steps",
        type =      int,
        default =   100,
        help =      """Maximum number of interactions that the agent will be allowed to make with 
                    the environment during each episode."""
    )

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+
    
    # Add environment parsers.
    add_grid_world_parser(parent_subparser =    _subparser_)