"""Argument definitions and parsing for rendering environment states."""

from argparse                                   import _ArgumentGroup, ArgumentParser, _SubParsersAction

from utilities.arguments.environment_parsers    import *

def add_render_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Add render command arguments to parent's subparser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's subparser object.
    """
    # Initialize Grid World game parser
    _parser_:       ArgumentParser =    parent_subparser.add_parser(
        name =      "render",
        help =      """Render the visualization of an environment."""
    )
    
    _subparser_:    _SubParsersAction = _parser_.add_subparsers(
        dest =      "environment",
        help =      """Environment to render."""
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+
    
    # Add environment parsers.
    add_grid_world_parser(parent_subparser =    _subparser_)