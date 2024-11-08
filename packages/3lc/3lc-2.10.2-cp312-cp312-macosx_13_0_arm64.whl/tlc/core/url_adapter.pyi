import abc
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from concurrent.futures import Future
from datetime import datetime
from enum import Enum
from tlc.core.tlc_core_threadpool import submit_future as submit_future
from tlc.core.url import Scheme as Scheme, Url as Url
from typing import Any, Iterator

logger: Incomplete

class IfExistsOption(str, Enum):
    '''An Enum indicating what to do if content already exists at the target URL

    ```python
    from tlc.core.url_adapter import IfExistsOption, UrlAdapter
    from tlc.core.url import Url

    url = Url("s3://my-bucket/my-file.txt")
    adapter = UrlAdapter.get_adapter(url)
    adapter.write_string_content_to_url(url, "Hello World!", IfExistsOption.OVERWRITE)
    ```
    '''
    OVERWRITE = 'overwrite'
    RENAME = 'rename'
    RAISE = 'raise'
    REUSE = 'reuse'

class UrlAdapterDirEntry(metaclass=abc.ABCMeta):
    """The base class for all directory entries."""
    @property
    @abc.abstractmethod
    def name(self) -> str:
        """The entry's base filename"""
    @property
    @abc.abstractmethod
    def path(self) -> str:
        """The entry's full path name"""
    @abstractmethod
    def is_dir(self) -> bool:
        """Return True if this entry is a directory"""
    @abstractmethod
    def is_file(self) -> bool:
        """Return True if this entry is a file"""
    @abstractmethod
    def mtime(self) -> Any:
        """Return the modification time object for this entry

        The mtime object is not specified to be of any particular type, but must be comparable to other mtime objects of
        the same type

        May raise exceptions when accessing the resources
        """
    @abstractmethod
    def mtime_datetime(self) -> datetime:
        """Return the modification time for this entry as a datetime object"""

class UrlAdapter(ABC, metaclass=abc.ABCMeta):
    """The base class for all URL adapters"""
    def __init__(self) -> None: ...
    @abstractmethod
    def schemes(self) -> list[Scheme]:
        """Get URL schemes"""
    @abstractmethod
    def read_string_content_from_url(self, url: Url) -> str:
        """Read content from URL synchronously, dispatch"""
    @abstractmethod
    def read_string_content_from_url_async(self, url: Url) -> Future:
        """Read content from URL asynchronously"""
    @abstractmethod
    def read_binary_content_from_url(self, url: Url) -> bytes:
        """Read binary content from URL synchronously, dispatch"""
    @abstractmethod
    def read_binary_content_from_url_async(self, url: Url) -> Future:
        """Read binary content from URL asynchronously"""
    def write_string_content_to_url(self, url: Url, content: str, options: IfExistsOption = ...) -> Url:
        """Write content to URL synchronously"""
    @abstractmethod
    def write_string_content_to_url_async(self, url: Url, content: str, options: IfExistsOption = ...) -> Future:
        """Write content to URL asynchronously"""
    def write_binary_content_to_url(self, url: Url, content: bytes, options: IfExistsOption = ...) -> Url:
        """Write binary content to URL synchronously

        Handles write options and dispatches to `_write_binary_content_to_url`"""
    @abstractmethod
    def write_binary_content_to_url_async(self, url: Url, content: bytes, options: IfExistsOption = ...) -> Future:
        """Write binary content to URL asynchronously"""
    def copy_url(self, source: Url, destination: Url, options: IfExistsOption = ...) -> Url:
        """Copy URL synchronously"""
    @abstractmethod
    def copy_url_async(self, source: Url, destination: Url, options: IfExistsOption = ...) -> Future:
        """Copy URL asynchronously"""
    @abstractmethod
    def delete_url(self, url: Url) -> None:
        """Delete URL synchronously"""
    @abstractmethod
    def delete_url_async(self, url: Url) -> Future:
        """Delete URL asynchronously"""
    @abstractmethod
    def make_dirs(self, url: Url, exist_ok: bool = False) -> None:
        """Create a leaf directory and all intermediate ones synchronously

        For flat file hierarchies, this may be a no-op, see `is_file_hierarchy_flat`."""
    @abstractmethod
    def make_dirs_async(self, url: Url, exist_ok: bool = False) -> Future:
        """Create a leaf directory and all intermediate ones asynchronously

        For flat file hierarchies, this may be a no-op, see `is_file_hierarchy_flat`."""
    @abstractmethod
    def get_file_size(self, url: Url) -> int:
        """Get the size of the file at the given URL synchronously"""
    @abstractmethod
    def get_file_size_async(self, url: Url) -> Future:
        """Get the size of the file at the given URL asynchronously"""
    @abstractmethod
    def list_dir(self, url: Url) -> Iterator[UrlAdapterDirEntry]:
        """List the entries belonging to the directory at the given URL synchronously"""
    @abstractmethod
    def list_dir_async(self, url: Url) -> Future:
        """List the entries belonging to the directory at the given URL asynchronously"""
    @abstractmethod
    def exists(self, url: Url) -> bool:
        """Return True if the given URL refers to an existing path synchronously"""
    @abstractmethod
    def exists_async(self, url: Url) -> Future:
        """Return True if the given URL refers to an existing path asynchronously"""
    @abstractmethod
    def is_dir(self, url: Url) -> bool:
        """Return True if the given URL refers to a directory synchronously"""
    @abstractmethod
    def is_dir_async(self, url: Url) -> Future:
        """Return True if the given URL refers to a directory asynchronously"""
    @abstractmethod
    def is_writable(self, url: Url) -> bool:
        """Return True if the given URL is writable"""
    @abstractmethod
    def is_writable_async(self, url: Url) -> Future:
        """Return True if the given URL is writable asynchronously"""
    def is_file_hierarchy_flat(self) -> bool:
        """Determine if the file hierarchy is flat for this adapter

        Cloud storage normally has a flat hierarchy, meaning that `make_dirs` is a no-op.
        """

class UrlAdapterAsyncFromSync(UrlAdapter, metaclass=abc.ABCMeta):
    """
    A UrlAdapter where the Async methods are implemented as Futures that call
    the equivalent Sync methods on the thread pool

    Derived classes must implement the Sync methods.
    """
    def __init__(self) -> None: ...
    def read_string_content_from_url_async(self, url: Url) -> Future: ...
    def read_binary_content_from_url_async(self, url: Url) -> Future: ...
    def write_string_content_to_url_async(self, url: Url, content: str, options: IfExistsOption = ...) -> Future: ...
    def write_binary_content_to_url_async(self, url: Url, content: bytes, options: IfExistsOption = ...) -> Future: ...
    def delete_url_async(self, url: Url) -> Future: ...
    def copy_url_async(self, source: Url, destination: Url, options: IfExistsOption = ...) -> Future: ...
    def make_dirs_async(self, url: Url, exist_ok: bool = False) -> Future: ...
    def get_file_size_async(self, url: Url) -> Future: ...
    def list_dir_async(self, url: Url) -> Future: ...
    def exists_async(self, url: Url) -> Future: ...
    def is_dir_async(self, url: Url) -> Future: ...
    def is_writable_async(self, url: Url) -> Future: ...

class UrlAdapterSyncFromAsync(UrlAdapter, metaclass=abc.ABCMeta):
    """
    A UrlAdapter where the Sync methods are implemented by calling the equivalent
    Async methods and then waiting on the Futures returned.

    Derived classes must implement the Async methods.
    """
    def read_string_content_from_url(self, url: Url) -> str: ...
    def read_binary_content_from_url(self, url: Url) -> bytes: ...
    def write_string_content_to_url(self, url: Url, content: str, options: IfExistsOption = ...) -> Url: ...
    def write_binary_content_to_url(self, url: Url, content: bytes, options: IfExistsOption = ...) -> Url: ...
    def delete_url(self, url: Url) -> None: ...
    def make_dirs(self, url: Url, exist_ok: bool = False) -> None: ...
    def get_file_size(self, url: Url) -> int: ...
    def list_dir(self, url: Url) -> Iterator[UrlAdapterDirEntry]: ...
    def exists(self, url: Url) -> bool: ...
