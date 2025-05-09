"""Argument definitions and parsing for Grid World environment."""

__all__ = ["add_grid_world_parser"]

from argparse   import _ArgumentGroup, ArgumentParser, _SubParsersAction

def add_grid_world_parser(
    parent_subparser:   _SubParsersAction
) -> None:
    """# Add Grid World game arguments to parent's subparser.

    ## Args:
        * parent_subparser  (_SubParsersAction):    Parent's subparser object.
    """
    # Initialize Grid World game parser
    _parser_:       ArgumentParser =    parent_subparser.add_parser(
        name =      "grid-world",
        help =      """Grid World is a single player game in which an agent has to navigate from the 
                    start square to the goal square, learning to avoid wall and loss squares."""
    )
    
    _subparser_:    _SubParsersAction = _parser_.add_subparsers(
        dest =      "agent",
        help =      """Agent playing game."""
    )

    # +============================================================================================+
    # | BEGIN ARGUMENTS                                                                            |
    # +============================================================================================+
    
    # BOARD DIMENSIONS =============================================================================
    _dimensions_:   _ArgumentGroup =    _parser_.add_argument_group("Dimensions")
    
    _dimensions_.add_argument(
        "--rows",
        type =      int,
        default =   3,
        help =      """Number of rows with which grid will be initialized. Defaults to 3."""
    )
    
    _dimensions_.add_argument(
        "--columns",
        type =      int,
        default =   4,
        help =      """Number of columns with which grid will be initialized. Defaults to 4."""
    )
    
    # BOARD COMPONENTS =============================================================================
    _components_:   _ArgumentGroup =    _parser_.add_argument_group("Components")
    
    _components_.add_argument(
        "--goal",
        type =      tuple,
        default =   (2, 3),
        help =      """Row, column coordinate at which goal square will be located. Defaults to 
                    (2, 3)."""
    )
    
    _components_.add_argument(
        "--start",
        type =      tuple,
        default =   (0, 0),
        help =      """Coordinate at which agent will begin the game."""
    )
    
    _components_.add_argument(
        "--loss",
        type =      tuple,
        default =   None,
        help =      """Row,column coordinate at which loss sqaure will be located."""
    )
    
    _components_.add_argument(
        "--walls",
        type =      list_of_tuples,
        default =   [],
        help =      """List of row,column coordinates at which wall squares will be loacted."""
    )

    # +============================================================================================+
    # | END ARGUMENTS                                                                              |
    # +============================================================================================+
    
# Define function for parsing list of tuples
def list_of_tuples(
    arg:    str
) -> list[tuple[int]]:
    """# Parse string into list of tuples of integers.

    ## Args:
        * arg   (str):  Argument being passed.

    ## Returns:
        * list[tuple[int]]: List of tuples of integers.
    """
    return [tuple(int(element) for element in coordinate.split(",")) for coordinate in arg.split(" ")]