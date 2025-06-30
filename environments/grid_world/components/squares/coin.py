"""# ludorum.environments.grid_world.components.squares.coin

Defines the coin square component of the Grid World grid.
"""

from typing                                                 import Any, Dict, override, Optional, Tuple

from termcolor                                              import colored

from environments.grid_world.components.squares.__base__    import Square

class Coin(Square):
    """# (Grid World) Coin

    Coin square class.
    """
    
    def __init__(self,
        row:    int,
        column: int,
        value:  Optional[float] =   0.5
    ):
        """# Instantiate Coin Square.

        ## Args:
            * row       (int):      Row in which square is located within grid.
            * column    (int):      Column in which square is located within grid.
            * value     (float):    Reward yielded from collecting coin. Defaults to 0.5.
        """
        # Instantiate square.
        super(Coin, self).__init__(row = row, column = column, value = value)
        
        # Define initial state.
        self._collected_:   bool =  False
        
    # PROPERTIES ===================================================================================
    
    @property
    def collected(self) -> bool:
        """# Collected?

        Flag indicating if coin has been collected.
        """
        return self._collected_
    
    @override
    @property
    def value(self) -> float:
        """# Reward

        Reward yielded from collecting coin.
        """
        return -self._value_ if self.collected else self._value_
    
    # METHODS ======================================================================================
        
    @override
    def interact(self) -> Tuple[float, Tuple[int, int], Dict[str, Any]]:
        """# Interact

        ## Returns:
            * Tuple[float, Tuple[int, int]]:
                * Reward for collecting coin
                * Square's location
        """
        # Increment visitations.
        self._visitations_ += 1
        
        # If coin has already been collected...
        if self.collected:
            
            # Simply return penalty.
            return self.value, self.coordinate, self.is_terminal, {"event": "landed on empty square"}
        
        # Otherwise, store reward.
        value:  float = self.value
            
        # Collect coin.
        self._collect_()
        
        # Return reward for collecting coin.
        return value, self.coordinate, self.is_terminal, {"event": "collected a coin"}
    
    @override
    def reset(self) -> None:
        """# Reset.

        Reset square.
        """
        self._collected_:   bool =  False
        self._visitations_: int =   0
    
    # HELPERS ======================================================================================
    
    def _collect_(self) -> None:
        """# Collect Coin.
        
        Set coin's collected property to True.
        """
        self._collected_:   bool =  True
    
    # DUNDERS ======================================================================================
    
    @override
    def __repr__(self) -> str:
        """Object Representation
        
        ## Returns:
            * str:  Object representation of Square.
        """
        return f"<Coin(row = {self.row}, column = {self.column}, collected = {self.collected})>"
    
    @override
    def __str__(self) -> str:
        """# Glyph

        ## Returns:
            * str:  Glyph representation of Square.
        """
        return " " if self.collected else colored(text = "$", color = "yellow")