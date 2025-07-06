"""# ludorum.environments.tic_tac_toe.components.cell

This module defines the individual cell structure in a Tic-Tac-Toe board.
"""

__all__ = ["Cell"]

from typing                                         import Tuple, Union

from torch                                          import Tensor

from environments.tic_tac_toe.components.players    import Player

class Cell():
    """# (Tic-Tac-Toe) Cell
    
    Individual cell component within a Tic-Tac-Toe board.
    """
    
    def __init__(self,
        row:    int,
        column: int,
        player: Union[int, str, Player] =   0
    ):
        """# Instantiate Cell.

        ## Args:
            * row       (int):                  Row in which cell is located.
            * column    (int):                  Column in which cell is located.
            * player    (int | str | Player):   Initial player value. Defaults to zero (no player).
        """
        # Define coordinates.
        self._row_:     int =   row
        self._column_:  int =   column
        
        # Define player.
        self._set_player_(player = player)
        
        
    # PROPERTIES ===================================================================================
    
    @property
    def column(self) -> int:
        """# (Cell) Column

        Column in which cell is located.
        """
        return self._column_
    
    @property
    def coordinate(self) -> Tuple[int, int]:
        """# (Cell) Coordinate

        Coordinate of cell within board.
        """
        return self._row_, self._column_
    
    @property
    def is_empty(self) -> bool:
        """# (Cell) is Empty?
        
        Indicate if cell is empty or has an entry.
        """
        return self._player_ == Player.EMPTY
    
    @property
    def onehot(self) -> Tensor:
        """(Player) One-Hot Encoding.

        One-hot encoding representation of cell's player entry.
        """
        return self._player_.onehot
    
    @property
    def player(self) -> int:
        """# (Current) Player Entry

        The current player occupying cell, if any.
        """
        return self._player_.number
    
    @property
    def row(self) -> int:
        """# (Cell) Row

        Row in which cell is located.
        """
        return self._row_
    
    # METHODS ======================================================================================
    
    def mark(self,
        player: int
    ) -> bool:
        """# Mark (Cell).
        
        Enter player's move into cell, if empty.

        ## Args:
            * player    (int):  +1 for player or -1 for opponent.

        ## Returns:
            * bool: True if move was made.
        """
        # If cell is not empty, move cannot be made.
        if not self.is_empty: return False
        
        # Set cell.
        self._set_player_(player = player)
    
    def reset(self) -> None:
        """# Reset (Cell).

        Reset cell to initial state.
        """
        self._player_:  Player =    Player.EMPTY
                                    
    # HELPERS ======================================================================================
        
    def _set_player_(self,
        player: Union[Player, int, str]
    ) -> None:
        """# Set Player.

        ## Args:
            * player    (Player | int | str): Player being entered into cell.
        """
        # Match player type.
        match player:
            
            # Object.
            case Player() as p: self._player_:  Player =    p
            
            # Number value.
            case int() as n:    self._player_:  Player =    Player.from_number(number = n)
            
            # Symbol value.
            case str() as s:    self._player_:  Player =    Player.from_symbol(symbol = s)
            
            # Invalid type.
            case _: raise TypeError(f"Invalid player type provided: {type(player)}")
    
    # DUNDERS ======================================================================================
    
    def __repr__(self) -> str:
        """# Object Representation

        Object representation of cell.
        """
        return f"<Cell(row = {self._row_}, column = {self._column_}, player = {self._player_})>"
    
    def __str__(self) -> str:
        """# String Representation

        String representation of cell.
        """
        return str(self._player_)