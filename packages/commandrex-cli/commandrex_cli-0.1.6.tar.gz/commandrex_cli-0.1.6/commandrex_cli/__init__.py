"""
CommandRex - A natural language interface for terminal commands.
"""

__version__ = "0.1.0"

from .main import main
from .config import Config
from .translator import CommandTranslator
from .executor import CommandExecutor
from .ui import CommandRexUI

__all__ = [
    "main",
    "Config",
    "CommandTranslator",
    "CommandExecutor",
    "CommandRexUI",
]