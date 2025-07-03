"""# ludorum.environments.registry

Dynamic environment registration and loading.
"""

from typing                 import Callable, Dict, Any

from environments.__base__  import Environment

# Initialize registry.
_REGISTRY_: Dict[str, Callable[..., Any]] = {}

# Define environment registration.
def register_environment(
    name:           str,
    constructor:    Callable[..., Any]
) -> None:
    """# Register Environment.

    ## Args:
        * name          (str):                  Unique name of environment.
        * constructor   (Callable[..., Any]):   Environment's constructor.
    """
    _REGISTRY_[name.lower()] = constructor
    
def load_environment(
    name:   str,
    **kwargs
) -> Environment:
    """# Load Environment.

    ## Args:
        * name  (str):  Environment selection.

    ## Returns:
        * Environment:  Instantiated environment.
        
    ## Raises:
        * ValueError:   If environment is not registered.
    """
    # If environment is not registered...
    if name.lower() not in _REGISTRY_:
        
        # Report error.
        raise ValueError(f"Invalid environment selection: {name}")
    
    # Otherwise, load environment.
    return _REGISTRY_[name.lower()](**kwargs)