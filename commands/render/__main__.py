"""# ludorum.commands.render.main

Render and environment visualization."""

from logging        import Logger

from environments   import *
from utilities      import get_child

def main(
    environment:    str,
    **kwargs
) -> None:
    """# Render Environment.

    ## Args:
        * environment   (str):  Environment being rendered.
    """
    # Initialize logger.
    __logger__: Logger =    get_child("render")
    
    # Define mapping of environments to their class definitions.
    _environments_: dict[str, Environment] =    {
                                                    "grid-world":   GridWorld
                                                }
    
    try:# Render environment.
        __logger__.info(f"Rendering {environment}:\n{_environments_[environment](**kwargs)}")
    
    except Exception as e:  __logger__.critical(f"Unexpected error caught: {e}")