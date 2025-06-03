"""Render and environment visualization."""

from logging        import Logger

from environments   import *
from utilities      import get_child

def render_environment(
    environment:    str,
    **kwargs
) -> None:
    """# Render Environment.

    ## Args:
        * environment   (str):  Environment being rendered.
    """
    # Initialize logger.
    __logger__: Logger =    get_child("render")
    
    # Match environment being rendered.
    match environment:
        
        # Grid World.
        case "grid-world":  __logger__.info(f"Grid World rendering:\n{GridWorld(**kwargs)}")
        
        # Invliad environment provided.
        case _:             __logger__.error(f"Invalid environment selection: {environment}")