from _typeshed import Incomplete
from datetime import datetime
from fsspec import AbstractFileSystem as AbstractFileSystem
from tlc.core.url import Scheme as Scheme, Url as Url
from tlc.core.url_adapter_registry import UrlAdapterRegistry as UrlAdapterRegistry
from tlc.core.url_adapters.fsspec_url_adapter import FSSpecUrlAdapter as FSSpecUrlAdapter, FSSpecUrlAdapterDirEntry as FSSpecUrlAdapterDirEntry
from typing import Any

logger: Incomplete

class AbfsUrlAdapterDirEntry(FSSpecUrlAdapterDirEntry):
    """A directory entry for an AbfsUrlAdapter"""
    def __init__(self, ls_info: dict[str, Any]) -> None: ...
    @property
    def name(self) -> str: ...
    @property
    def path(self) -> str: ...
    def mtime(self) -> datetime: ...

class AbfsUrlAdapter(FSSpecUrlAdapter):
    """
    An adapter for resolving reads/writes to URLs starting with `abfs://`
    """
    abfs_scheme: Incomplete
    abfs_protocol: Incomplete
    def __init__(self) -> None: ...
    def schemes(self) -> list[Scheme]: ...
    def is_file_hierarchy_flat(self) -> bool: ...
