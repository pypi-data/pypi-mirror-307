from _typeshed import Incomplete
from pyspark.serializers import (
    AutoBatchedSerializer as AutoBatchedSerializer,
    BatchedSerializer as BatchedSerializer,
    CompressedSerializer as CompressedSerializer,
    CPickleSerializer as CPickleSerializer,
    FlattenedValuesSerializer as FlattenedValuesSerializer,
)
from pyspark.util import fail_on_stopiteration as fail_on_stopiteration

process: Incomplete

def get_used_memory(): ...

MemoryBytesSpilled: int
DiskBytesSpilled: int

class Aggregator:
    createCombiner: Incomplete
    mergeValue: Incomplete
    mergeCombiners: Incomplete
    def __init__(self, createCombiner, mergeValue, mergeCombiners) -> None: ...

class SimpleAggregator(Aggregator):
    def __init__(self, combiner) -> None: ...

class Merger:
    agg: Incomplete
    def __init__(self, aggregator) -> None: ...
    def mergeValues(self, iterator) -> None: ...
    def mergeCombiners(self, iterator) -> None: ...
    def items(self) -> None: ...

class ExternalMerger(Merger):
    MAX_TOTAL_PARTITIONS: int
    memory_limit: Incomplete
    serializer: Incomplete
    localdirs: Incomplete
    partitions: Incomplete
    batch: Incomplete
    scale: Incomplete
    data: Incomplete
    pdata: Incomplete
    spills: int
    def __init__(self, aggregator, memory_limit: int = 512, serializer: Incomplete | None = None, localdirs: Incomplete | None = None, scale: int = 1, partitions: int = 59, batch: int = 1000) -> None: ...
    def mergeValues(self, iterator) -> None: ...
    def mergeCombiners(self, iterator, limit: Incomplete | None = None) -> None: ...
    def items(self): ...

class ExternalSorter:
    memory_limit: Incomplete
    local_dirs: Incomplete
    serializer: Incomplete
    def __init__(self, memory_limit, serializer: Incomplete | None = None) -> None: ...
    def sorted(self, iterator, key: Incomplete | None = None, reverse: bool = False): ...

class ExternalList:
    LIMIT: int
    values: Incomplete
    count: Incomplete
    def __init__(self, values) -> None: ...
    def __iter__(self): ...
    def __len__(self) -> int: ...
    def append(self, value) -> None: ...
    def __del__(self) -> None: ...

class ExternalListOfList(ExternalList):
    count: Incomplete
    def __init__(self, values) -> None: ...
    def append(self, value) -> None: ...
    def __iter__(self): ...

class GroupByKey:
    iterator: Incomplete
    def __init__(self, iterator) -> None: ...
    def __iter__(self): ...

class ExternalGroupBy(ExternalMerger):
    SORT_KEY_LIMIT: int
    def flattened_serializer(self): ...
