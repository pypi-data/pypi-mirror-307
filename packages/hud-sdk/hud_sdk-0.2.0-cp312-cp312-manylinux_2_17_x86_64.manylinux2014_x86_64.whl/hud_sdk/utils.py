import sys
from functools import wraps
from typing import Any, Callable, Coroutine, Optional, TypeVar
from uuid import UUID, uuid5

from .client import get_client
from .config import config
from .exception_handler import FatalErrorData
from .logging import internal_logger, send_logs_handler
from .native import check_linked_code, mark_linked_code
from .process_utils import get_current_pid
from .schemas.requests import SessionlessLogs
from .version import version

T = TypeVar("T")


def suppress_exceptions_async(
    default_return_factory: Callable[[], T],
) -> Callable[
    [Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]
]:
    def decorator(
        func: Callable[..., Coroutine[Any, Any, T]]
    ) -> Callable[..., Coroutine[Any, Any, T]]:
        @wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                internal_logger.exception(
                    "Exception in {}: {}".format(func.__name__, e)
                )
                return default_return_factory()

        return async_wrapper

    return decorator


def suppress_exceptions_sync(
    default_return_factory: Callable[[], T],
) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except Exception:
                internal_logger.exception(
                    "Supressed exception in function", data=dict(function=func.__name__)
                )
                return default_return_factory()

        return sync_wrapper

    return decorator


def mark_linked_function(function: Callable[..., Any]) -> None:
    if hasattr(function, "__code__"):
        if not check_linked_code(function.__code__):
            mark_linked_code(function.__code__)
    elif hasattr(function, "__call__") and hasattr(function.__call__, "__code__"):
        if not check_linked_code(function.__call__.__code__):
            mark_linked_code(function.__call__.__code__)
    else:
        name = getattr(function, "__name__", None)
        internal_logger.warning("Could not mark linked code", data={"function": name})


def calculate_uuid(unique_str: str) -> UUID:
    return uuid5(config.uuid_namespace, unique_str)


def send_fatal_error(
    key: Optional[str], service: Optional[str], message: Optional[str] = None
) -> None:
    client = None
    try:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        client = get_client(key, service, False)
        fatal_error = FatalErrorData(
            exc_type=exc_type,
            exc_value=exc_value,
            exc_traceback=exc_traceback,
            pid=get_current_pid(),
            extra_message=message,
        )
        client.send_fatal_error(fatal_error)
    except Exception:
        pass
    finally:
        if client:
            client.close()


def dump_logs_sync(key: str, service: str, session_id: Optional[str]) -> None:
    client = None
    try:
        client = get_client(key, service, False)
        logs = send_logs_handler.get_and_clear_logs()
        if session_id:
            client.set_session_id(session_id)
            client.send_logs_json(logs.to_json_data(), "Logs")
        else:
            sessionless_logs = SessionlessLogs(logs, key, service, version)
            client.send_sessionless_logs_json(
                sessionless_logs.to_json_data(), "SessionlessLogs"
            )
    finally:
        if client:
            client.close()
