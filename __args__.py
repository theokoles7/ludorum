"""# ludorum.args

Ludorum argument definitions & parsing.
"""

__all__ = ["parse_ludorum_arguments"]

from argparse   import ArgumentParser, _ArgumentGroup, Namespace, _SubParsersAction

from agents     import register_agent_parsers

def parse_ludorum_arguments() -> Namespace:
    """# Parse Ludorum Arguments.
    
    This function should be called at the entry point of the Ludorum application. The name space of 
    argument keys and values that it provides will be passed/provided to subsequent module entry 
    points.
    
    ## Returns:
        * NameSpace:    Name space of parsed arguments and their values.
    """
    # Initialize primary parser
    _parser_:       ArgumentParser =    ArgumentParser(
        prog =          "ludorum",
        description =   """Suite of environments, models, & methods in pursuit of achieving organic 
                        reasoning & logic by means of deep reinforcement learning."""
    )

    # Initialize sub-parser
    _subparser_:    _SubParsersAction = _parser_.add_subparsers(
        dest =          "command",
        help =          "Ludorum commands."
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+

    # LOGGING ======================================================================================
    _logging_:      _ArgumentGroup =    _parser_.add_argument_group(
        title =         "Logging",
        description =   "Logging configuration."    
    )

    _logging_.add_argument(
        "--logging-level",
        type =          str,
        choices =       ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL", "NOTSET"],
        default =       "INFO",
        help =          """Minimum logging level (DEBUG < INFO < WARNING < ERROR < CRITICAL). 
                        Defaults to "INFO"."""
    )

    _logging_.add_argument(
        "--logging-path",
        type =          str,
        default =       "logs",
        help =          """Path at which logs will be written. Defaults to "./logs/"."""
    )

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+

    # Register command parsers.
    register_agent_parsers(parent_subparser =   _subparser_)

    # Parse arguments
    return _parser_.parse_args()