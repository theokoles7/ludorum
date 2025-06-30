"""# ludorum.environments.args

This module handles the registration of environment parsers defines in sub-packages.
"""

from argparse                   import  _SubParsersAction

def register_environment_parsers(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Environment Parsers.

    ## Args:
        * parent_subparser  (_SubParsersAction): Parent's sub-parsers object.
    """
    # Deferred environment parser imports.
    from environments.grid_world    import register_grid_world_parser
    
    # Register environment parsers.
    register_grid_world_parser(parent_subparser = parent_subparser)