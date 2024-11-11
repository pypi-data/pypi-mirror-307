import contextlib
import os
from typing import Optional

from ._internal import worker_queue
from .logging import internal_logger, send_logs_handler
from .native import (
    get_and_swap_aggregations,
    get_hud_running_mode,
    set_hud_running_mode,
)
from .utils import dump_logs_sync


def should_run_hud() -> bool:
    hud_env_var = os.environ.get("HUD_ENABLE", False)
    if hud_env_var is False:
        internal_logger.info("HUD_ENABLE is not set")
        return False
    if not (
        isinstance(hud_env_var, str)
        and hud_env_var.lower() == "true"
        or hud_env_var == "1"
    ):
        internal_logger.info("HUD_ENABLE is not set to 'true' or '1'")
        return False
    if not get_hud_running_mode():
        internal_logger.info("HUD is not enabled")
        return False
    return True


def disable_hud(
    should_dump_logs: bool,
    should_clear: bool = True,
    key: Optional[str] = None,
    service: Optional[str] = None,
    session_id: Optional[str] = None,
) -> None:
    internal_logger.info(
        "Disabling HUD"
    )  # It will print to the console if HUD_DEBUG is set
    set_hud_running_mode(False)

    if should_dump_logs and key and service:
        with contextlib.suppress(Exception):
            dump_logs_sync(key, service, session_id)

    if should_clear:
        clear_hud()


def clear_hud() -> None:
    worker_queue.clear()

    get_and_swap_aggregations().clear()
    # we have two dictionaries swapping
    get_and_swap_aggregations().clear()

    send_logs_handler.get_and_clear_logs()


def enable_hud() -> None:
    set_hud_running_mode(True)
