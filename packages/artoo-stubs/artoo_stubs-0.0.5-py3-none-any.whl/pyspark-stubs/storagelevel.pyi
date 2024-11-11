from typing import Any, ClassVar

from _typeshed import Incomplete

__all__ = ['StorageLevel']

class StorageLevel:
    NONE: ClassVar['StorageLevel']
    DISK_ONLY: ClassVar['StorageLevel']
    DISK_ONLY_2: ClassVar['StorageLevel']
    DISK_ONLY_3: ClassVar['StorageLevel']
    MEMORY_ONLY: ClassVar['StorageLevel']
    MEMORY_ONLY_2: ClassVar['StorageLevel']
    MEMORY_AND_DISK: ClassVar['StorageLevel']
    MEMORY_AND_DISK_2: ClassVar['StorageLevel']
    OFF_HEAP: ClassVar['StorageLevel']
    MEMORY_AND_DISK_DESER: ClassVar['StorageLevel']
    useDisk: Incomplete
    useMemory: Incomplete
    useOffHeap: Incomplete
    deserialized: Incomplete
    replication: Incomplete
    def __init__(self, useDisk: bool, useMemory: bool, useOffHeap: bool, deserialized: bool, replication: int = 1) -> None: ...
    def __eq__(self, other: Any) -> bool: ...
