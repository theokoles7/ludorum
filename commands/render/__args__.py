"""# ludorum.commands.render.args

Argument registration for rendering environment states.
"""

from argparse       import ArgumentParser, _SubParsersAction

from environments   import *

def register_render_parser(
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
    
    # Add environment parsers.
    register_environment_parsers(parent_subparser = _subparser_)