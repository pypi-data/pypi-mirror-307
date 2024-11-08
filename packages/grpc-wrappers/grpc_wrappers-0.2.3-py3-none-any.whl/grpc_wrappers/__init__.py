from . import wrappers
from .wrapper import (
    GRPCInvisibleSequenceWrapper,
    GRPCInvisibleWrapper,
    GRPCMessageWrapper,
    GRPCRepeatedMessageWrapper,
)

try:
    from ._version import __version__, __version_tuple__
except ImportError:  # pragma: no cover
    __version__ = version = "unknown"
    __version_tuple__ = version_tuple = ("unknown",)  # type: ignore

__author__ = "Matthew Wardrop"
__author_email__ = "mpwardrop@gmail.com"

__all__ = [
    # "__version__",
    # "__version_tuple__",
    # "__author__",
    # "__author_email__",
    "wrappers",
    "GRPCInvisibleSequenceWrapper",
    "GRPCInvisibleWrapper",
    "GRPCMessageWrapper",
    "GRPCRepeatedMessageWrapper",
]
