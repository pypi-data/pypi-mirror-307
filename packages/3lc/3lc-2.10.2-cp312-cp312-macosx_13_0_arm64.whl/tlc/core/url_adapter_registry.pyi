from abc import ABC
from concurrent.futures import Future
from tlc.core.url import Scheme as Scheme, Url as Url
from tlc.core.url_adapter import IfExistsOption as IfExistsOption, UrlAdapter as UrlAdapter, UrlAdapterDirEntry as UrlAdapterDirEntry
from typing import Iterator

class UrlAdapterRegistry(ABC):
    """Maintains a list of currently registered UrlAdapters, and provides
    functionality for de-/serializing objects from Url."""
    @staticmethod
    def register_url_adapter_for_scheme(scheme: Scheme, url_adapter: UrlAdapter) -> None:
        """Register a URL adapter to be used for the given scheme"""
    @staticmethod
    def register_url_adapter(url_adapter: UrlAdapter) -> None:
        """Register a URL adapter"""
    @staticmethod
    def get_url_adapter_for_url(url: Url, default_value: UrlAdapter | None = None) -> UrlAdapter | None:
        """Get the URL adapter for the given URL"""
    @staticmethod
    def get_url_adapter_for_scheme(scheme: Scheme, default_value: UrlAdapter | None = None) -> UrlAdapter | None:
        """Get URL adapter for the given scheme"""
    @staticmethod
    def read_string_content_from_url(url: Url, default_value: str | None = None) -> str:
        """Resolve UrlAdapter and read the string content from the given URL

        If no adapter can be resolved for the given Url return the 'default_value' if given else raise an exception
        """
    @staticmethod
    def write_string_content_to_url(url: Url, content: str, options: IfExistsOption = ...) -> Url:
        """Resolve UrlAdapter and write the string content to the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def read_binary_content_from_url(url: Url, default_value: bytes | None = None) -> bytes:
        """Resolve UrlAdapter and read the binary content from the given URL

        If no adapter can be resolved for the given Url return the 'default_value' if given else raise an exception.
        """
    @staticmethod
    def read_binary_content_from_url_async(url: Url, default_value: bytes | None = None) -> Future:
        """Resolve UrlAdapter and read the binary content from the given URL

        If no adapter can be resolved for the given Url return the 'default_value' if given else raise an exception.
        """
    @staticmethod
    def write_binary_content_to_url(url: Url, content: bytes, options: IfExistsOption = ...) -> Url:
        """Resolve UrlAdapter and write the binary content to the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def write_binary_content_to_url_async(url: Url, content: bytes, options: IfExistsOption = ...) -> Future:
        """Resolve UrlAdapter and write the binary content to the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def copy_url(input: Url, output: Url, options: IfExistsOption = ...) -> Url:
        """Resolve UrlAdapter and copy the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def delete_url(url: Url) -> None:
        """Resolve UrlAdapter and delete the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def is_writable(url: Url) -> bool:
        """Resolve UrlAdapter and check if the given URL is writable

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def make_dirs(url: Url, exist_ok: bool = False) -> None:
        """Resolve UrlAdapter and create a leaf directory and all intermediate ones at the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def is_file_hierarchy_flat(url: Url) -> bool:
        """Resolve UrlAdapter and check if the given URL resides on storage with flat file hierarchy

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def get_file_size(url: Url) -> int:
        """Resolve UrlAdapter and get the size of the file at the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def list_dir(url: Url) -> Iterator[UrlAdapterDirEntry]:
        """Resolve UrlAdapter and list the entries belonging to the directory at the given URL

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def exists(url: Url) -> bool:
        """Resolve UrlAdapter and check if the given URL exists

        If no adapter can be resolved for the given Url an exception is raised
        """
    @staticmethod
    def print_url_adapters(line_prefix: str = '') -> None:
        """
        Print all URL adapters.
        """
    @staticmethod
    def schemes() -> list[str]:
        """Get URL schemes for registered adapters"""
    @staticmethod
    def is_dir(url: Url) -> bool:
        """Resolve UrlAdapter and check if the given URL is a directory

        If no adapter can be resolved for the given Url an exception is raised
        """
