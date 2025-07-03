"""# ludorum.agents.q_learning.commands.play.args

Argument definitions and parsing for Q-Learning agent's play command.
"""

__all__ = ["register_play_parser"]

from argparse       import _ArgumentGroup, ArgumentParser, _SubParsersAction

from environments   import register_environment_parsers

def register_play_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Q-Learning Play Argument Parser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's sub-parser object.
    """
    # Initialize parser.
    _parser_:       ArgumentParser =    parent_subparser.add_parser(
        name =          "play",
        help =          "Play a game.",
        description =   """Execute episode game play with q-learning agent."""
    )
    
    # Initialize sub-parser.
    _subparser_:    _SubParsersAction = _parser_.add_subparsers(
        dest =          "environment",
        help =          """Environment (game) that the agent will play."""
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+
    
    # CONTROL ======================================================================================
    
    _control_:      _ArgumentGroup =    _parser_.add_argument_group(title = "Control")
    
    _control_.add_argument(
        "--episodes",
        dest =      "episodes",
        type =      int,
        default =   100,
        help =      """Episodes for which agent will play game."""
    )
    
    _control_.add_argument(
        "--max-steps",
        dest =      "max_steps",
        type =      int,
        default =   100,
        help =      """Maximum number of steps that agent is allowed to take in an individual 
                    episode."""
    )

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+
    
    # Register environment parsers.
    register_environment_parsers(parent_subparser = _subparser_)