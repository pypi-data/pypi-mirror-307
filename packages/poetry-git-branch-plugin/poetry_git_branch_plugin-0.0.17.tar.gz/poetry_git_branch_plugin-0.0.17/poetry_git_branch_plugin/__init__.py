"""poetry-git-branch-plugin package init file."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = "unknown"

__all__ = ["__version__"]
