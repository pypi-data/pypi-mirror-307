import ctypes
import struct
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)

if TYPE_CHECKING:
    from typing import Protocol, Self

    class Lockable(Protocol):
        def acquire(self, blocking: bool = True, timeout: int = -1) -> bool: ...

        def release(self) -> None: ...

        def __enter__(self) -> bool: ...

        def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

else:
    Lockable = Any


class BaseInfoStructure(ctypes.Structure):
    head = 0  # type: int
    tail = 0  # type: int
    buffer_size = 0  # type: int
    available = 0  # type: int
    _fields_ = [
        ("head", ctypes.c_uint32),
        ("tail", ctypes.c_uint32),
        ("buffer_size", ctypes.c_uint32),
        ("available", ctypes.c_uint32),
    ]


InfoStructType = TypeVar("InfoStructType", bound=BaseInfoStructure)
WritableBuffer = Union[memoryview, bytearray]
T = TypeVar("T")


class CyclicBufferView:
    def __init__(self, buffer: WritableBuffer, buffer_size: int):
        self.buffer_size = buffer_size
        self.buffer = buffer  # type: WritableBuffer

    @overload
    def __getitem__(self, key: int) -> int: ...
    @overload
    def __getitem__(self, key: slice) -> bytes: ...

    def __getitem__(self, key: Union[slice, int]) -> Union[bytes, int]:
        if isinstance(key, int):
            if key > 0:
                key = key % self.buffer_size
            return self.buffer[key]
        len = key.stop - key.start
        if self.buffer_size - key.start < len:
            return bytes(self.buffer[key.start : self.buffer_size]) + bytes(
                self.buffer[: len - (self.buffer_size - key.start)]
            )
        else:
            return bytes(self.buffer[key])

    def __setitem__(self, key: slice, value: bytes) -> None:
        if isinstance(key, int):
            if key > 0:
                key = key % self.buffer_size
            self.buffer[key] = value
            return
        len = key.stop - key.start
        if self.buffer_size - key.start < len:
            self.buffer[key.start : self.buffer_size] = value[
                : self.buffer_size - key.start
            ]
            self.buffer[: len - (self.buffer_size - key.start)] = value[
                self.buffer_size - key.start :
            ]
        else:
            self.buffer[key] = value


class BufferBackedCyclicQueue(Generic[InfoStructType]):
    def __init__(
        self,
        buffer: WritableBuffer,
        info_struct_type: Type[InfoStructType],
        lock: Lockable,
        size: int,
    ):
        self._in_sync_context = False
        self.buffer = buffer
        self.info_struct_type = info_struct_type
        self.lock = lock
        self._timeout = -1
        self._buffer_size = size - ctypes.sizeof(info_struct_type)
        if self.buffer_size == 0:
            self.buffer_size = size - ctypes.sizeof(info_struct_type)
            self.available = self.buffer_size

        self.buffer_view = CyclicBufferView(buffer, self.buffer_size)

    def synchronized(func: Callable[..., T]) -> Callable[..., T]:  # type: ignore[misc]
        def synchronization_wrapper(self: "Self", *args: Any, **kwargs: Any) -> T:
            if self._in_sync_context:
                return func(self, *args, **kwargs)
            acquired_lock = False
            try:
                if not self.lock.acquire(timeout=self._timeout):
                    raise TimeoutError("Could not acquire lock")
                acquired_lock = True
                self._in_sync_context = True
                return func(self, *args, **kwargs)
            finally:
                if acquired_lock:
                    self._in_sync_context = False
                    self.lock.release()

        return synchronization_wrapper

    # This should only be used directly in a synchronized context
    @property
    @synchronized
    def _info(self) -> InfoStructType:
        return self.info_struct_type.from_buffer(self.buffer, self._buffer_size)

    @property
    @synchronized
    def head(self) -> int:
        return self._info.head

    @head.setter
    @synchronized
    def head(self, value: int) -> None:
        self._info.head = value

    @property
    @synchronized
    def tail(self) -> int:
        return self._info.tail

    @tail.setter
    @synchronized
    def tail(self, value: int) -> None:
        self._info.tail = value

    @property
    @synchronized
    def buffer_size(self) -> int:
        return self._info.buffer_size

    @buffer_size.setter
    @synchronized
    def buffer_size(self, value: int) -> None:
        self._info.buffer_size = value

    @property
    @synchronized
    def available(self) -> int:
        return self._info.available

    @available.setter
    @synchronized
    def available(self, value: int) -> None:
        self._info.available = value

    @synchronized
    def push(self, data: bytes) -> bool:
        data_to_write = struct.pack("I", len(data)) + data
        if len(data_to_write) > self._info.available:
            return False

        address = self._info.tail
        self._info.available -= len(data_to_write)

        self.buffer_view[address : address + len(data_to_write)] = data_to_write

        self._info.tail = (address + len(data_to_write)) % self.buffer_size
        return True

    @synchronized
    def popleft(self) -> Optional[bytes]:
        if self._info.head == self._info.tail and self._info.available > 0:
            return None

        len_address = self._info.head
        data_address = len_address + 4
        length = struct.unpack(
            "I", bytearray(self.buffer_view[self._info.head : self._info.head + 4])
        )[0]
        data = self.buffer_view[data_address : data_address + length]
        self._info.head = (data_address + length) % self.buffer_size
        self._info.available += length + 4
        return data

    del synchronized
