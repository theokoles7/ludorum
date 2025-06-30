"""# ludorum.environments.grid_world.components.squares.goal

Defines the goal square component of the Grid World grid.
"""

from typing                                                 import Any, Dict, override, Optional, Tuple

from termcolor                                              import colored

from environments.grid_world.components.squares.__base__    import Square

class Goal(Square):
    """# (Grid World) Goal

    Goal square class.
    """
    
    def __init__(self,
        row:    int,
        column: int,
        value:  Optional[float] =   1.0
    ):
        """# Instantiate Goal Square.

        ## Args:
            * row       (int):      Row in which square is located within grid.
            * column    (int):      Column in which square is located within grid.
            * value     (float):    Reward yielded from interacting with goal square. Defaults to 
                                    +1.0.
        """
        # Instantiate square.
        super(Goal, self).__init__(row = row, column = column, value = value)
        
        # Override properties.
        self._terminal_:    bool =  True
        
    # METHODS ======================================================================================
    
    @override
    def interact(self) -> Tuple[float, Tuple[int, int], bool, Dict[str, Any]]:
        """# Interact

        ## Returns:
            * Tuple[float, Tuple[int, int]]:
                * Step penalty
                * Square's location
                * Flag indicating if square is terminal state
        """
        # Increment visitations.
        self._visitations_ += 1
        
        # Return value and location.
        return self.value, self.coordinate, self.is_terminal, {"event": "won (reached goal square)"}
    
    # DUNDERS ======================================================================================
    
    @override
    def __repr__(self) -> str:
        """Object Representation
        
        ## Returns:
            * str:  Object representation of Square.
        """
        return f"<Loss(row = {self.row}, column = {self.column})>"
    
    @override
    def __str__(self) -> str:
        """# Glyph

        ## Returns:
            * str:  Glyph representation of Square.
        """
        return colored(text = "◯", color = "green")