"""quartofetch - manage Quarto paper repositories."""

from importlib.metadata import version, PackageNotFoundError
from .paper_manager import Paper, PaperManager
from .quarto_project import QuartoProject
from .logging_config import setup_logging, stage, substage

try:
    __version__ = version("quartofetch")
except PackageNotFoundError:  # pragma: no cover
    # Package is not installed
    __version__ = "0.0.0"

__all__ = [
    "Paper",
    "PaperManager",
    "QuartoProject",
    "setup_logging",
    "stage",
    "substage",
]
