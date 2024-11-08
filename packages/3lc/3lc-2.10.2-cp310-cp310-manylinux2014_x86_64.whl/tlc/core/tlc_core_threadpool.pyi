import concurrent.futures
from typing import Any

def submit_future(*args: Any, **kwargs: Any) -> concurrent.futures.Future: ...
