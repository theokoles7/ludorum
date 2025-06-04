"""# ludorum.commands.args

This module handles the registrations of command parsers defined in sub-packages.
"""

from argparse   import _SubParsersAction

def register_command_parsers(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Command Parsers.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's sub-parsers object.
    """
    # Deferred command parser imports.
    from commands.render    import register_render_parser
    
    # Register command parsers.
    register_render_parser(parent_subparser =   parent_subparser)