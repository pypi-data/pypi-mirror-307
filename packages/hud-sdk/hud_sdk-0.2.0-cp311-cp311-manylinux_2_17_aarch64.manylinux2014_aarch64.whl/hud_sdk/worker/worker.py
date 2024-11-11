import contextlib
import json
import os
import random
import signal
import subprocess
import sys
import threading
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Union,
)  # noqa: F401

from .. import globals
from .._internal import worker_queue
from ..agent.manager.client import Manager, get_manager  # noqa: F401
from ..agent.queue import BaseInfoStructure, BufferBackedCyclicQueue
from ..client import get_client  # noqa: F401
from ..collectors import PerformanceMonitor, get_loaded_modules, runtime_info
from ..config import config
from ..declarations import Declaration, DeclarationsAggregator
from ..endpoint_manager import EndpointsDeclarationsAggregator
from ..forkable import after_fork_in_child
from ..hook import set_hook
from ..invocations_handler import InvocationsHandler
from ..logging import internal_logger, send_logs_handler, user_logger
from ..native import get_hud_running_mode
from ..process_utils import get_current_pid, is_alive
from ..run_mode import disable_hud, should_run_hud
from ..schemas.events import EndpointDeclaration
from ..utils import send_fatal_error, suppress_exceptions_sync
from ..workload_metadata import get_cpu_limit

if TYPE_CHECKING:
    from collections import deque


worker_thread = None  # type: Optional[threading.Thread]


def should_run_worker() -> bool:
    return bool(
        get_hud_running_mode()
        and worker_thread
        and not should_finalize_worker(worker_thread)
    )


def should_finalize_worker(worker_thread: threading.Thread) -> bool:
    for thread in threading.enumerate():
        if thread == worker_thread:
            continue
        if (
            not thread.daemon
            and thread.is_alive()
            and thread.name != "pydevd.CheckAliveThread"
        ):
            return False
    return True


class Task:
    def __init__(
        self, func: Callable[[], Any], interval: float, initial_time: float
    ) -> None:
        self.func = func
        self.interval = interval
        self.last_run = initial_time + random.randint(0, int(interval)) - interval

    def run(self, time: float) -> bool:
        if time - self.last_run >= self.interval:
            self.last_run = time
            self.func()
            return True
        return False


manager_port = None


class Worker:
    def __init__(
        self,
        initialization_event: threading.Event,
        key: Optional[str] = None,
        service: Optional[str] = None,
    ) -> None:
        self.key = key
        self.service = service
        self.declarations = DeclarationsAggregator()
        self.endpoints_declarations = EndpointsDeclarationsAggregator()
        self.invocations_handler = InvocationsHandler()
        self.performance_monitor = PerformanceMonitor(get_cpu_limit())
        self.manager = None  # type: Optional[Manager]
        self.tasks = []  # type: List[Task]
        self.agent_pid = None  # type: Optional[int]
        self.manager_pid = None  # type: Optional[int]
        self.session_id = None  # type: Optional[str]
        self.initialization_event = initialization_event

    def run(self) -> None:
        internal_logger.info("Starting worker")
        is_main_process = True if manager_port is None else False
        try:
            self.key = self.key or os.environ.get("HUD_KEY", None)
            self.service = self.service or os.environ.get("HUD_SERVICE", None)

            if not self.key or not self.service:
                internal_logger.error("HUD_KEY and HUD_SERVICE must be set")
                if is_main_process:
                    user_logger.error(
                        "Not running, HUD_KEY and HUD_SERVICE must be set."
                    )
                disable_hud(should_dump_logs=False)
                return

            if not self.run_agent():
                user_logger.error(
                    "SDK has initiated a graceful shutdown. Your application remains unaffected.",
                )
                disable_hud(should_dump_logs=True, key=self.key, service=self.service)
                return
        finally:
            self.initialization_event.set()

        if not self.connect() or not self.manager:
            internal_logger.error("Failed to connect to manager")
            user_logger.error(
                "SDK has initiated a graceful shutdown. Your application remains unaffected.",
            )
            disable_hud(should_dump_logs=True, key=self.key, service=self.service)
            return

        self.manager.register_process(os.getpid())
        self.agent_pid = self.manager.agent_pid
        self.manager_pid = self.manager.manager_pid
        self.session_id = self.manager.session_id

        with self.manager.get_shared_memory() as memory:
            self._queue = BufferBackedCyclicQueue(
                memory.buf,
                BaseInfoStructure,
                self.manager.shared_memory_lock,
                memory.size,
            )
            self.register_tasks()
            waketime = time.time()
            internal_logger.info("Worker started")
            if is_main_process:
                user_logger.info("Initialized successfully")
            while True:
                if not should_run_worker():
                    self._finalize()
                    break
                waketime = time.time()
                for task in self.tasks:
                    if not get_hud_running_mode():
                        break
                    if task.run(waketime):
                        time.sleep(0.01)
                time.sleep(1)

    def run_agent(self) -> bool:
        try:
            global manager_port
            if manager_port is None:
                networkprocess = subprocess.Popen(
                    [sys.executable, "-m", "hud_sdk.agent", self.key, self.service],  # type: ignore[list-item]
                    stdout=subprocess.PIPE,
                )
                time.sleep(0.4)
                if networkprocess.stdout:
                    manager_port = int(
                        networkprocess.stdout.readline().decode().strip()
                    )
                else:
                    internal_logger.error("Failed to get manager port, stdout is None")
                    return False
                internal_logger.info("Manager port: {}".format(manager_port))
            return True
        except Exception:
            internal_logger.exception("Failed to run agent")
            return False

    def connect(self) -> bool:
        self.manager = get_manager(("localhost", manager_port), config.manager_password)
        self.manager.connect()
        if not self.manager.fully_initialized.wait(
            config.manager_initialization_timeout
        ):
            internal_logger.error("Manager initialization timeout")
            return False
        internal_logger.info("Connected to manager")
        return True

    def write(self, events: Union[Dict[Any, Any], List[Any]], event_type: str) -> None:
        self._queue.push(json.dumps([events, event_type]).encode())

    def register_tasks(self) -> None:
        current_time = time.time()
        self.tasks.append(
            Task(
                lambda: self.process_queue(worker_queue),
                config.process_queue_flush_interval,
                current_time,
            )
        )
        self.tasks.append(
            Task(
                self._dump_declarations,
                config.declarations_flush_interval,
                current_time,
            )
        )
        self.tasks.append(
            Task(
                self._dump_endpoint_declarations,
                config.declarations_flush_interval,
                current_time,
            )
        )
        self.tasks.append(
            Task(
                self._dump_invocations, config.invocations_flush_interval, current_time
            )
        )
        self.tasks.append(
            Task(
                self._dump_flow_metrics,
                config.flow_metrics_flush_interval,
                current_time,
            )
        )
        self.tasks.append(
            Task(self._dump_logs, config.logs_flush_interval, current_time)
        )
        self.tasks.append(
            Task(self._send_runtime, config.workload_data_flush_interval, current_time)
        )
        self.tasks.append(
            Task(
                self._send_performance, config.performace_report_interval, current_time
            )
        )
        self.tasks.append(
            Task(
                self._send_loaded_modules,
                config.modules_report_interval,
                current_time,
            )
        )
        self.tasks.append(
            Task(self._check_agent, config.agent_is_up_check_interval, current_time)
        )

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def process_queue(self, queue: "deque[Any]") -> None:
        qsize = len(queue)
        if not qsize:
            return
        if hasattr(queue, "maxlen") and queue.maxlen == qsize:
            internal_logger.warning("Event queue is full")
        try:
            for item in iter(queue.popleft, None):
                if isinstance(item, Declaration):
                    self.declarations.add_declaration(item)
                elif isinstance(item, EndpointDeclaration):
                    self.endpoints_declarations.add_declaration(item)
                else:
                    internal_logger.warning("Invalid item type: {}".format(type(item)))
                qsize -= 1
                if qsize == 0:
                    break
        except IndexError:
            pass

    def _finalize(self) -> None:
        if not get_hud_running_mode():
            internal_logger.info("HUD is not enabled, skipping finalization")
            return

        internal_logger.info("Finalizing worker")
        self.process_queue(worker_queue)
        self._dump_declarations()
        self._dump_endpoint_declarations()
        self._dump_invocations()
        self._dump_flow_metrics()
        self._dump_logs()

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _dump_declarations(self) -> None:
        latest_declarations = self.declarations.get_and_clear_declarations()
        if latest_declarations:
            declarations = [
                declaration.to_json_data() for declaration in latest_declarations
            ]
            self.write(declarations, latest_declarations[0].get_type())

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _dump_endpoint_declarations(self) -> None:
        latest_declarations = self.endpoints_declarations.get_and_clear_declarations()
        if latest_declarations:
            declarations = [
                declaration.to_json_data() for declaration in latest_declarations
            ]
            self.write(declarations, latest_declarations[0].get_type())

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _dump_invocations(self) -> None:
        invocations = self.invocations_handler.get_and_clear_invocations()
        if invocations:
            invocations_to_send = [
                invocation.to_json_data() for invocation in invocations
            ]
            self.write(invocations_to_send, invocations[0].get_type())

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _dump_flow_metrics(self) -> None:
        if not globals.metrics_aggregator:
            internal_logger.error("Metrics aggregator is not initialized")
            return
        metrics_by_type = globals.metrics_aggregator.get_and_clear_metrics()
        for metrics in metrics_by_type.values():
            if metrics:
                self.write(
                    [metric.to_json_data() for metric in metrics], metrics[0].get_type()
                )

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _dump_logs(self) -> None:
        logs = send_logs_handler.get_and_clear_logs()
        if logs.logs:
            self.write(logs.to_json_data(), "Logs")

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _send_loaded_modules(self) -> None:
        modules = get_loaded_modules()
        self.write(modules.to_json_data(), modules.get_type())

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _send_performance(self) -> None:
        performance = self.performance_monitor.monitor_process()
        if config.log_performance:
            internal_logger.info("performance data", data=performance.to_json_data())
        self.write(performance.to_json_data(), performance.get_type())

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _send_runtime(self) -> None:
        runtime = runtime_info()
        self.write(runtime.to_json_data(), runtime.get_type())

    @suppress_exceptions_sync(default_return_factory=lambda: None)
    def _check_agent(self) -> None:
        if not self.agent_pid or not is_alive(self.agent_pid):
            internal_logger.error("Agent is not running, shutting down")
            self.kill_manager_gracefully()

            disable_hud(
                should_dump_logs=True,
                key=self.key,
                service=self.service,
                session_id=self.session_id,
            )

    def kill_manager_gracefully(self) -> None:
        if self.manager and self.manager_pid and is_alive(self.manager_pid):
            try:
                internal_logger.info("Sending SIGTERM to manager process")
                os.kill(self.manager_pid, signal.SIGTERM)

                timeout = 5
                poll_interval = 0.5

                start_time = time.time()
                while time.time() - start_time < timeout:
                    if not is_alive(self.manager_pid):
                        internal_logger.info("Manager process exited")
                        return
                    time.sleep(poll_interval)

                internal_logger.warning(
                    "Manager process did not exit, sending SIGKILL."
                )
                os.kill(self.manager_pid, signal.SIGKILL)

            except Exception:
                internal_logger.exception("Error terminating manager process")


registered_after_fork = False


def init_hud_thread(key: Optional[str] = None, service: Optional[str] = None) -> None:
    global registered_after_fork
    if config.run_after_fork and not registered_after_fork:
        registered_after_fork = True
        after_fork_in_child.register_callback(lambda: init_hud_thread(key, service))

    is_main_process = True if manager_port is None else False
    user_logger.set_is_main_process(is_main_process)

    set_hook()  # Ensure the hook is set before starting the worker thread

    global worker_thread
    if worker_thread is not None and worker_thread.is_alive():
        internal_logger.info("Worker thread is already running")
        return

    if not should_run_hud():
        disable_hud(should_dump_logs=False)
        return

    # The main thread must block, at least until the `manager_port` global is populated.

    ready_event = threading.Event()

    def target() -> None:
        worker = Worker(ready_event, key, service)
        try:
            worker.run()
        except Exception as e:
            try:
                user_logger.error(
                    "SDK has initiated a graceful shutdown. Your application remains unaffected.",
                )
                internal_logger.exception("Exception in worker thread target")
                send_fatal_error(key, service, "Exception in worker thread target")
            except Exception:
                internal_logger.exception(
                    "Failed to send fatal error", data={"original_error": str(e)}
                )
        finally:
            disable_hud(
                should_dump_logs=True,
                key=key,
                service=service,
                session_id=worker.session_id,
            )
            with contextlib.suppress(Exception):
                if worker.manager:
                    worker.manager.deregister_process(get_current_pid())

    worker_thread = threading.Thread(target=target)
    worker_thread.start()
    if not ready_event.wait(config.agent_start_timeout):
        internal_logger.error("Agent startup timeout")
        user_logger.error(
            "SDK has initiated a graceful shutdown. Your application remains unaffected.",
        )
        disable_hud(should_dump_logs=True, key=key, service=service)
