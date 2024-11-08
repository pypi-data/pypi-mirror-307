from _typeshed import Incomplete
from tlc.core.object import Object as Object
from tlc.core.object_type_registry import ObjectTypeRegistry as ObjectTypeRegistry
from tlc.core.objects.tables.system_tables.indexing import _ScanUrl
from tlc.core.objects.tables.system_tables.indexing_table import IndexingTable as IndexingTable
from tlc.core.schema import DictValue as DictValue, Schema as Schema
from tlc.core.url import AliasPrecedence as AliasPrecedence, Url as Url, UrlAliasRegistry as UrlAliasRegistry
from tlc.core.url_adapters import ApiUrlAdapter as ApiUrlAdapter
from tlcconfig.options import ConfigSource as ConfigSource
from typing import Any

logger: Incomplete

class ConfigIndexingTable(IndexingTable):
    """A specialized indexing table for Config files fetched from URLs.

    This table is designed to manage Config file objects. Each row in this table corresponds to a config file object
    that is fetched from a URL. It extends from the generic `IndexingTable` to provide functionalities specifically
    optimized for handling external config files embedded with data.

    :Example:

    ```python
    table = ConfigIndexingTable.instance()
    table.wait_for_next_index()
    for row in table.table_rows:
        print(row)
    ```

    :Closing Comments:

    - **Singleton Pattern**: This class implements the Singleton pattern.
      Always use `ConfigIndexingTable.instance()` to get the singleton instance.

    """
    config_indexing_table_instance: ConfigIndexingTable | None
    def __init__(self, url: Url | None = None, scan_urls: list[_ScanUrl] | None = None, init_parameters: Any = None) -> None:
        """
        Initialize a ConfigIndexingTable object.

        :param url: The URL from which this table can be read.
        :param scan_urls: A list of URLs to scan for config files.
        :param init_parameters: Any initialization parameters.

        :raises ValueError: If some conditions, such as invalid URLs, are not met.
        """
    def update_config(self) -> None:
        """Update the configuration of the ConfigIndexingTable."""
    def ensure_dependent_properties(self) -> None:
        """Ensure that the dependent properties are updated."""
    @staticmethod
    def instance() -> ConfigIndexingTable:
        """
        Returns the singleton ConfigIndexingTable object
        """
    def should_consider_object(self, obj: Object) -> bool:
        """Only consider Config objects"""
    def start(self) -> None:
        """Start the ConfigIndexingTable and dispatch a config updater thread"""
    def stop(self) -> None:
        """Stop the ConfigIndexingTable and the config updater thread"""
    def wait_for_complete_index(self, timeout: float | None = None) -> bool: ...
