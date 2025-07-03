"""# ludorum.agents.components.q_table

Defines the structure and operations of the Q-Table.
"""

from collections    import defaultdict
from json           import dump, load
from pathlib        import Path
from typing         import Any, Dict, Hashable, List, Literal, Tuple, Union

from numpy          import argmax, array, asarray, float64, full, max as np_max, ndarray, zeros
from numpy.random   import uniform

from spaces         import Discrete

class QTable():
    """# Q-Table
    
    Structure for tracking action "qualities" for basic agents.    
    """
    
    def __init__(self,
        action_space:       Union[int, Discrete],
        bootstrap_method:   Literal["zeros", "random", "small-random", "optimistic"] =  "zeros"
    ):
        """# Instantiate Q-Table.

        ## Args:
            * action_space      (int | Discrete):   Actions that table needs to represent.
            * bootstrap_method  (str):              Method by which table will be bootstrapped. 
                                                    Defaults to "zeros".
        """
        # Assert that action space is either an integer or a discrete space.
        assert isinstance(action_space, (int, Discrete)), f"Invalid action space type provided: {type(action_space)}"
        
        # Define properties.
        self._action_space_:        int =                       action_space                        \
                                                                if isinstance(action_space, int)    \
                                                                else action_space.n
                                                            
        # Define bootstrap method.
        self._bootstrap_method_:    str =                       bootstrap_method
        
        # Initialize table.
        self._table_:               Dict[Tuple, List[float]] =  defaultdict(self._bootstrap_)
        
    # METHODS ======================================================================================
    
    def deserialize(self,
        data:   Dict[Any, List[float]]
    ) -> None:
        """# Deserialize Dictionary to Table."""
        # For each key: value in dictionary...
        for k, v in data.items():
            
            # Read into table.
            self._table_[k] = array(v, dtype = float64)
    
    def get_best_action(self,
        state:  Union[Tuple[Union[int, float], ...], int]
    ) -> int:
        """# Get Bast Action.
        
        Get the highest quality action for the given state.

        ## Args:
            * state (Union[Tuple[Union[int, float], ...], int]):    State being evaluated.

        ## Returns:
            * int:  Highest quality action for state.
        """
        return int(argmax(self[state]))
    
    def get_best_value(self,
        state:  Union[Tuple[Union[int, float], ...], int]
    ) -> float:
        """# Get Best Value.

        ## Args:
            * state (Union[Tuple[Union[int, float], ...], int]):    State being evaluated.

        ## Returns:
            * float:    Highest action value found for state.
        """
        return np_max(self[state])
    
    def load(self,
        path:   Union[str, Path]
    ) -> None:
        """# Load Table.

        ## Args:
            * path  (Union[str, Path]): Path from which table will be loaded.
        """
        # Open file for reading.
        with Path(path).open("r", encoding = "utf-8") as file_in:
            
            # Load table.
            self.deserialize(data = load(file_in))
    
    def save(self,
        path:   Union[str, Path]
    ) -> None:
        """# Save Table.

        ## Args:
            * path  (Union[str, Path]): Path at which table will be saved.
        """
        # Ensure path is proper.
        path:   Path =  Path(path)
        
        # Create directories if they dont exist.
        path.parent.mkdir(parents = True, exist_ok = True)
        
        # Open file for writing.
        with Path(path).open(mode = "w", encoding = "utf-8") as file_out:
            
            # Write table to file.
            dump(self.serialize(), fp = file_out)
    
    def serialize(self) -> Dict[Any, List[float]]:
        """# Serialize Table to Dictionary."""
        return {k: v.tolist() for k, v in self._table_.items()}
        
    # HELPERS ======================================================================================
    
    def _bootstrap_(self) -> ndarray:
        """# Bootstrap (Q-)Table.

        ## Args:
            * bootstrap_method  (str):  Method by which table will be bootstrapped.

        ## Returns:
            * ndarray:  Matrix registry of action values for given state.
        """
        # Match bootstrap method.
        match self._bootstrap_method_:
            
            # Zeros.
            case "zeros":           return zeros(shape = self._action_space_, dtype = float64)
            
            # Optimistic.
            case "optimistic":      return full(shape = self._action_space_, fill_value = 1.0, dtype = float64)
            
            # Random.
            case "random":          return uniform(low = -1.0, high = 1.0, size = self._action_space_).astype(float64)
            
            # Small Random.
            case "small-random":    return uniform(low = -0.1, high = 0.1, size = self._action_space_).astype(float64)
            
            # Invalid method.
            case _:     raise ValueError(f"Invalid bootstrap method provided: {self._bootstrap_method_}")
            
    def _normalize_state_(self,
        state:  Union[int, List, Tuple, ndarray]
    ) -> Hashable:
        """# Normalize State.

        ## Args:
            * state (Union[int, List, Tuple, ndarray]): State provided by agent.

        ## Returns:
            * Hashable: Hashable representation of unique state.
        """
        return tuple(asarray(state).flatten().astype(float64))
            
    # DUNDERS ======================================================================================
    
    def __contains__(self,
        state:  Union[Tuple[Union[int, float], ...], int]
    ) -> bool:
        """# Table Contains State?

        ## Args:
            * state (Union[Tuple[Union[int, float], ...], int]):    State being searched for.

        ## Returns:
            * bool: True if state exists in table.
        """
        return self._normalize_state_(state = state) in self._table_
    
    def __getitem__(self,
        state:  Union[Tuple[Union[int, float], ...], int]
    ) -> ndarray:
        """# Get Action Values.

        ## Args:
            * state (Union[Tuple[Union[int, float], ...], int]):    State whose action value(s) is 
                                                                    being fetched.

        ## Returns:
            * ndarray:  State's action value(s).
        """
        return self._table_[self._normalize_state_(state = state)]
    
    def __len__(self) -> int:
        """# Table Length.

        ## Returns:
            * int:  Number of states currently represented by table.
        """
        return len(self._table_)
    
    def __setitem__(self,
        key:    Tuple[Union[Tuple[Union[int, float], ...], int], int],
        value:  float
    ) -> None:
        """# Set Action Value.

        ## Args:
            * key:
                * Tuple[Union[Tuple[Union[int, float], ...], int]:  State index.
                * int:                                              Action index.
            * value (float):                                        Value being assigned at state, 
                                                                    action index.
        """
        self._table_[self._normalize_state_(state = key[0])][key[1]] = value