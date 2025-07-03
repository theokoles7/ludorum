"""# ludorum.agents.registry

Dynamic agent registration and loading.
"""

from typing             import Callable, Dict, Any

from agents.__base__    import Agent

# Initialize registry.
_REGISTRY_: Dict[str, Callable[..., Any]] = {}

# Define agent registration.
def register_agent(
    name:           str,
    constructor:    Callable[..., Any]
) -> None:
    """# Register Agent.

    ## Args:
        * name          (str):                  Unique name of agent.
        * constructor   (Callable[..., Any]):   Agent's constructor.
    """
    _REGISTRY_[name.lower()] = constructor
    
def load_agent(
    name:   str,
    **kwargs
) -> Agent:
    """# Load Agent.

    ## Args:
        * name  (str):  Agent selection.

    ## Returns:
        * Agent:    Instantiated agent.
        
    ## Raises:
        * ValueError:   If agent is not registered.
    """
    # If agent is not registered...
    if name.lower() not in _REGISTRY_:
        
        # Report error.
        raise ValueError(f"Invalid agent selection: {name}")
    
    # Otherwise, load agent.
    return _REGISTRY_[name.lower()](**kwargs)