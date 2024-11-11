import multiprocessing
import time
from contextlib import closing
from functools import wraps
from multiprocessing import resource_tracker
from multiprocessing.managers import BaseManager, BaseProxy
from multiprocessing.shared_memory import SharedMemory
from threading import Lock, get_ident
from typing import Any, Callable, Literal, Optional, Set, Tuple, TypeVar, Union, cast

from ...process_utils import get_current_pid
from ...run_mode import disable_hud
from ...utils import send_fatal_error


# Copied and modified from threading._RLock
class RLock:
    """This class implements reentrant lock objects.

    A reentrant lock must be released by the thread that acquired it. Once a
    thread has acquired a reentrant lock, the same thread may acquire it
    again without blocking; the thread must release it once for each time it
    has acquired it.
    """

    def __init__(self) -> None:
        self._block = Lock()
        self._internal_lock = Lock()
        self._owner = None  # type: Union[int, Tuple[int, int], None]
        self._count = 0
        self._lock_time = 0.0

    def _at_fork_reinit(self) -> None:
        self._internal_lock._at_fork_reinit()  # type: ignore[attr-defined]
        self._block._at_fork_reinit()  # type: ignore[attr-defined]
        self._owner = None
        self._count = 0

    def acquire(
        self,
        blocking: bool = True,
        timeout: int = -1,
        *,
        ident: Optional[Tuple[int, int]] = None,
    ) -> Union[bool, Literal[1]]:
        """Acquire a lock, blocking or non-blocking.

        When invoked without arguments: if this thread already owns the lock,
        increment the recursion level by one, and return immediately. Otherwise,
        if another thread owns the lock, block until the lock is unlocked. Once
        the lock is unlocked (not owned by any thread), then grab ownership, set
        the recursion level to one, and return. If more than one thread is
        blocked waiting until the lock is unlocked, only one at a time will be
        able to grab ownership of the lock. There is no return value in this
        case.

        When invoked with the blocking argument set to true, do the same thing
        as when called without arguments, and return true.

        When invoked with the blocking argument set to false, do not block. If a
        call without an argument would block, return false immediately;
        otherwise, do the same thing as when called without arguments, and
        return true.

        When invoked with the floating-point timeout argument set to a positive
        value, block for at most the number of seconds specified by timeout
        and as long as the lock cannot be acquired.  Return true if the lock has
        been acquired, false if the timeout has elapsed.

        """
        if ident:
            me = ident  # type: Union[int, Tuple[int, int]]
        else:
            me = get_ident()
        with self._internal_lock:
            if self._owner == me:
                self._count += 1
                return 1
        rc = self._block.acquire(blocking, timeout)
        with self._internal_lock:
            if rc:
                self._owner = me
                self._count = 1
                self._lock_time = time.time()
            return rc

    def release(self, *, ident: Optional[Tuple[int, int]] = None) -> None:
        """Release a lock, decrementing the recursion level.

        If after the decrement it is zero, reset the lock to unlocked (not owned
        by any thread), and if any other threads are blocked waiting for the
        lock to become unlocked, allow exactly one of them to proceed. If after
        the decrement the recursion level is still nonzero, the lock remains
        locked and owned by the calling thread.

        Only call this method when the calling thread owns the lock. A
        RuntimeError is raised if this method is called when the lock is
        unlocked.

        There is no return value.

        """
        if ident:
            me = ident  # type: Union[int, Tuple[int, int]]
        else:
            me = get_ident()
        with self._internal_lock:
            if self._owner != me:
                raise RuntimeError("cannot release un-acquired lock")
            self._count = count = self._count - 1
            if not count:
                self._owner = None
                self._lock_time = 0.0
                self._block.release()

    def get_owner_and_locktime(
        self,
    ) -> Optional[Tuple[Union[int, Tuple[int, int]], float]]:
        with self._internal_lock:
            if self._owner is None:
                return None
            return self._owner, self._lock_time


T = TypeVar("T")


def safe_manager_call(func: Callable[..., T]) -> Callable[..., T]:
    @wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return func(*args, **kwargs)
        except AttributeError:
            # Used for hasattr checks
            raise
        except BaseException:
            send_fatal_error(None, None, "Exception in manager call")
            # We don't send logs here, we will send them later. That's why we don't clear now.
            disable_hud(should_dump_logs=False, should_clear=False)
            raise

    return sync_wrapper


# These proxy classes are defined, but not exported in multiprocessing.managers. We modify them.
class AcquirerProxy(BaseProxy):
    _exposed_ = ("acquire", "release", "get_owner_and_locktime")

    @safe_manager_call
    def acquire(self, blocking: bool = True, timeout: Optional[int] = None) -> bool:
        args = (blocking,) if timeout is None else (blocking, timeout)
        return self._callmethod("acquire", args, kwds={"ident": (get_current_pid(), get_ident())})  # type: ignore[func-returns-value, no-any-return]

    @safe_manager_call
    def release(self) -> None:
        return self._callmethod(
            "release", kwds={"ident": (get_current_pid(), get_ident())}
        )

    @safe_manager_call
    def get_owner_and_locktime(
        self,
    ) -> Optional[Tuple[Union[int, Tuple[int, int]], float]]:
        return self._callmethod("get_owner_and_locktime")  # type: ignore[func-returns-value,no-any-return]

    @safe_manager_call
    def __enter__(self) -> bool:
        return self._callmethod("acquire", kwds={"ident": (get_current_pid(), get_ident())})  # type: ignore[func-returns-value, no-any-return]

    @safe_manager_call
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        return self._callmethod(
            "release", kwds={"ident": (get_current_pid(), get_ident())}
        )


class NamespaceProxy(BaseProxy):
    _exposed_ = ("__getattribute__", "__setattr__", "__delattr__")

    @safe_manager_call
    def __getattr__(self, key: str) -> Any:
        if key[0] == "_":
            return object.__getattribute__(self, key)
        callmethod = object.__getattribute__(self, "_callmethod")
        return callmethod("__getattribute__", (key,))

    @safe_manager_call
    def __setattr__(self, key: str, value: Any) -> None:
        if key[0] == "_":
            return object.__setattr__(self, key, value)
        callmethod = object.__getattribute__(self, "_callmethod")
        return callmethod("__setattr__", (key, value))  # type: ignore[no-any-return]

    @safe_manager_call
    def __delattr__(self, key: str) -> None:
        if key[0] == "_":
            return object.__delattr__(self, key)
        callmethod = object.__getattribute__(self, "_callmethod")
        return callmethod("__delattr__", (key,))  # type: ignore[no-any-return]


class EventProxy(BaseProxy):
    _exposed_ = ("is_set", "set", "clear", "wait")

    @safe_manager_call
    def is_set(self) -> bool:
        return self._callmethod("is_set")  # type: ignore[func-returns-value,no-any-return]

    @safe_manager_call
    def set(self) -> None:
        return self._callmethod("set")

    @safe_manager_call
    def clear(self) -> None:
        return self._callmethod("clear")

    @safe_manager_call
    def wait(self, timeout: Optional[float] = None) -> bool:
        return self._callmethod("wait", (timeout,))  # type: ignore[func-returns-value,no-any-return]


class Manager(BaseManager):

    @safe_manager_call
    def init_manager(self) -> None:
        with self.namespace_lock:
            self.namespace.connected_processes = set()
            self.namespace.agent_pid = 0

    @property
    @safe_manager_call
    def shared_memory_lock(self) -> AcquirerProxy:
        return self._get_shared_memory_lock()

    @property
    @safe_manager_call
    def namespace_lock(self) -> AcquirerProxy:
        return self._get_namespace_lock()

    @property
    @safe_manager_call
    def namespace(self) -> NamespaceProxy:
        return self._get_ns()

    @property
    @safe_manager_call
    def shared_memory_size(self) -> int:
        with self.namespace_lock:
            return self.namespace.shared_memory_size  # type: ignore[no-any-return]

    @shared_memory_size.setter
    @safe_manager_call
    def shared_memory_size(self, size: int) -> None:
        with self.namespace_lock:
            self.namespace.shared_memory_size = size

    @property
    @safe_manager_call
    def shared_memory_name(self) -> str:
        with self.namespace_lock:
            return self.namespace.shared_memory_name  # type: ignore[no-any-return]

    @shared_memory_name.setter
    @safe_manager_call
    def shared_memory_name(self, name: str) -> None:
        with self.namespace_lock:
            self.namespace.shared_memory_name = name

    @safe_manager_call
    def get_shared_memory(self) -> "closing[SharedMemory]":
        with self.shared_memory_lock, self.namespace_lock:
            if not hasattr(self.namespace, "shared_memory_size"):
                raise AttributeError(
                    "shared_memory_size must be set before shared_memory can be accessed"
                )
            if not hasattr(self.namespace, "shared_memory_name"):
                memory = SharedMemory(None, create=True, size=self.shared_memory_size)
                self.namespace.shared_memory_name = memory.name
            else:
                memory = SharedMemory(
                    self.namespace.shared_memory_name,
                    create=False,
                    size=self.shared_memory_size,
                )

                resource_tracker.unregister(
                    "/" + memory.name, "shared_memory"
                )  # Only the creator should unlink the shared memory
            return closing(memory)

    @property
    @safe_manager_call
    def connected_processes(self) -> Set[int]:
        return cast(Set[int], self.namespace.connected_processes)

    @connected_processes.setter
    @safe_manager_call
    def connected_processes(self, processes: Set[int]) -> None:
        with self.namespace_lock:
            self.namespace.connected_processes = processes

    @property
    @safe_manager_call
    def agent_pid(self) -> int:
        if not hasattr(self, "_cached_agent_pid"):
            with self.namespace_lock:
                self._cached_agent_pid = cast(int, self.namespace.agent_pid)
        return self._cached_agent_pid

    @agent_pid.setter
    @safe_manager_call
    def agent_pid(self, pid: int) -> None:
        with self.namespace_lock:
            self.namespace.agent_pid = pid

    @safe_manager_call
    def register_process(self, pid: int) -> None:
        with self.namespace_lock:
            processes = self.connected_processes
            processes.add(pid)
            self.connected_processes = processes

    @safe_manager_call
    def deregister_process(self, pid: int) -> None:
        with self.namespace_lock:
            processes = self.connected_processes
            processes.discard(pid)
            self.connected_processes = processes

    @property
    @safe_manager_call
    def manager_pid(self) -> int:
        if not hasattr(self, "_cached_manager_pid"):
            with self.namespace_lock:
                self._cached_manager_pid = cast(
                    int, self._get_manager_pid()._getvalue()
                )
        return self._cached_manager_pid

    @property
    @safe_manager_call
    def session_id(self) -> Optional[str]:
        with self.namespace_lock:
            if not hasattr(self.namespace, "session_id"):
                return None
            return self.namespace.session_id  # type: ignore[no-any-return]

    @session_id.setter
    @safe_manager_call
    def session_id(self, session_id: str) -> None:
        with self.namespace_lock:
            self.namespace.session_id = session_id

    @property
    @safe_manager_call
    def fully_initialized(self) -> EventProxy:
        return self._get_fully_initialized_event()

    def _get_shared_memory_lock(self) -> AcquirerProxy:
        return NotImplemented

    def _get_namespace_lock(self) -> AcquirerProxy:
        return NotImplemented

    def _get_ns(self) -> NamespaceProxy:
        return NotImplemented

    def _get_manager_pid(self) -> BaseProxy:
        return NotImplemented

    def _get_fully_initialized_event(self) -> EventProxy:
        return NotImplemented


def get_manager(address: Any = None, authkey: Any = None) -> Manager:
    return Manager(address, authkey, ctx=multiprocessing.get_context("spawn"))
