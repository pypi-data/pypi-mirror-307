import abc
import threading
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from tlc.core.object_type_registry import NotRegisteredError as NotRegisteredError
from tlc.core.url import Url as Url
from types import TracebackType
from typing import Any, Callable, Generator, Literal, TypedDict

logger: Incomplete

class _ScanUrl(TypedDict, total=False):
    """A dictionary representing a URL to scan with options."""
    url: Url
    layout: Literal['single_dir', 'project']
    object_type: Literal['table', 'run', 'config']
    interval: float | None
    create_default_dirs: bool | None
    indexer_type: str | None
    static: bool | None

@dataclass
class _UrlIndex:
    """A private class used to store Url index details.

    :param url: The URL of the file.
    :param m_time: The last modified time of the Url, as reported by scan.
    :param is_package: Whether the Url is a package, i.e. a directory containing a 3LC object file.
    :param base_dir: The base directory of the file.
    """
    url: Url
    m_time: datetime | None
    is_package: bool
    base_dir: Url
    def __init__(self, url, m_time, is_package, base_dir) -> None: ...

class _StopScanIteration(Exception):
    """An exception to signal that scanning stopped."""

@dataclass
class _BlacklistEntry:
    """A class for representing Urls that are being held in a blacklist.

    :param url: The URL of the file.
    :param exception: The exception that caused the Url to be blacklisted.
    :param expiry_time: The expiry time of the blacklist entry.
    :param retries: The number of retries currently performed for this Url.
    """
    url: Url
    exception: BaseException
    expiry_time: datetime | None
    retries: int
    def __init__(self, url, exception, expiry_time, retries) -> None: ...

def blacklist_message(url: Url, exception: BaseException, backoff: timedelta | None) -> str: ...
def resolve_message(url: Url, exception: BaseException, force: bool) -> str: ...

@dataclass
class _BlacklistExceptionHandler:
    """
    A class for handling exceptions encountered during handling of URLs.

    This class implements the logic for handling exceptions encountered during indexing of URLs. It includes the
    exception type to handle, the backoff function to compute the next retry time, and the description of the handler.

    :param type[BaseException] exception_type: The type of exception to handle.
    :param Callable[[int], timedelta] | None expiration_func: A function to compute the next expiration based on the
        retry number.
    :param Callable[[Url, BaseException, timedelta | None], str] blacklist_message: A function to generate a message
        when blacklisting a URL.
    :param int blacklist_log_level: The log level at which blacklist messages are logged. Default is logging.WARNING.
    :param Callable[[Url, BaseException,bool], str] resolve_message: A function to generate a message when resolving a
        URL.
    :param int resolve_log_level: The log level at which resolve messages are logged. Default is logging.INFO.
    :param str description: A description of the handler. Default is an empty string.
    """
    exception_type: type[BaseException]
    expiration_func: Callable[[int], timedelta] | None
    blacklist_message: Callable[[Url, BaseException, timedelta | None], str] = ...
    blacklist_log_level: int = ...
    resolve_message: Callable[[Url, BaseException, bool], str] = ...
    resolve_log_level: int = ...
    description: str = ...
    @classmethod
    def from_any(cls, conf: Any) -> _BlacklistExceptionHandler: ...
    def __init__(self, exception_type, expiration_func, blacklist_message=..., blacklist_log_level=..., resolve_message=..., resolve_log_level=..., description=...) -> None: ...

class _NotRegisteredHandler(_BlacklistExceptionHandler):
    """A handler for exceptions generated encountering unregistered types

    Blacklist URLs as normal but only warn once for every unregistered type-name.
    """
    def __init__(self) -> None: ...

class _UrlBlacklist:
    """Manages exceptions encountered during for example URL indexing, with configurable logging and expiry times.

    This class includes capabilities for adding, querying, updating, and resolving URLs in a blacklist. It utilizes a
    list of handler instances to provide distinct handling for various types of exceptions.

    :param config: A list of _BlackListExceptionHandlers that configures the blacklist for handling different errors.
    """
    config: Incomplete
    blacklist: Incomplete
    exempt_exceptions: Incomplete
    def __init__(self, config: list[_BlacklistExceptionHandler], exempt: list[type[BaseException]] = ...) -> None: ...
    def handle_exception(self, url: Url, exception: BaseException) -> bool: ...
    def is_blacklisted(self, url: Url) -> bool: ...
    def resolve(self, url: Url) -> bool:
        """Forcefully resolve the URL in the blacklist.

        This removes the URL from the blacklist if it is present even if the expiry is not yet met.
        :param url: The URL to resolve.
        :return bool: Returns whether the URL was blacklisted.
        """

class _BlacklistVisitor:
    """A context manager for visiting urls in the blacklist

    This manager correctly handles exceptions and updates the blacklist accordingly.
    """
    blacklist: Incomplete
    url: Incomplete
    is_blacklisted: Incomplete
    skip: bool
    def __init__(self, blacklist: _UrlBlacklist, url: Url) -> None: ...
    def __enter__(self) -> _BlacklistVisitor: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, _: TracebackType) -> bool | None: ...

class _ScanIterator(ABC, metaclass=abc.ABCMeta):
    """Abstract base class for iterating over Urls and finding relevant files.

    This class provides an iterator interface for iterating over directories containing 3LC objects. It is intended to
    be used as a base class for classes that implement directory iteration for different storage systems.

    :param scan_urls: The URL of the directory to iterate over.
    :param extensions: A list of file extensions to consider while scanning.
    :param tag: A tag to identify the iterator.
    :param blacklist_config: A list of _BlacklistExceptionHandlers that configures the blacklist for handling different
        errors.
    """
    extensions: Incomplete
    tag: Incomplete
    blacklist: Incomplete
    is_first_scan: bool
    def __init__(self, scan_urls: list[_ScanUrl], extensions: list[str], tag: str, blacklist_config: list[_BlacklistExceptionHandler] | None, stop_event: threading.Event | None = None) -> None: ...
    def __iter__(self) -> Generator[_UrlIndex, None, None]:
        """Support iteration over the object."""
    @abstractmethod
    def scan(self) -> Generator[_UrlIndex, None, None]:
        """Perform a recursive scan and yield all resulting Urls.

        This is the top level entry point for the iterator."""
    def add_scan_url(self, scan_url: _ScanUrl) -> None:
        """Try to add a scan_url to the iterator.

        If that doesn't work, raise a ValueError."""
    def remove_scan_url(self, scan_url: _ScanUrl) -> None:
        """Remove a scan_url from the iterator."""
    @property
    def scan_urls(self) -> list[_ScanUrl]: ...
    @abstractmethod
    def bid(self, scan_url: _ScanUrl) -> int:
        """Return a bid for the URL-config in [0,100] for this iterator instance.

        This is used to determine if this iterator instance can be used to scan a given URL."""

class _CompoundScanIterator(_ScanIterator):
    """An iterator that combines multiple index iterators."""
    iterators: Incomplete
    tag: Incomplete
    def __init__(self, iterators: list[_ScanIterator], tag: str) -> None: ...
    def add_iterator(self, it: _ScanIterator) -> None: ...
    def scan(self) -> Generator[_UrlIndex, None, None]: ...
    def add_scan_url(self, scan_url: _ScanUrl) -> None:
        """Add a scan url to the iterator. Overridden to add to the best iterator.

        Requires iterating over sub-iterators to find the best one.
        """
    def remove_scan_url(self, scan_url: _ScanUrl) -> None:
        """Remove a scan_url from the composite iterator."""
    @property
    def scan_urls(self) -> list[_ScanUrl]: ...
    def bid(self, config: _ScanUrl) -> int: ...

@dataclass
class _UrlContent:
    """Data class to represent the content of a Url along with metadata.

    :param url: The URL
    :param base_dir: The base directory of the Url.
    :param m_time: The last modification time of the Url.
    :param content: The parsed JSON content of the Url.
    """
    url: Url
    base_dir: Url
    m_time: datetime | None
    content: dict[str, Any]
    def __init__(self, url, base_dir, m_time, content) -> None: ...
