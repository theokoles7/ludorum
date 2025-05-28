"""# ludorum.environments.space.discrete"""

__all__ = ["DiscreteSpace"]

from numpy                          import int64
from torch                          import long, tensor, Tensor

from environments.space.__base__    import Space

class DiscreteSpace(Space):
    """# Discrete Space.

    Discrete space representing finite set of non-negative integers.
    
    ## Mathematical Definition:
        * S = {0, 1, 2, ..., n-1} ⊂ ℤ₊
        * |S| = n (finite cardinality)
        
    ## Common Use Cases:
        * Action spaces for discrete control (move up/down/left/right)
        * Categorical state representations (room numbers, discrete positions)
        * Classification outputs (class indices)
        
    ## Tensor Representation:
        Elements are converted to long tensors for use with neural networks, particularly for 
        embedding layers and categorical distributions.
        
    ## Attributes:
        * n     (int):      Number of discrete values {0, ..., n-1}.
        * shape (tuple):    Always () for scalar discrete values.
        * dtype (np.dtype): Always np.int64 for integer representation.
        
    ## Example:
    >>> action_space = Discrete(4)  # Actions: {0, 1, 2, 3}
    >>> assert 2 in action_space
    >>> assert -1 not in action_space
    >>> assert 4 not in action_space
    >>> action = action_space.sample()  # Random action
    >>> action_tensor = action_space.to_tensor(action)  # Long tensor
    """
    
    def __init__(self,
        n:  int
    ):
        """# Initialize discrete space.

        ## Args:
            * n (int):  Number of discrete values (must be positive).
        """
        # Assert that n is a positive integer.
        assert isinstance(n, int),  f"Expected n to be integer, got {type(n)}"
        assert n > 0,               f"Expected positive value for n parameter, got {n}"
        
        # Initialize space.
        super(DiscreteSpace, self).__init__(shape = (), data_type = int64)
        
        # Define n.
        self._n_:   int =   n
        
    def __eq__(self,
        other: any
    ) -> bool:
        """# Evaluate equality with another Discrete space object.

        ## Args:
            * other (any):  Discrete space object being compared.

        ## Returns:
            * bool:
                * True:     Discrete spaces have identical ranges.
                * False:    Discrete spaces do not have identical ranges, or 'other' is not a 
                            Discrete space.
        """
        # Return equality evaluation.
        return isinstance(other, DiscreteSpace) and self._n_ == other._n_
    
    def __repr__(self) -> str:
        """# Provide string format of Discrete space.

        ## Returns:
            * str:  String format of Discrete space.
        """
        # Return string format.
        return f"DiscreteSpace(n = {self._n_})"
        
    def contains(self,
        x:  int
    ) -> bool:
        """# Test if x ∈ {0, 1, ..., n-1}.

        ## Args:
            * x (int):  Integer value to search for.

        ## Returns:
            * bool:
                * True:     x ∈ S
                * False:    x ∉ S
        """
        # Indicate if x is an integer in space range.
        return isinstance(x, int) and 0 <= x < self._n_
    
    def from_tensor(self,
        tensor: Tensor
    ) -> int:
        """# Convert tensor back to discrete integer.

        ## Args:
            * tensor    (Tensor):   Scalar tensor containing integer value.

        ## Returns:
            * int:  Integer from tensor.
            
        ## Raises:
            * ValueError:   If tensor format is invalid or value is out of range.
        """
        # Raise error if not a scalar tensor.
        if tensor.numel() != 1:             raise ValueError(f"Expected scalar tensor, got shape {tensor.shape}")
        
        # Extract value from tensor.
        value:  int =   int(tensor.item())
        
        # Raise error if value is out of range of space.
        if not self.contains(x = value):    raise ValueError(f"Tensor value {value} is not in Discrete({self._n_})")
        
        # Return tensor value.
        return value
    
    def to_tensor(self,
        x:  int
    ) -> Tensor:
        """# Convert discrete integer to long tensor.

        ## Args:
            * x (int):  Integer value within space range.

        ## Returns:
            * Tensor:   Scalar long tensor containing x.
            
        ## Raises:
            * ValueError:   x ∉ S
        """
        # Raise error if x ∉ S.
        if not self.contains(x = x): raise ValueError(f"Value {x} is not in Discrete({self._n_})")
        
        # Return tensor containing x.
        return tensor(data = x, dtype = long)
    
    def sample(self) -> int:
        """# Provide uniform sample of [0, n - 1].

        ## Returns:
            * int:  Random integer in [0, n - 1].
        """
        # Return random integer from space range.
        return self._random_state_.randint(low = 0, high = self._n_)