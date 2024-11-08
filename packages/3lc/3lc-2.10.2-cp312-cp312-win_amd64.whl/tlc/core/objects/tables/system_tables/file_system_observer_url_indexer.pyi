import threading
from _typeshed import Incomplete
from tlc.core.objects.tables.system_tables.indexing import _BlacklistExceptionHandler, _ScanUrl, _UrlIndex
from tlc.core.objects.tables.system_tables.indexing_worker import _UrlIndexingWorker
from tlc.core.tlc_core_threadpool import submit_future as submit_future
from tlc.core.url import Scheme as Scheme, Url as Url
from typing import Iterator
from watchdog.events import FileSystemEvent as FileSystemEvent, FileSystemEventHandler

logger: Incomplete

class _FileEventHandler(FileSystemEventHandler):
    indexer: Incomplete
    base_dir: Incomplete
    def __init__(self, indexer: _FileSystemObserverUrlIndexer, base_dir: Url) -> None: ...
    def on_modified(self, event: FileSystemEvent) -> None: ...
    def on_created(self, event: FileSystemEvent) -> None: ...
    def on_deleted(self, event: FileSystemEvent) -> None: ...
    def process(self, event: FileSystemEvent) -> None: ...

class _FileSystemObserverUrlIndexer(_UrlIndexingWorker):
    """An indexer that watches directories and re-indexes the files whenever they change.

    This indexer is lighter than crawling since no work is performed unless files are changed.
    """
    def __init__(self, data_event: threading.Event, blacklist_config: list[_BlacklistExceptionHandler], tag: str = '', stop_event: threading.Event | None = None) -> None: ...
    def add_scan_url(self, url_config: _ScanUrl) -> None: ...
    def remove_scan_url(self, url_config: _ScanUrl) -> None: ...
    def get_scan_urls(self) -> list[_ScanUrl]: ...
    def handle_scan(self, new_scan: Iterator[_UrlIndex]) -> dict[Url, _UrlIndex] | None:
        """Checks a newly scanned index for changes and returns an optionally updated index"""
    def request_complete_reindex(self) -> None: ...
    def wait_for_complete_reindex(self, timeout: float | None = None) -> bool: ...
    def stop(self) -> None:
        """Method to signal the Indexer to stop its activity."""
    def start(self) -> None:
        """Method to start the Indexer."""
    @property
    def is_running(self) -> bool: ...
    def get_index(self) -> dict[Url, _UrlIndex]: ...
    def set_index(self, new_index: dict[Url, _UrlIndex]) -> None:
        """Set the new index and notify any waiting threads.

        The new data may have removed entries or even be empty.
        """
