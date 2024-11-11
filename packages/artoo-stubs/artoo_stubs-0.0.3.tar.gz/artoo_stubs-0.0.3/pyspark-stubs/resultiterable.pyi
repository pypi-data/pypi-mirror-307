from typing import Iterable, Iterator, TypeVar

from _typeshed import Incomplete
from pyspark._typing import SizedIterable

__all__ = ['ResultIterable']

T = TypeVar('T')

class ResultIterable(Iterable[T]):
    data: Incomplete
    index: int
    maxindex: Incomplete
    def __init__(self, data: SizedIterable[T]) -> None: ...
    def __iter__(self) -> Iterator[T]: ...
    def __len__(self) -> int: ...
