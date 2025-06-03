"""# ludorum.agents.nlm.layers.DimensionExpander"""

__all__ = ["DimensionExpander"]

from torch                  import Tensor
from torch.nn               import Module

from agents.nlm.__util__    import broadcast

class DimensionExpander(Module):
    """# Dimension Expander

    Captures a free variable into predicates, implemented by broadcast.
    
    Adapted from : https://github.com/google/neural-logic-machines/blob/master/difflogic/nn/neural_logic/modules/dimension.py
    """
    
    def __init__(self,
        dimension:  int
    ):
        """# Initialize Dimension Expander.

        ## Args:
            * dimension (int):  Dimension along which expansion will occur.
        """
        # Initialize module.
        super(DimensionExpander, self).__init__()
        
        # Define dimension.
        self._dimension_:   int =   dimension
        
    def forward(self,
        inputs: Tensor,
        n:      int | None =    None
    ) -> Tensor:
        """# Expand Input.
        
        Expand input tensor by unsqueezing it along the specified dimension.

        ## Args:
            * inputs    (Tensor):               Input tensor being expanded.
            * n         (int | None, optional): Size to which dimension will be expanded. Required 
                                                if dimension is zero. Defaults to None.

        ## Returns:
            * Tensor:   Expanded tensor.
        """
        # If dimension is zero...
        if self._dimension_ == 0:
            
            # Assert that `n` is provided.
            assert n is not None,   f"N parameter must be provided when dimension is zero."
            
        # Otherwise, default to size of respective input dimension.
        n:          int =   inputs.size(dim = self._dimension_) if n is None else n
        
        # Add extra dimension for broadcasting.
        dimension:  int =   self._dimension_ + 1
        
        # Return expanded tensor.
        return  broadcast(
                    tensor =    inputs.unsqueeze(dim = dimension),
                    dimension = dimension,
                    size =      n
                )
        
    def get_output_dimension(self,
        input_dimension:    int
    ) -> int:
        """# Get Output Dimension.
        
        Get output dimension after expansion (same as input dimension in this case).

        ## Args:
            * input_dimension   (int):  Input dimension.

        ## Returns:
            * int:  Output dimension, which in the case of the expander, is the same as the input.
        """
        # Simply return input.
        return input_dimension