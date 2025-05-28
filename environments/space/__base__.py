"""ludorum.environments.space.__base__"""

__all__ = ["Space"]

from abc            import ABC, abstractmethod
from typing         import Union

from numpy          import dtype, float32
from numpy.random   import RandomState
from torch          import Tensor

class Space(ABC):
    """# Abstract space.
    
    Defines the mathematical structure and computational interface that all spaces must implement. 
    Follows OpenAI Gym space conventions while adding research-focused features like tensor 
    conversion and mathematical validation.
    """
    
    def __init__(self,
        shape:      tuple[int] =        (),
        data_type:  Union[dtype, str] = float32
    ):
        """# Initialize action/observation space.

        ## Args:
            * shape (tuple[int]):   Dimensional specifications for space.
            * dtype (dtype | str):  Data type of elements within space.
        """
        # Define attributes.
        self._shape_:           tuple[int] =    shape
        self._dtype_:           dtype =         dtype(data_type)
        
        # Initialize random state generator.
        self._random_state_:    RandomState =   RandomState()
        
    def __contains__(self,
        x:  any
    ) -> bool:
        """# Wrapper to accommodate Python 'in' operator.

        ## Args:
            * x (any):  Element to search for.

        ## Returns:
            * bool: True if element is contained in space, False otherwise.
        """
        return self.contains(x = x)
    
    def __repr__(self) -> str:
        """# Provide string format of space.

        ## Returns:
            * str:  String format of space.
        """
        return f"{self.__class__.__name__}(shape = {self._shape_}, dtype = {self._dtype_})"
        
    @abstractmethod
    def contains(self,
        x:  any
    ) -> bool:
        """# Test if x ∈ S.

        ## Args:
            * x (any):  Element to search for.

        ## Returns:
            * bool:
                * True:     x ∈ S
                * False:    x ∉ S
        """
        pass
    
    @abstractmethod
    def from_tensor(self,
        tensor: Tensor
    ) -> any:
        """# Convert tensor to space element.

        ## Args:
            * tensor    (Tensor):   Tensor in expected format.

        ## Returns:
            * any:  Element in space's native format.
            
        ## Raises:
            * ValueError:   Tensor cannot be converted to valid space element.
        """
        pass
    
    @abstractmethod
    def to_tensor(self,
        x:  any
    ) -> Tensor:
        """# Convert space element to tensor representation.

        ## Args:
            * x (any):  Element from this space (must satisfy x ∈ S).

        ## Returns:
            * Tensor:   Tensor representation of x.
            
        ## Raises:
            * ValueError:   x ∉ S.
        """
        pass
    
    @abstractmethod
    def sample(self) -> any:
        """# Generate a uniformly random element from space.

        ## Returns:
            * any:  Random space element.
        """
        pass
    
    def seed(self,
        seed:   int =   None
    ) -> None:
        """# Set random seed for reproducibile sampling.

        ## Args:
            * seed  (int, optional):    Random seed value. Defaults to None for system entropy.
        """
        self._random_state_:    RandomState =   RandomState(seed = seed)