"""Ludorum application argument definitions and parsing."""

from argparse                       import ArgumentParser, _ArgumentGroup, Namespace, _SubParsersAction

from utilities.arguments.commands   import *

# Initialize primary parser
_parser_:       ArgumentParser =    ArgumentParser(
    prog =          "ludorum",
    description =   """Suite of environments, models, & methods in pursuit of achieving organic 
                    reasoning & logic by means of deep reinforcement learning."""
)

# Initialize sub-parser
_subparser_:    _SubParsersAction = _parser_.add_subparsers(
    dest =          "command",
    help =          "Ludorum commands."
)

# +================================================================================================+
# | BEGIN ARGUMENTS                                                                                |
# +================================================================================================+

# LOGGING ==========================================================================================
_logging:       _ArgumentGroup =    _parser_.add_argument_group(
    title =         "Logging",
    description =   "Logging configuration."    
)

_logging.add_argument(
    "--logging-level",
    type =          str,
    choices =       ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
    default =       "INFO",
    help =          """Minimum logging level (DEBUG < INFO < WARNING < ERROR < CRITICAL). Defaults 
                    to "INFO"."""
)

_logging.add_argument(
    "--logging-path",
    type =          str,
    default =       "logs",
    help =          """Path at which logs will be written. Defaults to "./logs/"."""
)

# +================================================================================================+
# | END ARGUMENTS                                                                                  |
# +================================================================================================+

# Add commands.
add_play_parser(    parent_subparser =      _subparser_)
add_render_parser(  parent_subparser =    _subparser_)

# Parse arguments
ARGS:       Namespace =         _parser_.parse_args()