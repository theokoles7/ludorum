"""# ludorum.environments.tic_tac_toe.components.board

This module defines the Tic-Tac-Toe board component structure and validation operations.
"""

__all__ = ["Board"]

from typing                                     import Any, Dict, List, Optional, Tuple

from numpy                                      import array
from numpy.typing                               import NDArray
from torch                                      import stack, Tensor

from environments.tic_tac_toe.components.cell   import Cell

class Board():
    """# (Tic-Tac-Toe) Board
    
    Manages a 2D matrix of grid cells and manages game rules.
    """
    
    def __init__(self,
        # Dimension.
        size:           Optional[int] =     3,
        
        # Rewards/penalties.
        win_reward:     Optional[float] =    1.0,
        loss_penalty:   Optional[float] =   -1.0,
        draw_penalty:   Optional[float] =   -0.5,
        step_penalty:   Optional[float] =   -0.1,
        **kwargs
    ):
        """# Instantiate (Tic-Tac-Toe) Board.

        ## Args:
            * size          (int):      Dimension of (square) tic-tac-toe board. Defaults to 3.
            * win_reward    (float):    Reward yielded if agent wins game. Defaults to 1.0.
            * loss_penalty  (float):    Penalty incurred if agent loses game. Defaults to -1.0.
            * draw_penalty  (float):    Penalty incurred if game ends in draw. Defaults to -0.5.
            * step_penalty  (float):    Penalty incurred each time agent makes a move. Defaults to 
                                        -0.1.
        """
        # Define size.
        self._size_:            int =   size
        
        # Define starting player.
        self._current_player_:  int =   1
        
        # Define rewards/penalties.
        self._win_reward_:      float = win_reward
        self._loss_penalty_:    float = loss_penalty
        self._draw_penalty_:    float = draw_penalty
        self._step_penalty_:    float = step_penalty
        
        # Populate grid.
        self._populate_grid_()
        
    # PROPERTIES ===================================================================================
    
    @property
    def array(self) -> NDArray:
        """# (Board) to NDArray.

        One-hot encoded array of board state.
        """
        return self.tensor.numpy()
    
    @property
    def has_winner(self) -> bool:
        """# (Game) has Winner?

        True if game has ended in a win.
        """
        return self.winner is not None
    
    @property
    def is_draw(self) -> bool:
        """# (Game) is Draw?

        True if board is full and there is no winner.
        """
        return self.is_full and self.winner is None
    
    @property
    def is_full(self) -> bool:
        """# (Board) is Full?

        True if there are no empty cells in grid.
        """
        return all(not cell.is_empty for row in self._grid_ for cell in row)
    
    @property
    def is_over(self) -> bool:
        """# (Game) is Over?
        
        True if game has a winner or ended in draw.
        """
        return self.has_winner or self.is_draw
    
    @property
    def tensor(self) -> Tensor:
        """# (Board) to Tensor.

        One-hot encoded tensor of board state.
        """
        return  stack(
                    [cell.onehot for row in self._grid_ for cell in row]
                ).reshape((self._size_, self._size_, 3), -1)
        
    @property
    def valid_actions(self) -> List[int]:
        """# Valid Actions.

        List of actions that are valid given current board state.
        """
        return [a for a in range(self._size_ ** 2) if self._action_is_valid_(a)]
    
    @property
    def winner(self) -> Optional[int]:
        """# (Game) Winner
        
        Game winner, if a player has won the game.
        """
        # Initialize lines for validation.
        lines:  List[List[Cell]] =  [[self._grid_[r][c] for c in range(self._size_)] for r in range(self._size_)]   +\
                                    [[self._grid_[c][r] for c in range(self._size_)] for r in range(self._size_)]   +\
                                    [[self._grid_[i][i] for i in range(self._size_)]]                               +\
                                    [[self._grid_[i][self._size_ - i - 1] for i in range(self._size_)]]
        
        # For each line...
        for line in lines:
            
            # Compute sum of line.
            total:  int =   sum(cell.player for cell in line)
                
            # Player wins.
            if total ==  self._size_:   return 1
                
            # Opponent wins.
            if total == -self._size_:   return -1
                
        # No winner found.
        return None
        
    # METHODS ======================================================================================
        
    def make_move(self,
        row:    int,
        column: int
    ) -> Tuple[float, NDArray, bool, Dict[str, Any]]:
        """# Make Move.
        
        Make move submitted if it's valid.

        ## Args:
            * row       (int):  Row in which move will be made.
            * column    (int):  Column in which move will be made.
        
        ## Returns:
            * Tuple[Any, float, bool, Dict]:
                - float:    Reward received/penalty incurred
                - ndarray:  Next state of the environment
                - bool:     Done flag indicating if the episode has ended
                - Dict:     Additional information
        """
        # If move is not currently valid, it cannot be made.
        if not self._move_is_valid_(row = row, column = column):
            
            return  (
                        self._step_penalty_,
                        self.array,
                        self.is_over,
                        {"event": "attempted invalid move"}
            )
        
        # Otherwise, mark cell.
        self._grid_[row][column].mark(player = self._current_player_)
        
        # Switch players.
        self._switch_player_()
        
        # Return results.
        return  (
                    self._evaluate_move_(),
                    self.array,
                    self.is_over,
                    {"event": f"made move at ({row}, {column})"}
                )
        
    def make_move_by_action(self,
        action: int
    ) -> Tuple[float, NDArray, bool, Dict[str, Any]]:
        """# Make Move by Action.
        
        Make move submitted if it's valid.

        ## Args:
            * action    (int):  Action being submitted.
        
        ## Returns:
            * Tuple[Any, float, bool, Dict]:
                - float:    Reward received/penalty incurred
                - ndarray:  Next state of the environment
                - bool:     Done flag indicating if the episode has ended
                - Dict:     Additional information
        """
        return  self.make_move(
                    row =       action // self._size_,
                    column =    action  % self._size_
                )
    
    def reset(self) -> NDArray:
        """# Reset (Board).

        Reset board to initial state.
        
        ## Returns:
            * ndarray:  State of board after reset.
        """
        # For each row...
        for row in self._grid_:
            
            # Reset each cell in row.
            for cell in row: cell.reset()
            
        # Reset current player.
        self._current_player_:  int =   1
        
        # Return board state.
        return self.to_ndarray()
        
    def to_ndarray(self) -> NDArray:
        """# (Board) to NDArray.

        ## Returns:
            * ndarray:  2D array representation of current board state.
        """
        return array([[cell.player for cell in row] for row in self._grid_])
        
    # HELPERS ======================================================================================
    
    def _action_is_valid_(self,
        action: int
    ) -> bool:
        """# Action is Valid?

        ## Args:
            * action    (int):  Action being validated.

        ## Returns:
            * bool: True if action is valid.
        """
        return  self._move_is_valid_(
                    row =       action // self._size_,
                    column =    action %  self._size_
                )
    
    def _coordinate_to_state_(self,
        row:    int,
        column: int
    ) -> int:
        """# Coordinate to State.
        
        Convert row, column coordinate to state representation.

        ## Args:
            * row       (int):  Row component of coordinate.
            * column    (int):  Column component of coordinate.

        ## Returns:
            * int:  State representation coordinate.
        """
        return row * self._size_ + column
    
    def _evaluate_move_(self) -> float:
        """# Evaluate (Last) Move.

        ## Returns:
            * float:    Reward yielded/penalty incurred by last move.
        """
        # If game is not over, simply assign step penalty.
        if not self.is_over:    return self._step_penalty_
        
        # If game is a draw, assign draw penalty.
        if self.is_draw:        return self._draw_penalty_
        
        # If opponent won, assign loss penalty.
        if self.winner == -1:   return self._loss_penalty_
        
        # Otherwise, player won, so assign reward.
        if self.winner == 1:    return self._win_reward_
    
    def _is_in_bounds_(self,
        row:    int,
        column: int
    ) -> bool:
        """# (Coordinate) is in Bounds?

        ## Args:
            * row       (int):  Row being validated.
            * column    (int):  Column being validated.

        ## Returns:
            * bool: True is coordinate is in bounds of grid.
        """
        return 0 <= row < self._size_ and 0 <= column < self._size_
    
    def _move_is_valid_(self,
        row:    int,
        column: int
    ) -> bool:
        """# Move is Valid?

        ## Args:
            * row       (int):  Row at which move is being validated.
            * column    (int):  Column at which move is being validated.

        ## Returns:
            bool: True if cell is empty and move can be made.
        """
        # If coordinate is out of bounds, move is not relevant.
        if not self._is_in_bounds_(row = row, column = column): return False
        
        # Otherwise, simply indicate that cell is empty.
        return self._grid_[row][column].is_empty
    
    def _populate_grid_(self) -> None:
        """# Populate Grid.
        
        Initialize the board with empty cells, according to dimension specifications.
        """
        self._grid_:    List[List[Cell]] =  [
                                                [
                                                    Cell(row = r, column = c)
                                                    for c in range(self._size_)
                                                ]   for r in range(self._size_)
                                            ]
        
    def _state_to_coordinate_(self,
        state:  int
    ) -> Tuple[int, int]:
        """# State to Coordinate.
        
        Convert state to coordinate equivalent.

        ## Args:
            * state (int):  State being converted to coordinate.

        ## Returns:
            * Tuple[int, int]:  Coordinate equivalent of state.
        """
        return state // self._size_, state % self._size_
        
    def _switch_player_(self) -> None:
        """# Switch Player.
        
        Alternate current player after moves.
        """
        self._current_player_:  int = -self._current_player_
    
    # DUNDERS ======================================================================================
    
    def __repr__(self) -> str:
        """# Object Representation

        Object representation of board.
        """
        return f"<Board(size = {self._size_})>"
    
    def __str__(self) -> str:
        """# String Representation

        String representation of board.
        """
        # Predefine separation line and column index.
        line:           str =   ("\n   " + ("───┼" * (self._size_ - 1)) + ("─" * 3))
        grid_string:    str =   ("   ") + " ".join(f" {column} " for column in range(self._size_))
        
        # For each row in grid...
        for r, row in enumerate(self._grid_):
            
            # Render cell row.
            grid_string += f"\n {r} " + "│".join(f" {cell} " for cell in row)
            
            # Append line if not on last row.
            grid_string += line if r < self._size_ - 1 else ""
            
        # Return string representation.
        return grid_string