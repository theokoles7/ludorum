"""Primary CLI argument definitions & parsing."""

__all__ = ["ARGS"]

from argparse                       import ArgumentParser, _ArgumentGroup, Namespace, _SubParsersAction

from utils.arguments.command_args   import *

# Initialize primary parser
_parser:    ArgumentParser =    ArgumentParser(
    prog =          "ludorum",
    description =   """Suite of environments, models, & methods in pursuit of achieving organic 
                    reasoning & logic by means of deep reinforcement learning."""
)

# Initialize sub-parser
_subparser: _SubParsersAction = _parser.add_subparsers(
    dest =          "command",
    help =          "Ludorum commands."
)

# +================================================================================================+
# | BEGIN ARGUMENTS                                                                                |
# +================================================================================================+

# INPUT ============================================================================================
_input:     _ArgumentGroup =    _parser.add_argument_group(
    title =         "Input",
    description =   "Input/dataset directory configuration."
)

_input.add_argument(
    "--input-directory",
    type =          str,
    default =       "input",
    help =          """Directory under which datasets/input data can be located. Defaults to 
                    "./input/"."""
)

# LOGGING ==========================================================================================
_logging:   _ArgumentGroup =    _parser.add_argument_group(
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

# OUTPUT ===========================================================================================
_output:    _ArgumentGroup =    _parser.add_argument_group(
    title =         "Output",
    description =   "Output/reporting directory configuration."
)

_output.add_argument(
    "--output-directory",
    type =          str,
    default =       "output",
    help =          """Directory under which reports/output data can be located. Defaults to 
                    "./output/"."""
)

# Add command parsers
add_game_parser(parent_subparser =  _subparser)

# +================================================================================================+
# | END ARGUMENTS                                                                                  |
# +================================================================================================+

# Parse arguments
ARGS:       Namespace =         _parser.parse_args()