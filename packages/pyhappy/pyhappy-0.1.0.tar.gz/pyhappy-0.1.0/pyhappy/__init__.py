"""
This module initializes the core components of the project, including
the necessary classes and setup required for the application to run smoothly.

Modules and classes provided in this file:

- ConsoleLogger: A class for logging messages to the console, assisting in
  debugging and providing runtime information.
- FixIDEComplain: A class that addresses IDE warnings regarding
  unimplemented code while allowing the code to execute correctly.
- Project setup: Handles the initialization of key components, ensuring
  that they are properly configured and available for use in the application.

This file serves as the entry point for setting up the project's infrastructure,
providing centralized management of logging, initialization, and troubleshooting
through the classes and functions contained within it.
"""

__version__ = "0.1.0"
__author__ = "Alaamer"
__email__ = "alaamerthefirst@gmail"
__url__ = "https://github.com/alaamer12/happy"

from packages.core.pyhappy.collections import *  # noqa
from packages.core.pyhappy.enum_registry import *  # noqa
from packages.core.pyhappy.enums_toolkits import *  # noqa
from packages.core.pyhappy.exceptions import *  # noqa
from packages.core.pyhappy.log import *  # noqa
from packages.core.pyhappy.re import *  # noqa
from packages.core.pyhappy.time import *  # noqa
from packages.core.pyhappy.toolkits import *  # noqa
from packages.core.pyhappy.types import *  # noqa

__all__ = [
    "collections",
    "enum_registry",
    "enums_toolkits",
    "exceptions",
    "log",
    "re",
    "time",
    "toolkits",
    "types",
]
