import os
import sys

# NOTE: the modules from "ONEAIOPS_LIB_PATH" will be used
# if the module will not be found among installed packages
# We are relying on the order of module search path
# https://docs.python.org/3/tutorial/modules.html#the-module-search-path
sys.path.insert(
    0,
    os.environ.get("ONEAIOPS_LIB_PATH", "/usr/share/one/python/dist-packages"),
)


from .config import SessionConfig
from .core import One, TimeIndex
from .session import Session

__all__ = (
    # sub-packages
    "core",
    # Class
    "Session",
    "SessionConfig",
    "One",
    "TimeIndex",
)
