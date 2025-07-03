"""# ludorum.agents.q_learning.commands.args

Tis module handles the registration of the Q-Learning agent command argument parsers.
"""

from argparse   import _SubParsersAction

def register_command_parsers(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Q-Learning Agent Command Parsers.

    ## Args:
        * parent_subparser  (_SubParsersAction): Parent's sub-parsers object.
    """
    # Deferred agent parser imports.
    from agents.q_learning.commands.play    import register_play_parser

    # Register agent parsers.
    register_play_parser(parent_subparser =   parent_subparser)