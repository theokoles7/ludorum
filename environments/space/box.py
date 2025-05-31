"""# ludorum.environments.space.box"""

__all__ = ["BoxSpace"]

from typing                         import Union

from numpy                          import all, allclose, any, array, asarray, broadcast_to, dtype, float32, isscalar, ndarray
from torch                          import from_numpy, Tensor

from environments.space.__base__    import Space

class BoxSpace(Space):
    """# Box Space.

    Continuous space representing n-dimensional bounded box.
    
    ## Mathematical Definition:
        S = [low, high]ⁿ = {x ∈ ℝⁿ | low ≤ x ≤ high (element-wise)}
        
    ## Shape Specification:
        * Shape = (n₁, n₂, ..., nₖ) defines k-dimensional tensor structure.
        * Total elements = n₁ × n₂ × ... × nₖ
        * Bounds are broadcast to match shape if needed.
        
    ## Tensor Representation:
        Elements are converted to float tensors matching the specified shape, suitable for neural 
        network inputs and continuous control.
        
    ## Attributes:
        * low       (np.ndarray):   Lower bounds (broadcast to shape)
        * high      (np.ndarray):   Upper bounds (broadcast to shape)
        * shape     (TupleType):    Tensor dimensionality structure
        * data_type (np.dtype):     Float dtype for elements
        
    ## Example:
    >>> # 2D position space: [(x, y)] where x,y ∈ [0, 10]
    >>> position_space = Box(low=0.0, high=10.0, shape=(2,))
    >>> 
    >>> # 3×3 image space with pixel values in [0, 1]
    >>> image_space = Box(low=0.0, high=1.0, shape=(3, 3))
    >>> 
    >>> position = position_space.sample()  # Random position
    >>> pos_tensor = position_space.to_tensor(position)  # Float tensor
    """
    
    def __init__(self,
        low:        float | ndarray,
        high:       float | ndarray,
        shape:      tuple =             None,
        data_type:  Union[dtype, str] = float32
    ):
        """# Initialize Box Space.
        
        Initialize continuous box space with bounds and shape.

        ## Args:
            * low       (float | ndarray):              Scalar value or an array matching shape 
                                                        parameter.
            * high      (float | ndarray):              Scalar value or an array matching shape 
                                                        parameter.
            * shape     (tuple, optional):              Tensor shape. Defaults to shape from 
                                                        low/high if None.
            * data_type (Union[dtype, str], optional):  NumPy data type of elements. Defaults to 
                                                        float32.
                                                        
        ## Raises:
            * ValueError:   If bounds are inconsistent or invalid.
        """
        # Convert bounds to arrays.
        if isscalar(low):   self._low_:     ndarray =   array(low,  dtype = data_type)
        if isscalar(high):  self._high_:    ndarray =   array(high, dtype = data_type)
        
        # If a shape was not provided...
        if shape is None:
            
            # And low/high shapes are not the same, then raise an error.
            if low.shape != high.shape: raise ValueError(f"Low and high bounds must have the same shape: {low.shape} != {high.shape}")
            
            # Otherwise, infer space shape from low shape.
            shape:  tuple =     low.shape
            
        # Otherwise...
        else:
            
            # Broadcast bounds to specified shape.
            low:    ndarray =   broadcast_to(low,   shape = shape).astype(data_type)
            high:   ndarray =   broadcast_to(high,  shape = shape).astype(data_type)
        
        # If low values are grater than high values, raise error.
        if any(low >= high): raise ValueError(f"All low bounds must be less than high bounds.")
        
        # Initialize space.
        super(BoxSpace, self).__init__(shape = shape, data_type = dtype(data_type))
        
        # Define attributes.
        self._low_:     ndarray =   low
        self._high_:    ndarray =   high
        
    def __eq__(self,
        other:  any
    ) -> bool:
        """# Evaluate equality with another Box space object.

        ## Args:
            * other (any):  Box space object being compared.

        ## Returns:
            * bool:
                * True:     Box spaces have identical ranges.
                * False:    Box spaces do not have identical ranges, or 'other' is not a 
                            Box space.
        """
        # Return equality evaluation.
        return  (
                    isinstance(other, BoxSpace)         and
                    self._shape_ == other._shape_       and
                    allclose(self._low_,  other._low_)  and
                    allclose(self._high_, other._high_)
                )
        
    def __repr__(self) -> str:
        """# Provide string format of Box space.

        ## Returns:
            * str:  String format of Box space.
        """
        # Return string format.
        return f"BoxSpace(low = {self._low_}, high = {self._high_}, shape = {self._shape_}, dtype = {self._dtype_})"
        
    def contains(self,
        x:  any
    ) -> bool:
        """# Test if x ∈ [low, high]ⁿ (element-wise).

        ## Args:
            * x (any):  Array-like value to test

        ## Returns:
            * bool:
                * True:     x ∈ [low, high]ⁿ
                * False:    x ∉ [low, high]ⁿ
        """
        try:# Convert x to array.
            x:  ndarray =   asarray(x, dtype = self._dtype_)
            
            # Return False if element shape is not consistent with space.
            if x.shape != self._shape_: return False
            
            # Indicate if element components are within space range.
            return all(self._low_ <= x) and all(x <= self._high_)
            
        # Indicate that element is not contained within space or invalid element type was provided.
        except (ValueError, TypeError): return False
        
    def from_tensor(self,
        tensor: Tensor
    ) -> ndarray:
        """# Convert tensor back to numpy array.

        ## Args:
            * tensor    (Tensor):   Float tensor with shape matching space.

        ## Returns:
            * ndarray:  Array representation.
            
        ## Raises:
            * ValueError:   If tensor shape doesn't match or values out of bounds.
        """
        # Raise error if shape is inconsistent with space.
        if tuple(tensor.shape) != self._shape_: raise ValueError(f"Tensor shape {tensor.shape} inconsistent with space {self._shape_}")
        
        # Convert tensor to array.
        x:  ndarray =   tensor.detach().cpu().numpy().astype(self._dtype_)
        
        # Raise error if element is out of space range.
        if not self.contains(x = x):            raise ValueError(f"Tensor values {tensor} out of space bounds [{self._low_}, {self._high_}]")
        
        # Return converted element.
        return x
        
    def sample(self) -> ndarray:
        """# Sample Uniformly from [low, high]ⁿ.

        ## Returns:
            * ndarray:  Random array with shape matching space.
        """
        # Provide sample.
        return  (
                    self._low_ +
                    self._random_state_.uniform(size = self._shape_) *
                    (self._high_ - self._low_)
                )
        
    def to_tensor(self,
        x:  any
    ) -> Tensor:
        """# Convert box element to float tensor.

        ## Args:
            * x (any):  Array-like element (must be within bounds).

        ## Returns:
            * Tensor:   Float tensor with matching shape.
            
        ## Raises:
            * ValueError:   If x not within bounds or wrong shape.
        """
        # Raise error if values do not satisfy space bounds.
        if not self.contains(x): raise ValueError(f"Value {x} violates space bounds [{self._low_}, {self._high_}]")
        
        # Return element as tensor.
        return from_numpy(asarray(x, dtype = self._dtype_).copy())