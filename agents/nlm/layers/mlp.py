"""# ludorum.agents.nlm.layers.MLPLayer"""

__all__ = ["MLPLayer"]

from torch                      import Tensor
from torch.nn                   import Linear, Module, Sequential

from agents.nlm.layers.linear   import LinearLayer

class MLPLayer(Module):
    """# MLP Layer
    
    A multi-layer perceptron (MLP) layer with activation for hidden layers.

    Adapted from jatorch.nn.cnn.layers: https://github.com/vacancy/Jacinle/blob/master/jactorch/nn/cnn/layers.py
    """
    
    def __init__(self,
        input_dimension:    int,
        output_dimension:   int,
        hidden_dimensions:  list[int] | int
    ):
        """# Initialize MLP Layer.

        ## Args:
            * input_dimension   (int):              Number of input features.
            * output_dimension  (int):              Number of output features.
            * hidden_dimensions (list[int] | int):  List of hidden layer sizes.
        """
        # Initialize module.
        super(MLPLayer, self).__init__()
        
        # Define dimensions.
        self._input_dimension_:     int =           input_dimension
        self._output_dimension_:    int =           output_dimension
        self._hidden_dimensions_:   list[int] =     hidden_dimensions if isinstance(hidden_dimensions, list) else [hidden_dimensions]
        
        # Define attributes.
        self._flatten_:             bool =          True
        self._last_activation_:     bool =          False
        
        # Define dimensions list.
        dimensions:                 list[int] =     [self._input_dimension_] + self._hidden_dimensions_ + [self._output_dimension_]
        
        # Initialize modules list.
        modules:                    list[Module] =  []
        
        # or each hidden dimension...
        for i in range(len(self._hidden_dimensions_)):
            
            # Create hidden layer.
            modules.append(LinearLayer(
                in_features =   dimensions[i],
                out_features =  dimensions[i + 1]
            ))
            
        # Append final layer.
        modules.append(Linear(
            in_features =   dimensions[-2],
            out_features =  dimensions[-1],
            bias =          True
        ))
        
        # Apply layers sequentially.
        self._mlp_:                 Sequential =    Sequential(*modules)
    
    def reset_parameters(self) -> None:
        """# Reset Parameters.
        
        Reset parameters of linear layer.
        """
        # For each module in layer...
        for module in self.modules():
            
            # If it is a linear layer, reset the parameters.
            if isinstance(module, Linear): module.reset_parameters()

    def forward(self,
        input:  Tensor
    ) -> Tensor:
        """# Forward Pass.
        
        Forward pass through the MLP.

        ## Args:
            * input (Tensor):   The input tensor.

        ## Returns:
            * Tensor:   The output tensor after passing through the MLP layers.
        """
        # Flatten if desired.
        if self._flatten_: input: Tensor = input.view(input.size(0), -1)
        
        # Make forward pass through layer.
        return self._mlp_(input)