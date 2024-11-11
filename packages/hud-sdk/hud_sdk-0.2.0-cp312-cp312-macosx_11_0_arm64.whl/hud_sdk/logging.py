import traceback
from collections import deque
from datetime import datetime, timezone
from logging import (
    CRITICAL,
    DEBUG,
    ERROR,
    INFO,
    WARNING,
    Formatter,
    Handler,
    Logger,
    LoggerAdapter,
    LogRecord,
    StreamHandler,
    getLogger,
)
from typing import (
    TYPE_CHECKING,
    Any,
    List,  # noqa: F401
    MutableMapping,
    Tuple,
)

from .config import config
from .forkable import ForksafeSequence
from .schemas.events import ExceptionInfo, Log
from .schemas.requests import Logs
from .schemas.schema import JSON  # noqa: F401


class SendToClientHandler(Handler):
    def __init__(
        self,
    ) -> None:
        self._logs = ForksafeSequence(
            lambda: deque(maxlen=config.logs_queue_size)
        )  # type: ForksafeSequence[deque[LogRecord]]
        super().__init__()

    def get_and_clear_logs(self) -> Logs:
        logs_count = len(self._logs)
        logs = []  # type: List[Log]
        while logs_count > 0:
            logs.append(self._record_to_log_event(self._logs.popleft()))
            logs_count -= 1
        return Logs(logs, datetime.now(timezone.utc))

    @staticmethod
    def _record_to_log_event(log_record: LogRecord) -> "Log":
        exc = None
        if log_record.exc_info:
            exc_type, exc_value, exc_traceback = log_record.exc_info
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            exc = ExceptionInfo(
                name=str(getattr(exc_type, "__name__", "")),
                value=str(exc_value),
                stack_trace="".join(tb_lines),
            )

        return Log(
            message=log_record.getMessage(),
            data=getattr(log_record, ExtraDataAdapter.DATA, {}),
            timestamp=log_record.created * 1000,  # time in ms
            level=log_record.levelname,
            pathname=log_record.pathname,
            lineno=log_record.lineno,
            exception=exc,
        )

    def emit(self, record: LogRecord) -> None:
        self._logs.append(record)

    def handleError(self, record: LogRecord) -> None:
        return None


if TYPE_CHECKING:
    _LoggerAdapter = LoggerAdapter[Logger]
else:
    _LoggerAdapter = LoggerAdapter


class ExtraDataAdapter(_LoggerAdapter):
    DATA = "data"

    def __init__(self, logger: Logger):
        super().__init__(logger, {})

    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> Tuple[Any, MutableMapping[str, Any]]:
        extra = kwargs.get("extra", {})
        data = kwargs.pop("data", None)

        if data is not None:
            extra[self.DATA] = data  # Add the custom data to extra

        kwargs["extra"] = extra
        return msg, kwargs


class MainProcessAdapter(_LoggerAdapter):
    def __init__(self, logger: Logger):
        super().__init__(logger, {})
        self.is_main_process = True

    def set_is_main_process(self, is_main_process: bool) -> None:
        self.is_main_process = is_main_process

    def process(
        self, msg: Any, kwargs: MutableMapping[str, Any]
    ) -> Tuple[Any, MutableMapping[str, Any]]:
        extra = kwargs.get("extra", {})
        prefix = "Hud:" if self.is_main_process else "Hud: [pid=%(process)d]"
        extra["prefix"] = prefix
        kwargs["extra"] = extra
        return msg, kwargs


def init_logging(logger_name: str) -> ExtraDataAdapter:
    logger = getLogger(logger_name)
    adapter = ExtraDataAdapter(logger)

    logger.propagate = False  # We don't want the internal logs to be propagated to get to the customer's loggers

    logger.setLevel(DEBUG)
    send_logs_handler.setLevel(config.log_level)
    logger.addHandler(send_logs_handler)

    if config.debug_logs or config.verbose_logs:
        handler = StreamHandler()
        if config.debug_logs:
            handler.setLevel(DEBUG)
        else:
            handler.setLevel(config.log_level)
        FormatterClass = ColorsFormatter if config.pretty_logs else ConsoleFormatter
        handler.setFormatter(
            FormatterClass(
                "{}:%(process)d %(asctime)s.%(msecs)03d [%(levelname)s] %(message)s".format(
                    config.debug_prefix
                ),
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )

        logger.addHandler(handler)

    return adapter


def init_user_logging(logger_name: str) -> MainProcessAdapter:
    user_logger = getLogger(logger_name)
    adapter = MainProcessAdapter(user_logger)

    user_logger.propagate = False
    user_logger.setLevel(INFO)

    handler = StreamHandler()
    handler.setLevel(INFO)
    formatter = UserFormatter("%(prefix)s %(message)s")
    handler.setFormatter(formatter)
    user_logger.addHandler(handler)

    return adapter


class UserFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        if hasattr(record, "prefix"):
            # We want to format the process id inside the prefix
            record.prefix = record.prefix % record.__dict__
        return super().format(record)


class ConsoleFormatter(Formatter):
    def format(self, record: LogRecord) -> str:
        data = getattr(record, ExtraDataAdapter.DATA, {})
        return "%s %s" % (super().format(record), str(data) if data else "")


class ColorsFormatter(ConsoleFormatter):
    COLORS = {
        DEBUG: "\033[34m",  # Blue
        INFO: "\033[32m",  # Green
        WARNING: "\033[33m",  # Yellow
        ERROR: "\033[31m",  # Red
        CRITICAL: "\033[41m",  # Red background
    }
    RESET = "\033[0m"  # Reset color code

    def format(self, record: LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        return "%s%s%s" % (color, super().format(record), self.RESET)


send_logs_handler = SendToClientHandler()
internal_logger = init_logging("hud_sdk.internal")
user_logger = init_user_logging("hud_sdk.user")
