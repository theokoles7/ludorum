"""# ludorum.environments.tic_tac_toe.components.glyphs

This module provides the players for the Tic Tac Toe environment.
"""

__all__ = ["Player"]

from enum           import Enum

from torch          import equal, tensor, Tensor

class Player(Enum):
    """(Tic-Tac-Toe) Glyph

    This enumeration defines the players used to represent the Tic Tac Toe environment.
    """
    
    EMPTY = {"number":  0, "symbol": " ", "onehot": tensor((1, 0, 0))}
    X     = {"number":  1, "symbol": "X", "onehot": tensor((0, 1, 0))}
    O     = {"number": -1, "symbol": "O", "onehot": tensor((0, 0, 1))}
    
    # PROPERTIES ===================================================================================
    
    @property
    def number(self) -> int:
        """# (Player) Number

        Integer value of the player: +1 (X), -1 (O), or 0 (empty).
        """
        return self.value["number"]
    
    @property
    def onehot(self) -> Tensor:
        """# (Player) One-Hot Encoding.

        One-hot encoding representation of player.
        """
        return self.value["onehot"]
    
    @property
    def symbol(self) -> str:
        """# (Player) Symbol

        Symbolic representation of the player (e.g., 'X', 'O').
        """
        return self.value["symbol"]
    
    # CLASS METHODS ================================================================================
    
    @classmethod
    def from_number(cls,
        number:  int
    ) -> "Player":
        """# (Player) from Value

        Return the player corresponding to the given numeric value.

        ## Args:
            * number    (int):  +1 for player or -1 for opponent.

        ## Raises:
            * ValueError:   If player number is not known.

        ## Returns:
            * Player:   Player initialized from value.
        """
        # For each defined player...
        for player in cls:
            
            # If it matches the value provided, return that player.
            if player.number == number: return player
            
        # Otherwise, report invalid player number.
        raise ValueError(f"No player found with number {number}")
    
    @classmethod
    def from_onehot(cls,
        encoding: Tensor
    ) -> "Player":
        """# (Player) from One-Hot Encoding.

        ## Args:
            * onehot    (Tensor):  One-hot encoding representation of player.

        ## Raises:
            * ValueError:   If player encoding is not known.

        ## Returns:
            * Player:   Player initialized from one-hot encoding.
        """
        # For each defined player...
        for player in cls:
            
            # If it matches the value provided, return that player.
            if equal(player.onehot, encoding): return player
            
        # Otherwise, report invalid player number.
        raise ValueError(f"No player found with encoding {encoding}")
    
    @classmethod
    def from_symbol(cls,
        symbol: str
    ) -> "Player":
        """# (Player) from Symbol

        Return the player corresponding to the given symbol value.

        ## Args:
            * symbol    (str):  "X" for player or "O" for opponent.

        ## Raises:
            * ValueError:   If player symbol is not known.

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