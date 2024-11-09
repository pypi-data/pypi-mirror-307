from collections import namedtuple

from .hy3 import *

__title__ = "hytek"
__author__ = "plun1331"
__license__ = "MIT"
__copyright__ = "Copyright 2024-present plun13331"

version_info = namedtuple("version_info", "major minor micro releaselevel serial")(
    major=0, minor=0, micro=5, releaselevel="alpha", serial=0
)

__version__ = f"{version_info.major}.{version_info.minor}.{version_info.micro}"
