"""SARSA agent parser & argument definitions."""

__all__ = ["add_sarsa_learning_parser"]

from argparse   import ArgumentParser, _SubParsersAction

def add_sarsa_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Add SARSA agent arguments to parent's subparser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's subparser object.
    """
    # Initialize SARSA Agent parser
    _parser_:   ArgumentParser =    parent_subparser.add_parser(
        name =      "sarsa",
        help =      "sarsa agent (Value-based > Tabular-based)."
    )
    
    # Define SARSA Agent arguments
    _parser_.add_argument(
        "--learning-rate",
        type =      float,
        default =   0.1,
        help =      "Agent's learning rate for value updates. Defaults to 0.1."
    )
    
    _parser_.add_argument(
        "--discount-rate",
        type =      float,
        default =   0.99,
        help =      "Discount factor for future rewards. Defaults to 0.99."
    )
    
    _parser_.add_argument(
        "--exploration-rate",
        type =      float,
        default =   1.0,
        help =      "Exploration rate for epsilon-greedy policy. Defaults to 1.0."
    )