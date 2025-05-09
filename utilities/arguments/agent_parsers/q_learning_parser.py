"""Argument definitions and parsing for Q-Learning agent."""

__all__ = ["add_q_learning_parser"]

from argparse   import ArgumentParser, _SubParsersAction

def add_q_learning_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Add Q-Learning agent sub-parser & arguments to parent's sub-parser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's sub-parser object.
    """
    # Initialize Q-Learning Agent parser.
    _parser_:   ArgumentParser =    parent_subparser.add_parser(
        name =      "q-learning",
        help =      "Q-Learning agent."
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+

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

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+