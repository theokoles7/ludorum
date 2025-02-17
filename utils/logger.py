"""Logging utilities."""

__all__ = ["LOGGER"]

from logging            import getLogger, Formatter, Logger, StreamHandler
from logging.handlers   import RotatingFileHandler
from os                 import makedirs
from os.path            import dirname
from sys                import stdout

from utils.arguments    import ARGS
from utils.timestamp    import TIMESTAMP

# Match command being executed
match ARGS.command:

    # Experiment
    case "run-experiment":  _log_path_: str =   f"{ARGS.logging_path}/experiments/{TIMESTAMP}.log"

    # Game
    case "play-game":       _log_path_: str =   f"{ARGS.logging_path}/games/{ARGS.game}/{ARGS.agent}/{TIMESTAMP}.log"

# Ensure that logging path exists
makedirs(name = dirname(p = _log_path_), exist_ok = True)

# Initialize logger
LOGGER:         Logger =                getLogger("ludorum")

# Set logging level
LOGGER.setLevel(ARGS.logging_level)

# Define console handler
stdout_handler: StreamHandler =         StreamHandler(stream = stdout)
stdout_handler.setFormatter(Formatter("%(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(hdlr = stdout_handler)

# Define file handler
file_handler:   RotatingFileHandler =   RotatingFileHandler(filename = _log_path_, maxBytes = 1048576, backupCount = 3)
file_handler.setFormatter(Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))
LOGGER.addHandler(hdlr = file_handler)