"""# ludorum.agents.q_learning.actions.play.args

Define arguments parser and definitions for `q-learning play` command.
"""

from argparse                           import ArgumentParser, _SubParsersAction

from environments.grid_world.__args__   import register_grid_world_parser

def register_play_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Play Parser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's subparser object.
    """
    # Initialize parser.
    _parser_:       ArgumentParser =    parent_subparser.add_parser(
        name =      "play",
        help =      """Play a game with agent."""
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
        help =      """Episodes for which game play will repeat. Defaults to 100."""
    )
    
    _parser_.add_argument(
        "--max-steps",
        type =      int,
        default =   100,
        help =      """Maximum number of interactions that the agent will be allowed to make with 
                    the environment during each episode. Defaults to 100."""
    )
    
    _parser_.add_argument(
        "--animate",
        dest =      "animate",
        action =    "store_true",
        default =   False,
        help =      """Render animation of agent interacting with environment."""
    )

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+
    
    # Register environment parsers.
    register_grid_world_parser(parent_subparser =   _subparser_)