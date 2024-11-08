from _typeshed import Incomplete
from abc import ABC
from enum import Enum, IntEnum
from io import BufferedReader, TextIOWrapper
from pathlib import Path
from typing import Any, Generator, Literal

logger: Incomplete
Options: Incomplete

class AliasPrecedence(IntEnum):
    """An enumeration of the precedence levels for URL aliases.

    AliasPrecedence is used to determine the precedence of URL aliases when multiple aliases are registered (with
    different precedence). The algorithm considers aliases in ascending order, with lower value aliases taking
    precedence over higher precedence aliases. The precedence matching algorithm simply picks the first eligible alias
    and discards any other aliases with the same token.
    """
    PRIMARY = 1
    SECONDARY = 2

class UrlAliasRegistry(ABC):
    '''Maintains a list of currently registered UrlAliases.

    This registry allows for the management of URL aliases, which are shorthand tokens that map to full URL paths.
    By using this registry, applications can more easily handle URLs by converting long, cumbersome paths into
    shorter, manageable tokens. The class provides methods for registering, un-registering, applying, and expanding
    aliases.

    :Example:

    ```python
    # Create a registry instance
    registry = UrlAliasRegistry.instance()

    # Register aliases
    registry.register_url_alias("<HOME>", "http://www.example.com/home")
    registry.register_url_alias("<PROFILE>", "http://www.example.com/profile")

    # Apply aliases to a URL string
    aliased_str = registry.apply_aliases("http://www.example.com/home/page")
    # aliased_str will be "<HOME>/page"

    # Expand aliases in a URL string
    original_str = registry.expand_aliases("<HOME>/page")
    # original_str will be "http://www.example.com/home/page"
    ```

    '''
    url_alias_registry_instance: UrlAliasRegistry | None
    def __init__(self) -> None:
        """Initialize a new UrlAliasRegistry instance.

        Initializes the internal structures for maintaining URL aliases.
        """
    def __iter__(self) -> Generator[tuple[str, str, AliasPrecedence], Any, Any]:
        """Iterate over all registered aliases.

        :returns: A generator that yields tuples of the form (token, path).
        """
    def __contains__(self, token: str) -> bool:
        """Check if a token is registered.

        :param token: The token to check. Required to be an exact match including start and end markers.
        :returns: `True` if the token is registered, otherwise `False`.
        """
    def __getitem__(self, token: str) -> tuple[str, AliasPrecedence]:
        """Get the path and level of an alias.

        :param token: The token to get.
        :returns: A tuple containing the path and level of the alias.
        :raises KeyError: If the alias is not registered.
        """
    def __len__(self) -> int:
        """Get the number of registered aliases."""
    @staticmethod
    def normalize_path(input: str) -> str:
        """Normalize a path string so that it conforms to the registry standard.

        :param input: The string to normalize.
        :returns: The normalized string.
        """
    def str_has_alias(self, input: str) -> bool:
        """Whether this string is considered to contain an alias"""
    def register_url_alias(self, token: str, path: str, force: bool = False, precedence: AliasPrecedence = ...) -> None:
        """Register and validates an alias for a URL.

        :param token: The token of the alias.
        :param path: The path that the alias refers to
        :param force: If True, force the registration of the alias even if it is already registered.
        :raises ValueError: If the token or path is invalid or if the alias already exists and would be modified.
        """
    def unregister_url_alias(self, token: str, precedence: AliasPrecedence = ...) -> str:
        """Unregister an alias.

        :param token: The token of the alias.
        :returns: The path that the alias referred to.
        :raises KeyError: If the alias is not registered.
        """
    def apply_aliases(self, input: str) -> str:
        """Apply registered URL aliases to a string. C:/Tmp/my_data => <TMP_PATH>/my_data

        Replaces strings that contain a possible token with the corresponding alias token path.
        A string can only contain a single alias token and aliases may not be nested.
        If multiple tokens are found, the token that corresponds to the longest path will be used.

        :param input: The string to modify.
        :returns: The modified string with aliases applied.
        """
    def expand_aliases(self, input: str, allow_unexpanded: bool = True) -> str:
        """Expand the alias if any in a string by substituting the token with the registered path segment.

        :param input: The string to modify.
        :param allow_unexpanded: If `True`, aliases that cannot be expanded will be left in the string. If `False`, an
                                    exception will be raised if an alias cannot be expanded.
        :returns: The modified string with aliases expanded.
        """
    def get_aliases(self) -> dict[str, str]: ...
    def print_url_aliases(self, line_prefix: str = '') -> None:
        """Print all registered URL aliases.

        Prints each alias and its corresponding path, each prefixed by `line_prefix`.

        :param line_prefix: A string prefix to prepend to each printed line.
        """
    @staticmethod
    def instance() -> UrlAliasRegistry:
        """Get the singleton instance of the UrlAliasRegistry.

        :returns: The singleton instance of the UrlAliasRegistry.
        """

class Scheme(Enum):
    '''An enumeration of URL schemes.

    This enum is used to represent the scheme of a URL. The scheme is the part of the URL before the first colon (:).
    In order to get the string representation of the scheme, use the value property of the enum, e.g.

    ```python
    FILE.value == "file"
    HTTP.value == "http"
    ```
    '''
    FILE = 'file'
    HTTP = 'http'
    HTTPS = 'https'
    S3 = 's3'
    GS = 'gs'
    ABFS = 'abfs'
    API = 'api'
    RELATIVE = 'relative'
    ALIAS = 'alias'

class Url(ABC):
    '''A class which represents a URL.

    A URL in 3LC is a combination of a scheme and a path. Many methods in 3LC accept URLs as arguments and/or return
    URLs. They are also used to refer to [Tables](tlc.core.objects.table.Table) and to cross reference between them. A
    file URL in 3LC will behave identically on both Posix and Windows systems.

    Since a URL in 3LC might contain aliases, and even the scheme might not be determined until aliases are expanded, it
    is important to note which methods and properties will expand.

    The [path](tlc.core.url.Url.path) and [scheme](#tlc.core.url.Url.scheme) properties of the URL will expand aliases

    :Examples:

    *Scheme is determined from the input string*

    ```python
    file_url = Url("/path/to/file")  # Or Url("file:///path/to/file")
    file_url.scheme == Scheme.FILE
    file_url.path == "/path/to/file"
    str(file_url) == "/path/to/file"  # omit file:// scheme

    s3_url = Url("s3://bucket/path/to/object")
    s3_url.scheme == Scheme.S3
    s3_url.path == "bucket/path/to/object"
    str(s3_url) == "s3://bucket/path/to/object"  # include s3:// scheme

    gcs_url = Url("gs://bucket/path/to/object")
    gcs_url.scheme == Scheme.GS
    gcs_url.path == "bucket/path/to/object"
    str(gcs_url) == "gs://bucket/path/to/object"  # include gs:// scheme

    relative_url = Url("path/to/file")
    relative_url.scheme == Scheme.RELATIVE
    relative_url.path == "path/to/file"
    str(relative_url) == "path/to/file"  # omit relative:// scheme

    # *Aliases are expanded when the URL is used*
    # Assume <SAMPLE_DATA> is **not** registered
    alias_url = Url("<SAMPLE_DATA>/data.csv")
    alias_url.scheme == Scheme.ALIAS
    alias_url.path == "<SAMPLE_DATA>/data.csv"
    str(alias_url) == "<SAMPLE_DATA>/data.csv"

    # Set the alias
    UrlAliasRegistry.instance().register_url_alias(token="<SAMPLE_DATA>", path="/path/to/data")
    # It will now be expanded when using path and scheme properties
    alias_url.scheme == Scheme.FILE
    alias_url.path == "/path/to/data/data.csv"
    str(alias_url) == "<SAMPLE_DATA>/data.csv"

    # Set an alternative alias
    UrlAliasRegistry.instance().unregister_url_alias(token="<SAMPLE_DATA>")
    UrlAliasRegistry.instance().register_url_alias(token="<SAMPLE_DATA>", path="/alternate/path/to/data")
    alias_url.scheme == Scheme.FILE
    alias_url.path == "/alternate/path/to/data/data.csv"

    UrlAliasRegistry.instance().unregister_url_alias(token="<SAMPLE_DATA>")
    ```

    :Terminology:

    - A _normalized_ URL has a scheme, uses single-forward slashes as path separator, and does not end-with a slash.
    - An _expanded_ URL has aliases expanded, and is normalized.
    - An _absolute_ URL is a expanded which means that it can be used as a stable persisted reference.
       - Relative URLs are converted to absolute URLs based on an "owner" URL, or, if applicable, the current working
         directory of the process
    - Relative and Api URLs will have "relative://" or "api://" as their scheme but these schemes will be omitted
      from the stringified representation.

    :Caveats:
    - The URL does not make any network calls or access to the file system. It therefore cannot resolve symlinks, and
      use of these is discouraged in combination with 3LC.
    - There are a few exotic Windows paths that are not supported:
      - The use of a Windows-drive letter without a slash, e.g. `C:foo/bar`, is not supported. Use `C:/foo/bar` instead.

    :param value: The URL as a string, Path, or Url object. When this argument is passed as a string, it will be
                  normalized and the scheme is deduced from the string contents.
    :param scheme: The scheme of the URL, if known.
    :param normalized_path: The normalized path of the URL, if known. If both scheme and normalized_path are passed,
                            they will be used directly without any normalization or parsing. It is the responsibility of
                            the caller to ensure that the scheme and normalized_path are valid.
    :raises ValueError: If the URL is specified with both value and scheme/path.
    '''
    def __init__(self, value: str | Path | Url | None = None, scheme: Scheme | None = None, normalized_path: str | None = None) -> None: ...
    @property
    def scheme(self) -> Scheme:
        """Return the scheme of the expanded URL.

        Calling this method will expand aliases in the URL. If the alias cannot be expanded, it will return
        [Scheme.ALIAS](#tlc.core.url.Scheme.ALIAS).

        To access the scheme of the URL without expanding aliases, use the `_scheme` member
        variable.

        :returns: The scheme of the URL.
        :raises ValueError: If the url scheme cannot be determined.
        """
    @property
    def path(self) -> str:
        '''Return the path of the expanded URL.

        Calling this method will expand aliases in the URL.

        This will return the path without a scheme, so e.g. an S3 URL will return the path without the protocol.

        ```python
        Url("s3://bucket/table.json").path == "/bucket/table.json"
        Url("relative://foo/bar").path == "foo/bar"
        ```

        '''
    @staticmethod
    def absolute_from_relative(url: Url, owner: Url | str | None = None) -> Url:
        """Convert a relative URL to an absolute URL, given an owner URL.

        :param url: The relative URL to convert.
        :param owner: The owner URL, if necessary for conversion.
        """
    @staticmethod
    def relative_from(url: Url, owner: Url | None) -> Url:
        '''Transform a URL into relative form taking a given owner URL into account.

        Create an URL relative to the given owner URL that is equivalent to the absolute URL. The owner URL can be a
        parent directory of the absolute URL, but it may also be a directory or file that shares part of the absolute
        URL\'s path. If the absolute URL and owner URL are not compatible, the function will raise a ValueError

        If the transformation is not possible, for example if the URL and the owner have different schemes, the function
        will return the original URL.

        :Example:

        ```python
        # Owner URL is a directory
        absolute_url = "s3://bucket/path/to/file.ext"
        owner_url = "s3://bucket/path"
        relative_url = Url.relative_from_absolute(absolute_url, owner_url)
        str(relative_url) == "to/file.ext"

        # Owner URL is a file
        absolute_url = "s3://bucket/path/to/file2.ext"
        owner_url = "s3://bucket/path/to/file1.ext"
        relative_url = Url.relative_from_absolute(absolute_url, owner_url)
        assert str(relative_url) == "../file2.ext"
        ```

        :raises ValueError: If the absolute URL and owner URL are not compatible
        '''
    def expand_aliases(self, allow_unexpanded: bool = True) -> Url:
        """Expand aliases in the URL.

        :param allow_unexpanded: If `True`, aliases that cannot be expanded will be left in the URL. If `False`, an
                                    exception will be raised if an alias cannot be expanded.
        :returns: The scheme and path of the URL with aliases expanded.
        """
    def apply_aliases(self) -> Url:
        """Apply all registered aliases to this URL.

        :returns: The URL with aliases applied.
        """
    def is_absolute(self) -> bool:
        """Check if the normalized, unexpanded URL is absolute.

        {bdg-info}`Notice that this method does not expand aliases.`

        :returns: True if the URL is absolute, False otherwise.
        """
    def to_relative(self, owner: Url | str | None = None) -> Url:
        """Relativize a URL, including applying aliases.

        :param owner: The owner URL, if necessary for conversion.
        :returns: A relative URL if possible, otherwise the original URL.
        :raises NotImplementedError: If the conversion is not supported.
        """
    def to_relative_with_max_depth(self, owner: Url, max_depth: int) -> Url:
        """Relativize the given URL with respect to the given owner URL, up to a maximum depth.

        If `url` does not have a common prefix with `owner` up to `max_depth`, `url` is returned with only aliases.

        :param url: The URL to relativize.
        :param owner: The URL to relativize with respect to.
        :param max_depth: The maximum depth to relativize up to.
        :return: The relativized URL.
        """
    def to_absolute(self, owner: Url | str | None = None) -> Url:
        """Convert a relative URL to an absolute URL.

        :param owner: The owner URL, if necessary for conversion.
        :returns: An absolute URL.
        :raises NotImplementedError: If the conversion is not supported.
        """
    def escape(self) -> str:
        """Double-escape the URL string to handle paths in service endpoints.

        Some services require double-escaping to process URLs correctly due to internal un-escaping passes.

        :returns: A double-escaped URL string.
        """
    def replace(self, old: str, new: str) -> Url:
        """Replace occurrences of a substring in the URL with a new substring.

        The intended use case for this method is to e.g., replace a file extension in a URL.

        This methods textually replaces occurrences of the old substring with the new substring in the path of the URL.
        Notice that the replacement will happen on the normalized path, which is not necessarily identical to the path
        passed to the Url constructor when it was first created.

        Changing the scheme of the URL is not supported, however it is possible to replace an alias.
        If the alias contains the scheme (e.g. url.scheme == ALIAS) the scheme can be changed.

        Notice that this method does not expand aliases.

        :param old: The substring to be replaced.
        :param new: The new substring to replace the old substring.
        :returns: A new URL with the specified substring replaced.
        """
    def join(self, other: Url) -> Url:
        """Join two URLs.

        The other URL needs to be a relative URL

        :param other: The URL to join with the current URL. Required to be relative.
        :returns: A new URL, which is the result of joining the current and other URLs.
        :raises ValueError: If the other URL is not relative.
        """
    def create_unique(self, require_writable: bool = False) -> Url:
        """Create a unique and possibly writable version of the Url.

        This method will create a unique URL by appending a unique identifier to the URL, if necessary. If the resulting
        URL is not writable, it will try to create a fallback URL in the PROJECT_ROOT_URL location.

        The fallback mechanism is currently implemented for:
            - Table-URLs in the form of <project>/datasets/<dataset>/tables/<table>

        :returns: A unique Url (which is writable if so requested)
        """
    def create_sibling(self, name: str) -> Url:
        '''Create a new Url next to the current Url.

        :Example:
        ```
        Url("C:/path/to/file.json").create_sibling("umap.json") == Url("C:/path/to/umap.json")
        Url("C:/path/to/dir").create_sibling("other") == Url("C:/path/to/other")
        ```

        :param name: The name of the new Url.
        :returns: A new Url next to the current Url.
        '''
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> int: ...
    def __truediv__(self, other: str | Url) -> Url:
        """Join two URLs using the division operator.

        :param other: The URL to join with the current URL.
        :returns: A new URL, which is the result of joining the current and other URLs.
        """
    def __bool__(self) -> bool: ...
    def to_str(self) -> str:
        """Convert the URL to a normalized string.

        This returns the normalized, un-expanded URL as a string.

        :returns: The URL as a string.
        """
    @staticmethod
    def get_path_type(path: str) -> str:
        """Determine if a path, without scheme, is a Windows or Posix path."""
    @staticmethod
    def normalize_chars(url: str) -> str:
        """Normalize characters in a URL.

        :param url: The URL to normalize.
        :return: The normalized URL.
        """
    @staticmethod
    def get_normalized(value: str) -> tuple[Scheme, str]:
        """Get the normalized value of the string representation of a URL."""
    @staticmethod
    def split_url(value: str) -> tuple[str, str]:
        """Split a URL into a scheme and a path.

        Unlike urlparse, this function does not require a scheme to be present in the URL.
        It will also not parse the drive letter (e.g. C:/) in a Windows URL as part of the URL.
        """
    @staticmethod
    def join_url(scheme: Scheme | None, path: str) -> str:
        """Join a scheme and a path into a URL.

        :param scheme: The scheme.
        :param path: The path.
        :return: The URL with scheme applied
        """
    @staticmethod
    def get_scheme(value: str) -> Scheme:
        """Get the scheme of the string representation of a URL.

        :parm value: The URL as a string.
        :raises ValueError: If the URL scheme is not supported.
        :returns: The scheme of the URL.
        """
    def __fspath__(self) -> str:
        """Get the file system path representation of the URL.

        :raises TypeError: If the URL cannot be used as a file path.
        """
    def open(self, mode: str) -> BufferedReader | TextIOWrapper:
        """Open the URL as a file.

        :param mode: The file mode to use when opening the URL.
        :returns: A file-like object.
        :raises TypeError: If the URL cannot be opened as a file.
        """
    def __enter__(self) -> BufferedReader | TextIOWrapper:
        """Implement the context manager protocol for the URL.

        :raises TypeError: If the URL cannot be used as a context manager.
        """
    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
        """Exit the context manager, closing the file or stream if necessary."""
    def read(self, mode: str = 'b') -> str | bytes:
        """Read the contents of the URL.

        :param mode: The mode to use when reading
        """
    def write(self, content: str | bytes, mode: str = 'b', if_exists: Literal['overwrite', 'rename', 'raise'] = 'overwrite') -> None:
        '''Write data to a URL.

        :param content: The content to write.
        :param mode: The mode to use when writing.
        :param if_exists: The write options to use when writing, can be "overwrite", "rename", or "raise".
        '''
    def exists(self) -> bool:
        """Check if the URL exists.

        :returns: True if the URL exists, False otherwise.

        :raises Exception: If the URL cannot be accessed.
        """
    def make_parents(self, exist_ok: bool = False) -> None:
        """Make all parent directories of the URL.

        :param exist_ok: If True, do not raise an exception if the directory already exists.
        :raises Exception: If the URL cannot be accessed.
        """
    @property
    def parent(self) -> Url:
        """Get the parent URL of the URL.

        :returns: The parent URL.
        """
    @property
    def name(self) -> str:
        '''Get the name of the URL.

        :Example:
        ```
        Url("C:/folder/file.txt").name == "file.txt"
        Url("C:/folder").name == "folder"
        ```

        :returns: The name of the URL.
        '''
    @property
    def stem(self) -> str:
        '''Get the stem of the URL.

        :Example:
        ```
        Url("example.json").stem == "example"
        ```

        :returns: The stem of the URL.
        '''
    @property
    def extension(self) -> str:
        '''Get the extension of the URL.

        :Example:
        ```
        Url("example.json").extension == ".json"
        ```

        :returns: The extension of the URL.
        '''
    @property
    def parts(self) -> list[str]:
        """Get the parts of the URL.

        :returns: The parts of the URL.
        """
    @staticmethod
    def api_url_for_object(obj: object) -> Url:
        """Get the API URL for an object.

        This is the default URL for an object when a persistent URL is not specified.
        API URLs allow objects to be addressable as long as they are in memory.

        :param object: The object to get the API URL for.
        """
    def delete(self) -> None:
        """Delete the URL.

        :raises Exception: If the URL cannot be deleted.
        """
    @classmethod
    def create_table_url(cls, table_name: str | None = None, dataset_name: str | None = None, project_name: str | None = None, root: str | Url | None = None) -> Url:
        """Create a URL for a Table conforming to the 3LC project folder layout.

        :param table_name: The table name to use. If not provided, the default table name will be used.
        :param dataset_name: The dataset name to use. If not provided, the default dataset name will be used.
        :param project_name: The project name to use. If not provided, the current active project will be used.
        :param root: The root url to use. If not provided, the project root url will be used.

        :returns: A Url for a table with the specified names.
        """
    @classmethod
    def create_run_url(cls, run_name: str | None = None, project_name: str | None = None, root: str | Url | None = None) -> Url:
        """Create a URL for a run conforming to the 3LC project folder layout.

        :param run_name: The name of the run. If not provided, the default run name will be used.
        :param project_name: The name of the project. If not provided, the active project will be used.
        :param root: The root URL of the project. If not provided, the project root URL will be used.

        :returns: A URL for a run with the specified names.
        """
    def to_minimal_dict(self, _: bool = False) -> str:
        """Convert the URL to a minimal, serializable representation.

        :returns: The URL as a str.
        """
    def flush(self) -> None:
        """This method is only implemented to ensure that a Url is not used in the place of a str, pathlib.Path or file
        object in cases where this will cause silent errors. This method only raises a more helpful error message.
        """
    def is_descendant_of(self, other: Url) -> bool:
        """Check if the URL is a descendant of another URL.

        :param other: The URL to check if the current URL is a descendant of.
        :returns: True if the URL is a descendant of the other URL, False otherwise.
        """
    def is_dataset_table_url(self) -> bool:
        """Check if the URL is a standard dataset table URL.

        :returns: True if the URL is a canonical table URL, False otherwise.
        """
    def is_run_url(self) -> bool:
        """Check if the URL is a standard run URL.

        :returns: True if the URL is a canonical run URL, False otherwise.
        """
    def is_metrics_table_url(self) -> bool:
        """Check if the URL is a standard metrics table URL.

        :returns: True if the URL is a canonical metrics table URL, False otherwise.
        """
