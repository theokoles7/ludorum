"""Go game implementation."""

__all__ = ["Go"]

from games.__base__ import Environment

class Go(Environment):
    """Go game environment."""

    def __init__(self, **kwargs):
        """# Initialize Go game environment."""

        raise NotImplementedError(f"The Go game environment has not been implemented.")