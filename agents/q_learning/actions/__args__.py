"""# ludorum.agents.q_learning.actions.args

Handle registration of Q-Learning action parsers.
"""

from argparse   import _SubParsersAction

def register_action_parsers(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Action Parsers.

    ## Args:
        * parent_subparser  (_SubParsersAction): Parent's sub-parsers object.
    """
    # Deferred action parser imports.
    from agents.q_learning.actions.play.__args__    import register_play_parser
    
    # Register action parsers.
    register_play_parser(parent_subparser = parent_subparser)