import logging
from _typeshed import Incomplete
from io import StringIO
from typing import Any

class _TqdmLogFormatter:
    """A custom log formatter for tqdm progress bars.

    This class modifies the formatting of a provided logger within the context of a `with` statement.
    The log formatting is returned to its original state when exiting the `with` context.

    :param logger: The logger to modify.
    """
    def __init__(self, logger: logging.Logger) -> None: ...
    def __enter__(self) -> logging.Logger: ...
    def __exit__(self, exc_type: Any, exc_value: Any, exc_traceback: Any) -> None: ...

class _TqdmLogWriter(StringIO):
    """A writer designed to allow tqdm to write progress bars to logging.

    `TqdmLogWriter` is an extension of `StringIO` that logs messages using a provided logger, while ensuring that tqdm
    progress bars display correctly. The writer also injects an extra 'interactive' attribute into the log record, which
    can be used for filtering

    :param logger: The logger to use for logging messages.
    """
    def __init__(self, logger: logging.Logger) -> None: ...
    def write(self, buffer: str) -> int:
        """Writes the content of the buffer to the logger.

        Modifies the logger formatting for the duration of the logging operation to ensure
        correct display of tqdm progress bars.

        :param buffer: The string to write to the logger.
        """
    def flush(self) -> None: ...

class _InteractiveFilter(logging.Filter):
    '''A filter that prevents records tagged with \'interactive\':True from being logged.

    Example usage:

    ```python
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(\'%(asctime)s - %(name)s - %(levelname)s - %(message)s\')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate = False

    interactive_filter = _InteractiveFilter()
    logger.addFilter(interactive_filter)

    from tqdm import tqdm

    with tqdm(total=100, file=_TqdmLogWriter(logger)) as progressBar:
        for i in range(10):
            progressBar.update(10)
    ```

    This will cause all tqdm progress bar updates to be logged by your logger. However, the filter will prevent them
    from actually being output if they contain the "interactive": True attribute in their extra dict.

    This filter can be used to prevent tqdm progress bars from being logged, e.g. when running in a non-interactive
    environment like pytest.
    '''
    def filter(self, record: logging.LogRecord) -> bool: ...

class _DuplicateNFilter(logging.Filter):
    """A filter that allows the first N duplicate log messages to be emitted.

    The filter counts the number of times each unique log message (based on message text and location) has been emitted.
    It allows the first `max_occurrences` and suppresses subsequent duplicates.

    When the number of unique messages exceeds `max_tracked_messages`, it clears the stored counts to manage memory
    usage.

    This filter can be configured to apply only to specific log levels.

    Note this filter is not thread-safe.
    """
    logged_messages: Incomplete
    max_occurrences: Incomplete
    max_tracked_messages: Incomplete
    levels: Incomplete
    def __init__(self, max_occurrences: int = 5, levels: tuple[int] | None = None, max_tracked_messages: int = 10000) -> None: ...
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter out duplicate log messages based on message text and location."""
