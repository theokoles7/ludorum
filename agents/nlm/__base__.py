"""# ludorum.agents.nlm.NeuralLogicMachine

Implementation of Neural Logic Machine as presented in the 2019 paper by Honghua Dong et. al.

## References:
Paper:  https://arxiv.org/pdf/1904.11694.pdf
Source: https://github.com/google/neural-logic-machines
"""

from logging            import Logger

from torch              import cat, Tensor
from torch.nn           import Module, ModuleList

from agents.nlm.layers  import LogicLayer
from utilities.logger   import get_child

class NeuralLogicMachine(Module):
    """# Neural Logic Machine

    Neural Logic Machine (NLM) is a neural-symbolic architecture for both inductive learning and 
    logic reasoning. NLMs use tensors to represent logic predicates. This is done by grounding the 
    predicate as True or False over a fixed set of objects. Based on the tensor representation, 
    rules are implemented as neural operators that can be applied over the premise tensors and 
    generate conclusion tensors.

    ## References:
    * Paper:  https://arxiv.org/pdf/1904.11694.pdf
    * Source: https://github.com/google/neural-logic-machines
    """
    
    def __init__(self,
        depth:              int,
        breadth:            int,
        input_dimensions:   tuple[int],
        output_dimensions:  tuple[int],
        hidden_dimension:   int,
        exclude_self:       bool =              True,
        residual:           bool =              False,
        io_residual:        bool =              False,
        recursion:          bool =              False,
        connections:        list[list[bool]] =  None
    ):
        """# Initialize Neural Logic Machine.

        ## Args:
            * depth             (int):                  The number of logic layers.
            * breadth           (int):                  The breadth of each logic layer.
            * input_dimensions  (tuple[int]):           Input dimensions for each layer.
            * output_dimensions (tuple[int]):           Output dimensions for each layer.
            * hidden_dimension  (int):                  Hidden dimension of the logic model.
            * exclude_self      (bool):                 Exclude multiple occurrences of the same 
                                                        variable.
            * residual          (bool):                 Use residual connections.
            * io_residual       (bool):                 Use input/output-only residual connections.
            * recursion         (bool):                 Enable recursion for weight sharing.
            * connections       (list of list[bool]):   Connections between layers.
        """
        # Initialize module.
        super(NeuralLogicMachine, self).__init__()
        
        # Define attributes.
        self._depth_:               int =               depth
        self._breadth_:             int =               breadth
        self._residual_:            bool =              residual
        self._io_residual_:         bool =              io_residual
        self._recursion_:           bool =              recursion
        self._connections_:         list[list[bool]] =  connections
        
        # Assert that exactly one type of recursion is being requested.
        assert self._residual_ ^ self._io_residual_,    f"Only one type of residual connection type allowed."
        
        # Initialize module list.
        self._layers_:              ModuleList =        ModuleList()
        
        # Start with the input input dimension of the first layer.
        current_dimensions:         list[int] =         input_dimensions
        
        # Calculate total dimensions needed for IO residual option.
        total_output_dimension:     list[int] =         [0 for _ in range(self._breadth_ + 1)]
        
        # For each layer prescribed by depth...
        for layer in range(depth):
            
            # If IO residual option indicated, and not on first layer...
            if layer > 0 and self._io_residual_:
                
                # Update current dimensions.
                current_dimensions: list[int] =         [x + y for x, y in zip(current_dimensions, input_dimensions)]
            
            # Create a logic layer for this depth.
            layer:                  LogicLayer =        LogicLayer(
                                                            breadth =           breadth,
                                                            input_dimensions =  current_dimensions,
                                                            output_dimensions = output_dimensions,
                                                            hidden_dimension =  hidden_dimension,
                                                            exclude_self =      exclude_self,
                                                            residual =          residual
                                                        )
            
            # Update current dimensions to the output of the layer.
            current_dimensions:     Tensor =            layer._output_dimensions_
            
            # Apply masking to dimension.
            current_dimensions:     Tensor =            self._mask_(
                                                            dimensions =        current_dimensions,
                                                            index =             layer,
                                                            masked_value =      0
                                                        )
            
            # Append to layers list.
            self._layers_.append(layer)
            
        # Set output dimensions for IO residual or set to last layer's output dimensions by default.
        self._output_dimensions_:   list[int] =         total_output_dimension if io_residual else current_dimensions
        
    def _mask_(self,
        dimensions:     list[int],
        index:          int,
        masked_value:   int
    ) -> list[int]:
        """# Mask Entries.
        
        Mask out specific entries in a layer's output based on the specified connection mask.

        ## Args:
            * dimensions    (list[int]):    The dimensions of the current layer.
            * index         (int):          Index of the layer.
            * masked_value  (int):          Value to replace masked entries.

        ## Returns:
            * list[int]:    Modified dimensions list with masked entries.
        """
        # If connections have been defined...
        if self._connections_ is not None:
            
            # Assert that index is valid for connections.
            assert index < len(self._connections_), f"Index {index} invalid for list of length {len(self._connections_)}"
            
            # Reference mask for the layer's connection.
            mask:   list[bool] =    self._connections_[index]
            
            # If the mask is defined...
            if mask is not None:
                
                # Assert compatible dimensions.
                assert len(mask) == len(dimensions),    f"Length of mask ({len(mask)} incompatible with dimensions length {len(dimensions)})"
                
                # Apply mask.
                dimensions: list[int] = [x if y else masked_value for x, y in zip(dimensions, mask)]
                
        # Return dimensions.
        return dimensions
    
    def forward(self,
        inputs: list[Tensor],
        depth:  int =           None
    ) -> list[Tensor]:
        """# Forward Pass.
        
        Forward pass through Neural Logic Machine.

        ## Args:
            * inputs    (list[Tensor]):     List of input tensors.
            * depth     (int, optional):    Depth of layers to use for inference. Defaults to None.

        ## Returns:
            * list[Tensor]: Final output after logical inference.
        """
        # Initialize outputs for each group.
        outputs:    list[Tensor] =      [None for _ in range(self._breadth_ + 1)]
        
        # Initialize copy of input tensors.
        temp:       list[Tensor] =      inputs
        
        # If no specific depth is provided, use default.
        if depth is None:           depth:  int =   self._depth_
        
        # If recursion not requested, ensure depth does not exceed the machine depth.
        if not self._recursion_:    depth:  int =   min(depth, self._depth_)
        
        # Define helper merge function.
        def merge(
            x:  Tensor | None,
            y:  Tensor | None
        ) -> Tensor:
            """# Merge Tensors.

            ## Args:
                * x (Tensor | None):    Tensor input 1.
                * y (Tensor | None):    Tensor input 2.

            ## Returns:
                * Tensor:   Merged tensors.
            """
            # If x is not provided, return y.
            if x is None:   return y
            
            # If y is not provided, return x.
            if y is None:   return x
            
            # Otherwise, return concatenated tensors.
            return cat(tensors = [x, y], dim = -1)
        
        # Initialize last layer for recursion.
        last_layer: LogicLayer | None = None
        
        # For each depth level...
        for level in range(depth):
            
            # If using IO residual and not on first level...
            if level > 0 and self._io_residual_:
                
                # Merge pairs of input tensors.
                for i, input in enumerate(inputs): temp[i] = merge(temp[i], input)
                
            # If recursion is enabled...
            if self._recursion_ and level >= 3:
                
                # Assert that residual is not also being used.
                assert not self._residual_, "Recursion not permitted while also using residual"
                
                # Alternate between layers for weight sharing.
                last_layer, layer =     last_layer, self._layers_[level]
                
            # Otherwise, last layer is current layer.
            else: last_layer =          self._layers_[level]
            
            # Forward pass inputs through current layer.
            temp:   list[Tensor] =      last_layer(temp)
            
            # Apply mask to outputs.
            temp:   list[Tensor] =      self._mask_(
                                            dimensions = temp,
                                            index = level,
                                            masked_value = None
                                        )
            
            # If IO residual...
            if self._io_residual_:
                
                # Merge outputs.
                for o, output in enumerate(temp): outputs[o] = merge(outputs[o], output)
                
        # If no IO residual, just use the final output as the result.
        if not self._io_residual_: outputs = temp
        
        # Return outputs.
        return outputs