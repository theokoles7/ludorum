"""# ludorum.environments

This package defines various types of reinforcement learning environments, focusing on games.

Game environments can be categorized into different categories based on their action and state space 
definitions, such as discrete or continuous, as well as how many agents/players the game requires, 
etc. Each category has its own unique features for which testing an agent may be more preferable.
"""

__all__ =   [
                # Environment Loader.
                "load_environment",
    
                # Abstract Environment.
                "Environment",
                
                # Discrete, Single Player.
                "GridWorld"
            ]

from environments.__base__      import Environment

from environments.grid_world    import GridWorld

# Define environment loader function.
def load_environment(
    environment:    str,
    **kwargs
) -> Environment:
    """# Load Environment
    
    Initialize and provide environment based on selection and parameters.

    ## Args:
        * environment   (str):  Environment selection. For a full list of options, refer to 
                                ludorum.environments package or documentation.

    ## Returns:
        * Environment:  Initialized environment, based on selection and keyword arguments.
    """
    from logging            import Logger
    
    from utilities          import LOGGER
    
    # Initialize logger.
    __logger__: Logger =    LOGGER.getChild("environment-loader")
    
    # Log action for debugging.
    __logger__.debug(f"Loading environment: {environment} ({kwargs})")
    
    # Match environment selection.
    match environment:
        
        # Grid World
        case "grid-world":  return GridWorld(**kwargs)
        
        # Invalid environment selection.
        case _:             raise ValueError(f"Invalid environment selected: {environment}")