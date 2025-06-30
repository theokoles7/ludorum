"""# ludorum.environments.grid_world.components.squares.loss

Defines the loss square component of the Grid World grid.
"""

from typing                                                 import Any, Dict, override, Optional, Tuple

from termcolor                                              import colored

from environments.grid_world.components.squares.__base__    import Square

class Loss(Square):
    """# (Grid World) Loss

    Loss square class.
    """
    
    def __init__(self,
        row:    int,
        column: int,
        value:  Optional[float] =   -1.0
    ):
        """# Instantiate Loss Square.

        ## Args:
            * row       (int):      Row in which square is located within grid.
            * column    (int):      Column in which square is located within grid.
            * value     (float):    Penalty incurred for interacting with loss square. Defaults to 
                                    -1.0.
        """
        # Instantiate square.
        super(Loss, self).__init__(row = row, column = column, value = value)
        
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
        return self.value, self.coordinate, self.is_terminal, {"event": "lost (reached loss square)"}
    
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
        return colored(text = "◯", color = "red")