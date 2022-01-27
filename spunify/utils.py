""" Utility funcitons for the project. """

from itertools import islice
from pathlib import Path
from typing import Iterable


def get_cache_path() -> Path:
    """Returns the path to the cache file."""
    return get_project_root() / ".cache.json"


def get_project_root() -> Path:
    """Returns the project root directory."""
    return Path(__file__).parent.parent


def chunks(iterable: Iterable, size: int = 100) -> Iterable:
    """
    Split an iterable into chunks.

    :param col: The collection to be split.
    :param size: The size of the chunks.
    :yield: A list of chunks.
    """
    it = iter(iterable)
    while chunk := list(islice(it, size)):
        yield list(chunk)
