from tlc.client.session import Session as Session
from tlc.core.objects.mutable_objects.run import Run as Run
from tlc.core.url import Url as Url
from typing import Any

def log(data: dict[str, Any], run: Run | Url | None = None) -> None:
    """Log data to the 3LC service.

    :param data: The data to log.
    """
