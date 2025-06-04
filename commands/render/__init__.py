"""# ludorum.commands.render

This package constructs a utility for rendering environment visualizations.
"""

__all__ =   [
                # Argument registration.
                "register_render_parser",
                
                # Main process.
                "main"
            ]

# Argument registration.
from commands.render.__args__   import register_render_parser

# Main process.
from commands.render.__main__   import main