"""# ludorum.agents.args

This module handles the registration of agent parsers defined in sub-packages.
"""

from argparse   import _SubParsersAction

def register_agent_parsers(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Agent Parsers.

    ## Args:
        * parent_subparser  (_SubParsersAction): Parent's sub-parsers object.
    """
    # Deferred agent parser imports.
    from agents.nlm         import register_nlm_parser
    from agents.q_learning  import register_q_learning_parser

    # Register agent parsers.
    register_nlm_parser(parent_subparser =          parent_subparser)
    register_q_learning_parser(parent_subparser =   parent_subparser)