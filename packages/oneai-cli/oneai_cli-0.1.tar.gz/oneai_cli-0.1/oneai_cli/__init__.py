__version__ = "v0.0.1"

import logging
import logging.config
from importlib.resources import files

from rich.console import Console

log = logging.getLogger("pyoneai-ops.cli")
console = Console()
