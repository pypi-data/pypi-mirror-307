import sys
import traceback
from types import TracebackType
from typing import Any, Optional, Type

from .client import get_client
from .logging import internal_logger
from .process_utils import get_current_pid


class FatalErrorData:
    def __init__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
        pid: int,
        extra_message: Optional[str] = None,
    ):
        self.error_message = str(exc_value) if exc_value else ""
        self.error_name = exc_type.__name__ if exc_type else ""
        self.error_stack = (
            "".join(traceback.format_tb(exc_traceback)) if exc_traceback else ""
        )
        self.pid = pid
        self.extra_message = extra_message


EXCEPTIONS_TO_IGNORE = [KeyboardInterrupt]


def install_exception_handler() -> None:
    ORIGINAL_EXCEPTHOOK = sys.excepthook

    def exception_handler(
        exc_type: Type[BaseException],
        exc_value: BaseException,
        exc_traceback: Optional[TracebackType],
    ) -> Any:
        client = None
        try:
            if exc_type not in EXCEPTIONS_TO_IGNORE:
                internal_logger.exception("Uncaught exception")

                fatal_error = FatalErrorData(
                    exc_type,
                    exc_value,
                    exc_traceback,
                    get_current_pid(),
                    "Uncaught exception",
                )
                client = get_client(is_async=False)
                client.send_fatal_error(fatal_error)
        except Exception:
            internal_logger.exception("Failed to send fatal error")
        finally:
            try:
                if client:
                    client.close()
            except Exception:
                pass
            return ORIGINAL_EXCEPTHOOK(exc_type, exc_value, exc_traceback)

    sys.excepthook = exception_handler
