"""# ludorum.agents.nlm.layers.LogicLayer"""

__all__ = ["LogicLayer"]

from logging                        import Logger

from torch                          import cat, Tensor
from torch.nn                       import Module, ModuleList

from agents.nlm.layers.expander     import DimensionExpander
from agents.nlm.layers.inference    import LogicInferenceLayer
from agents.nlm.layers.permutation  import DimensionPermutation
from agents.nlm.layers.reducer      import DimensionReducer
from utilities                      import get_child

class LogicLayer(Module):
    """# Logic Layer
    
    A logic layer that performs differentiable logic deduction.
    
    Each logic layer computes inference over input predicates by applying logic rules. The logic is 
    performed in two stages: 
    * Expansion/Reduction:      for inter-group deduction
    * Logic model application:  for intra-group deduction
    
    Adapted from: https://github.com/google/neural-logic-machines/blob/master/difflogic/nn/neural_logic/layer.py
    """
    
    def __init__(self,
        breadth:            int,
        input_dimensions:   list[int],
        output_dimensions:  list[int],
        hidden_dimension:   int,
        exclude_self:       bool =      True,
        residual:           bool =      False
    ):
        """# Initialize Logic Layer.

        ## Args:
            * breadth           (int):          The breadth (max order) of the logic layer.
            * input_dimensions  (list[int]):    The number of input channels for each input group.
            * output_dimensions (list[int]):    The number of output channels for each group.
            * hidden_dimension  (int):          The hidden dimension of the logic model.
            * exclude_self      (bool):         Whether to exclude multiple occurrences of the same 
                                                variable in logic deduction.
            * residual          (bool):         Whether to use residual connections for the outputs.
        """
        # Initialize module.
        super(LogicLayer, self).__init__()
        
        # Initialize logger.
        self.__logger__:                Logger =            get_child("logic-layer")
        
        # Assert that breadth is positive.
        assert 0 < breadth, f"Breadth expected to be positive, got {breadth}"
        
        # Warn of performance complications for breadth greater than 3.
        if breadth > 3: self.__logger__.warning(f"Using a breadth greater than 3 may cause performance complications (speed & memory).")
        
        # Define maximum order (degree) of logic.
        self._max_order_:               int =               breadth
        
        # Set residual flag.
        self._residual_:                bool =              residual
        
        # Ensure input and output dimensions are lists of the correct length, being no greater than 
        # max order.
        input_dimensions:               list[int] =             self.make_list(
                                                                    x =     input_dimensions, 
                                                                    n =     self._max_order_ + 1,
                                                                    dtype = int
                                                                )
        output_dimensions:              list[int] =             self.make_list(
                                                                    x =     output_dimensions,
                                                                    n =     self._max_order_ + 1,
                                                                    dtype = int
                                                                )
        
        # Initialize module lists.
        self._logic_:                   ModuleList =            ModuleList()
        self._dimension_permutation_:   ModuleList =            ModuleList()
        self._dimension_expanders_:     ModuleList =            ModuleList()
        self._dimension_reducers_:      ModuleList =            ModuleList()
        
        # For each order of logic prescribed...
        for order in range(self._max_order_ + 1):
            
            # Start with input dimension.
            current_dimension:          int =                   input_dimensions[order]
            
            # For all but the first order...
            if order > 0:
                
                # Initialize expander.
                expander:               DimensionExpander =     DimensionExpander(
                                                                    dimension = order - 1
                                                                )
                
                # Append to expanders list.
                self._dimension_expanders_.append(expander)
                
                # Add expanded dimension.
                current_dimension +=                            expander.get_output_dimension(
                                                                    input_dimension = input_dimensions[order - 1]
                                                                )
            
            # Otherwise, no expansion is needed for first degree.
            else: self._dimension_expanders_.append(None)
            
            # For the next degree...
            if order + 1 < self._max_order_ + 1:
                
                # Define a dimension reducer.
                reducer:                DimensionReducer =      DimensionReducer(
                                                                    dimension =     order + 1,
                                                                    exclude_self =  exclude_self
                                                                )
                
                # Append to reducers list.
                self._dimension_reducers_.append(reducer)
                
                # Add reduced dimension.
                current_dimension +=                            reducer.get_output_dimension(
                                                                    input_dimension = input_dimensions[order + 1]
                                                                )
            
            # Otherwise, no reduction is needed for first degree.
            else: self._dimension_reducers_.append(None)
            
            # For the first order...
            if current_dimension == 0:
                
                # Do no create logic or permutation.
                self._dimension_permutation_.append(None)
                self._logic_.append(None)
                
                # Set output dimension to zero when no logic is applied.
                output_dimensions[order] =                      0
                
            # Otherwise...
            else:
                
                # Create permutation layer for this group.
                permutation:            DimensionPermutation =  DimensionPermutation(
                                                                    dimension = order
                                                                )
                
                # Append to permutation list.
                self._dimension_permutation_.append(permutation)
                
                # Apply permutation to current dimensions.
                current_dimension:      int =                   permutation.get_output_dimension(
                                                                    input_dimension =   current_dimension
                                                                )
                
                # Append logic layer.
                self._logic_.append(LogicInferenceLayer(
                    input_dimension =   current_dimension,
                    output_dimension =  output_dimensions[order],
                    hidden_dimension =  hidden_dimension
                ))
                
        # Define dimensions lists.
        self._input_dimensions_:        list[int] =             input_dimensions
        self._output_dimensions_:       list[int] =             output_dimensions
        
        # If residual connections is specified...
        if self._residual_:
            
            # For each input dimension, add input dimensions to output dimensions for residual.
            for i in range(len(self._input_dimensions_)): self._output_dimensions_[i] += self._input_dimensions_[i]
            
    def forward(self,
        inputs: list[Tensor]
    ) -> list[Tensor]:
        """# Forward Pass.
        
        Forward pass through logic layer.

        ## Args:
            * inputs    (list[Tensor]): List on inputs for each group of the logic layer.

        ## Returns:
            * list[Tensor]: Output from each logic layer group.
        """
        # Assert that the number of inputs matches expected order.
        assert len(inputs) == self._max_order_ + 1, f"Number of input tensors ({len(inputs)} should be {self._max_order_})"
        
        # Initialize list to store outputs.
        outputs:        list[Tensor] =  []
        
        # For each group of logic layer...
        for group in range(self._max_order_ + 1):
            
            # Initialize temporary list to store input of adjacent groups.
            temp:       list[Tensor] =  []
            
            # If not the first group...
            if group > 0 and self._input_dimensions_[group - 1] > 0:
                
                # Reference expansion size.
                n:      int =           inputs[group].size(1) if group == 1 else None
                
                # Append expanded tensor to temporary list.
                temp.append(self._dimension_expanders_[group](inputs[group -1], n))
                
            # If not the last group, and to temporary list.
            if group < len(inputs) and self._input_dimensions_[group] > 0: temp.append(inputs[group])
            
            # Reduce inputs from next group.
            if group + 1 < len(inputs) and self._input_dimensions_[group + 1] > 0: temp.append(self._dimension_reducers_[group](inputs[group + 1]))
            
            # If no inputs were collected, output should be None.
            if len(temp) == 0: output: Tensor = None
            
            # Otherwise...
            else:
                
                # Concatenate all inputs along the last dimension.
                temp =                  cat(tensors = temp, dim = -1)
                
                # Apply permutation to the concatenated inputs.
                temp =                  self._dimension_permutation_[group](temp)
                
                # Apply logic inference layer.
                output: Tensor =        self._logic_[group](temp)
                
            # If residual is specified...
            if self._residual_ and self._input_dimensions_[group] > 0:
                
                # Concatenate the input with the output.
                output: Tensor =        cat(tensors = [inputs[group], output], dim = -1)
                
            # Append output to list.
            outputs.append(output)
            
        # Return final output list.
        return outputs
        
    def make_list(self,
        x:      list,
        n:      int,
        dtype:  type
    ) -> list[any]:
        """# Make List of N Elements.
        
        Ensure that `x` is either a list of `n` elements or single element of type `dtype`.

        ## Args:
            * x     (list | any):   Element or list.
            * n     (int):          Desired length of list.
            * dtype (type):         Expected type of list elements.

        ## Returns:
            * list[any]:    List of length `n` and type `dtype`.
        """
        # Assert that data type is not list.
        assert dtype is not list,               f"Data type should not be list."
        
        # If `x` is a single element of type `dtype`, create an `n` length list of it.
        if isinstance(x, dtype): x = [x,] * n
        
        # Assert that list is desired length.
        assert len(x) == n,                     f"Parameters should be {dtype} or list of {n} elements."
        
        # For each element in list...
        for e, element in enumerate(x):
            
            # Assert that it is of proper type.
            assert isinstance(element, dtype),  f"Elements expected to be {dtype}, but x[{e}] is {type(element)}"
            
        # Return list.
        return x