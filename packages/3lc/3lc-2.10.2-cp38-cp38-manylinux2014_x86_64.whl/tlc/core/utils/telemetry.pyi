from _typeshed import Incomplete
from datetime import datetime
from sentry_sdk.integrations import Integration
from tlc.core.utils.track_project_metadata import compute_project_usage_metadata as compute_project_usage_metadata, get_project_usage_metadata as get_project_usage_metadata
from tlcsaas.api_key import SentryConfiguration as SentryConfiguration
from typing import Any

class JupyterExcepthookIntegration(Integration):
    """Hook into Jupyter's excepthook to capture unhandled exceptions so that they get reported to Sentry."""
    identifier: str
    @staticmethod
    def setup_once() -> None: ...

class Telemetry:
    """Telemetry class for 3LC.

    This class is responsible for initializing the telemetry system for 3LC.
    """
    telemetry_instance: Telemetry | None
    def __init__(self) -> None: ...
    @staticmethod
    def instance() -> Telemetry:
        """Get the telemetry instance."""
    @staticmethod
    def get_sentry_environment() -> str:
        '''Get the Sentry environment.

        This method uses various heuristics to determine the environment in which the code is running.

        1. If the TLC_SENTRY_ENVIRONMENT environment variable is set, it will take precedence over the other logic.
        2. If the tlc module is installed from a wheel, the environment will be set to "production".
        3. If neither of these are set, we will assume that we are running from a development environment.
        '''
    @staticmethod
    def get_sentry_config() -> SentryConfiguration: ...
    @staticmethod
    def get_sentry_dashboard_config() -> dict: ...
    @property
    def is_enabled(self) -> bool: ...
    def should_capture_messages(self, is_include_object_service: bool = True) -> bool: ...
    LogLevelStr: Incomplete
    def capture_message(self, message_text: str, message_tags: dict[str, Any] | None = None, message_extras: dict[str, Any] | None = None, level: LogLevelStr = 'info', include_stack_trace: bool = False) -> None: ...

class RunningMessage:
    session_id: Incomplete
    start_time: Incomplete
    trigger_time: Incomplete
    def __init__(self, session_id: str, start_time: datetime) -> None: ...
    async def consider_message(self) -> None: ...
