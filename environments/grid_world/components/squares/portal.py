"""# ludorum.environments.grid_world.components.squares.portal

Defines the portal square component of the Grid World grid.
"""

from typing                                                 import Any, Dict, override, Optional, Tuple

from environments.grid_world.components.squares.__base__    import Square

class Portal(Square):
    """# (Grid World) Portal

    Portal square class.
    """
    
    def __init__(self,
        row:    int,
        column: int,
        exit:   Tuple[int, int],
        value:  Optional[float] =   -0.01
    ):
        """# Instantiate Portal Square.

        ## Args:
            * row       (int):      Row in which square is located within grid.
            * column    (int):      Column in which square is located within grid.
            * value     (float):    Penalty incurred by entering portal. Defaults to -0.01.
            * value     (float):    Coordinate at which agent will appear after interacting 
                                    (entering) portal. Defaults to 0.5.
        """
        # Instantiate square.
        super(Portal, self).__init__(row = row, column = column, value = value)
        
        # Define properties.
        self._exit_:    Tuple[int, int] =   exit
        
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
        return self.value, self._exit_, self.is_terminal, {"event": f"entered portal to {self._exit_}"}
    
    # DUNDERS ======================================================================================
    
    @override
    def __repr__(self) -> str:
        """Object Representation
        
        ## Returns:
            * str:  Object representation of Square.
        """
        return f"<Portal(row = {self.row}, column = {self.column}, exit = {self._exit_})>"
    
    @override
    def __str__(self) -> str:
        """# Glyph

        ## Returns:
            * str:  Glyph representation of Square.
        """
        return "░"