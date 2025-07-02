"""# ludorum.environments.tic_tac_toe.components.glyphs

This module provides the players for the Tic Tac Toe environment.
"""

__all__ = ["Player"]

from enum   import Enum

class Player(Enum):
    """(Tic-Tac-Toe) Glyph

    This enumeration defines the players used to represent the Tic Tac Toe environment.
    """
    
    EMPTY = {"number":  0, "symbol": " "}
    X     = {"number":  1, "symbol": "X"}
    O     = {"number": -1, "symbol": "O"}
    
    # PROPERTIES ===================================================================================
    
    @property
    def symbol(self) -> str:
        """# (Player) Symbol

        Symbolic representation of the player (e.g., 'X', 'O').
        """
        return self.value["symbol"]
    
    @property
    def number(self) -> int:
        """# (Player) Number

        Integer value of the player: +1 (X), -1 (O), or 0 (empty).
        """
        return self.value["number"]
    
    # CLASS METHODS ================================================================================
    
    @classmethod
    def from_number(cls,
        number:  int
    ) -> "Player":
        """# (Player) from Value

        Return the player corresponding to the given numeric value.

        ## Args:
            * number    (int):  +1 for player or -1 for opponent.

        ## Returns:
            * Player:   Player initialized from value.
        """
        # For each defined player...
        for player in cls:
            
            # If it matches the value provided, return that player.
            if player.number == number: return player
            
        # OTherwise, report invalid player number.
        raise ValueError(f"No player found with number {number}")
    
    @classmethod
    def from_symbol(cls,
        symbol: str
    ) -> "Player":
        """# (Player) from Symbol

        Return the player corresponding to the given symbol value.

        ## Args:
            * symbol    (str):  "X" for player or "O" for opponent.

        ## Returns:
            * Player:   Player initialized from symbol.
        """
        # For each defined player...
        for player in cls:
            
            # If it matches the value provided, return that player.
            if player.symbol == symbol.upper(): return player
            
        # OTherwise, report invalid player number.
        raise ValueError(f"No player found with symbol {symbol}")
    
    # DUNDERS ======================================================================================
    
    def __repr__(self) -> str:
        """# Object Representation.
        
        Return the object representation of the glyph.
        """
        return f"<{self.name}>"
    
    def __str__(self) -> str:
        """# String Representation.
        
        Return the string representation of the glyph.
        """
        return self.symbol