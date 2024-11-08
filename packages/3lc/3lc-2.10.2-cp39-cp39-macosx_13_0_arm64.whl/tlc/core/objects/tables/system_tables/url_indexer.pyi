import threading
from _typeshed import Incomplete
from tlc.core.objects.tables.system_tables.indexing import _BlacklistExceptionHandler, _ScanUrl, _UrlIndex
from tlc.core.objects.tables.system_tables.indexing_worker import _UrlIndexingWorker
from tlc.core.url import Url as Url

logger: Incomplete
MACOS: Incomplete

class _UrlIndexer:
    '''An internal handler for indexing URLs.

    This class manages multiple indexer-workers that (may) perform their work in other threads. The concrete sub-indexer
    for a URL is determined by looking at the URL, options, and the currently registered and active indexers.

    The current strategy for determining the sub-indexer is as follows:
    1. If the URL is marked with the field { "static" : True }, it is indexed by the StaticUrlIndexer class.
    2. If the URL is a filesystem URL it is indexed by the FileSystemObserverUrlIndexer class.
    3. If the URL is not handled by the above indexers, it is indexed by the CrawlUrlIndexer class.

    Parameters
    :param blacklist_config: A list of _BlacklistExceptionHandlers that configures the blacklist for
        handling different errors.
    :param tag: A tag to identify the indexer.


    '''
    def __init__(self, blacklist_config: list[_BlacklistExceptionHandler] | None = None, tag: str = '') -> None: ...
    @property
    def data_event(self) -> threading.Event: ...
    def add_scan_url(self, scan_url: _ScanUrl) -> None:
        """Add a scan URL to the indexer.

        The indexer will determine the best sub-indexer for the given URL and add it to the list of URLs to be
        scanned."""
    @property
    def indexers(self) -> list[_UrlIndexingWorker]: ...
    def remove_scan_url(self, scan_url: _ScanUrl) -> None: ...
    def get_scan_urls(self) -> list[_ScanUrl]: ...
    @staticmethod
    def create_indexer_for(config: list[_ScanUrl], tag: str) -> _UrlIndexer: ...
    def get_index(self) -> dict[Url, _UrlIndex]: ...
    def start(self) -> None: ...
    def stop(self) -> None: ...
    @property
    def is_running(self) -> list[bool]: ...
    def join(self, timeout: float | None = None) -> None:
        """Wait for all (if any) indexer threads to join."""
    def wait_for_complete_reindex(self, timeout: float | None = None) -> bool:
        """Wait for a complete a re-indexing cycle.

        :returns: True if at all the sub-indexers completed the re-indexing cycle within the timeout, False otherwise.
        """
    def touch(self) -> None:
        """Touch the scheduler to signal that external usage is active and the indexer should not go into idle."""
