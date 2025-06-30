"""# ludorum.environments.grid_world.components.squares.base

Defines the basic square component of the Grid World grid.
"""

from typing import Any, Dict, Optional, Tuple

class Square():
    """# (Grid World) Square
    
    Basic square representation.
    """
    
    def __init__(self,
        row:    int,
        column: int,
        value:  Optional[float] =   -0.01
    ):
        """# Instantiate Square.

        ## Args:
            * row       (int):      Row in which square is located within grid.
            * column    (int):      Column in which square is located within grid.
            * value     (float):    Reward yielded from collecting coin. Defaults to -0.01.
        """
        # Define properties.
        self._column_:      int =   column
        self._row_:         int =   row
        self._terminal_:    bool =  False
        self._value_:       float = value
        self._visitations_: int =   0
        self._walkable_:    bool =  True
        
    # PROPERTIES ===================================================================================
    
    @property
    def column(self) -> int:
        """# Column

        Column in which square is located within grid.
        """
        return self._column_
    
    @property
    def coordinate(self) -> Tuple[int, int]:
        """# Coordinate

        Row, column coordinate at which square is located within grid.
        """
        return self.row, self.column
    
    @property
    def is_terminal(self) -> bool:
        """# (Square) is Terminal?

        Flag indicating if square represents a terminal state for the environment.
        """
        return self._terminal_
    
    @property
    def row(self) -> int:
        """# Row

        Row in which square is located within grid.
        """
        return self._row_
    
    @property
    def value(self) -> float:
        """# Value

        Reward yielded/penalty incurred by interacting with square.
        """
        return self._value_
    
    @property
    def visitations(self) -> int:
        """# Visitations

        Count of how many times agent has visited square.
        """
        return self._visitations_
        
    # METHODS ======================================================================================
    
    def interact(self) -> Tuple[float, Optional[Tuple[int, int]], bool, Dict[str, Any]]:
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
        return self.value, self.coordinate, self.is_terminal, {"event": "landed on empty square"}
    
    # DUNDERS ======================================================================================
    
    def __repr__(self) -> str:
        """Object Representation
        
        ## Returns:
            * str:  Object representation of Square.
        """
        return f"<Square(row = {self.row}, column = {self.column})>"
    
    def __str__(self) -> str:
        """# Glyph

        ## Returns:
            * str:  Glyph representation of Square.
        """
        return " "