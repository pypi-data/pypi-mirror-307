from filelock import FileLock
from tlc.core.url import Scheme as Scheme, Url as Url
from typing import Generator

def tlc_object_lock(url: Url) -> Generator[FileLock | None, None, None]:
    """A context manager for locking a tlc object.

    Currently locking is only implemented for FILE objects.
    """
