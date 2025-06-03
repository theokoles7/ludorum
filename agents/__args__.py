"""# ludorum.agents.__args__

This module handles the registration of agent parsers defined in sub-packages.
"""

from argparse   import _SubParsersAction

from agents.nlm import register_nlm_parser

def register_agent_parsers(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Register Agent Parsers.

    ## Args:
        * parent_subparser  (_SubParsersAction): Parent's sub-parsers object.
    """
    # Register agent parsers.
    register_nlm_parser(parent_subparser =  parent_subparser)