"""# ludorum.environments.tic_tac_toe.base

Tic-Tac-Toe environment interface.
"""

from random                                     import choice
from typing                                 import Any, Dict, List, override, Optional, Tuple, Union

from numpy                                  import int8
from numpy.typing                           import NDArray
from torch                                  import Tensor

from agents                                 import Agent
from environments.__base__                  import Environment
from environments.tic_tac_toe.components    import Board
from spaces                                 import Box, Discrete

class TicTacToe(Environment):
    """# Tic-Tac-Toe (Environment)
    
    Environment interface for interacting with the Tic-Tac-Toe game.
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
        """# Instantiate Tic-Tac-Toe (Environment).

        ## Args:
            * size          (int):      Dimension of (square) tic-tac-toe board. Defaults to 3.
            * win_reward    (float):    Reward yielded if agent wins game. Defaults to 1.0.
            * loss_penalty  (float):    Penalty incurred if agent loses game. Defaults to -1.0.
            * draw_penalty  (float):    Penalty incurred if game ends in draw. Defaults to -0.5.
            * step_penalty  (float):    Penalty incurred each time agent makes a move. Defaults to 
                                        -0.1.
        """
        # Initialize game board.
        self._board_:               Board =     Board(**{k: v for k, v in locals().items() if k != "self"})
        self._size_:                int =       size
        
        # Define action & observation spaces.
        self._action_space_:        Discrete =  Discrete(n = self._size_ ** 2)
        self._observation_space_:   Box =       Box(
                                                    lower = -1,
                                                    upper = 1,
                                                    shape = (self._size_, self._size_),
                                                    dtype = int8
                                                )
        
    # PROPERTIES ===================================================================================
    
    @property
    def array(self) -> NDArray:
        """# (Board) to NDArray.

        One-hot encoded array of board state.
        """
        return self._board_.array
    
    @override
    @property
    def action_space(self) -> Discrete:
        """# (Tic-Tac-Toe) Action Space.

        Space representing discrete actions value zero through the square of the size of the board 
        minus 1.
        """
        return self._action_space_
    
    @override
    @property
    def done(self) -> bool:
        """# Is Game Over?

        True if game has a winner or ended in draw.
        """
        return self._board_.has_winner or self._board_.is_draw
    
    @property
    def name(self) -> str:
        """# (Environment) Name.

        Name of environment.
        """
        return "Tic-Tac-Toe"
    
    @override
    @property
    def observation_space(self) -> Box:
        """# (Tic-Tac-Toe) Observation Space.

        Space representing the shape of environment state observations.
        """
        return self._observation_space_
    
    @property
    def tensor(self) -> Tensor:
        """# (Board) to Tensor.

        One-hot encoded tensor of board state.
        """
        return self._board_.tensor
    
    # METHODS ======================================================================================
    
    @override
    def reset(self) -> NDArray:
        """# Reset Environment.

        ## Returns:
            * NDArray:  State of environment after reset.
        """
        return self._board_.reset()
    
    @override
    def step(self,
        action: Union[int, Tuple[int, int]]
    ) -> Tuple[float, NDArray, bool, Dict[str, Any]]:
        """# Step.
        
        ## Args:
            * action    (int | Tuple[int, int]):    Action to be taken in the environment.
        
        ## Returns:
            * Tuple[Any, float, bool, Dict]:
                - float:    Reward received/penalty incurred
                - NDArray:  Next state of the environment
                - bool:     Done flag indicating if the episode has ended
                - Dict:     Additional information
        """
        # Match action data type.
        match action:
            
            # Integer.
            case int() as a:    reward, state, done, info = self._board_.make_move_by_action(action = a)
            
            # Tuple.
            case tuple() as a:  reward, state, done, info = self._board_.make_move(row = a[0], column = a[1])
            
            # Invalid action.
            case _:             raise TypeError(f"Action expected to be integer or coordinate, got {type(action)}")
            
        # If game is not over, opponent takes turn.
        if not done: self._board_.make_move_by_action(action = choice(self._board_.valid_actions))
        
        # Return actin results.
        return reward, state, done, info
    
    # DUNDERS ======================================================================================
    
    def __repr__(self) -> str:
        """# Object Representation

        Object representation of environment.
        """
        return f"<TicTacToe(size = {self._size_}, done = {self.done})>"
    
    def __str__(self) -> str:
        """# String Representation

        String representation of environment.
        """
        return str(self._board_)