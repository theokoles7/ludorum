"""# ludorum.environments.grid_world.components.squares.wall

Defines the wall square component of the Grid World grid.
"""

from typing                                                 import Any, Dict, override, Optional, Tuple

from environments.grid_world.components.squares.__base__    import Square

class Wall(Square):
    """# (Grid World) Wall

    Wall square class.
    """
    
    def __init__(self,
        row:    int,
        column: int,
        value:  Optional[float] =   -0.1
    ):
        """# Instantiate Wall Square.

        ## Args:
            * row       (int):      Row in which square is located within grid.
            * column    (int):      Column in which square is located within grid.
            * reward    (float):    Penalty incurred for colliding with wall. Defaults to -0.1.
        """
        # Instantiate square.
        super(Wall, self).__init__(row = row, column = column, value = value)
        
        # Override walkable property.
        self._walkable_:    bool =  False
        
    # METHODS ======================================================================================
    
    @override
    def interact(self) -> Tuple[float, None, bool, Dict[str, Any]]:
        """# Interact

        ## Returns:
            * Tuple[float, Tuple[int, int]]:
                * Step penalty
                * None, because walls are not walkable
        """
        # Increment visitations.
        self._visitations_ += 1
        
        # Return value and location.
        return self.value, None, self.is_terminal, {"event": "collided with wall"}
    
    # DUNDERS ======================================================================================
    
    @override
    def __repr__(self) -> str:
        """Object Representation
        
        ## Returns:
            * str:  Object representation of Square.
        """
        return f"<Wall(row = {self.row}, column = {self.column})>"
    
    @override
    def __str__(self) -> str:
        """# Glyph

        ## Returns:
            * str:  Glyph representation of Square.
        """
        return "█"