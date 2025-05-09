"""Render and environment visualization."""

from logging        import Logger

from environments   import *
from utilities      import LOGGER

def render_environment(
    environment:    str,
    **kwargs
) -> None:
    """# Render Environment.

    ## Args:
        * environment   (str):  Environment being rendered.
    """
    # Initialize logger.
    __logger__: Logger =    LOGGER.getChild("render")
    
    # Match environment being rendered.
    match environment:
        
        # Grid World.
        case "grid-world":  __logger__.info(f"Grid World rendering:\n{GridWorld(**kwargs)}")
        
        # Invliad environment provided.
        case _:             __logger__.error(f"Invalid environment selection: {environment}")