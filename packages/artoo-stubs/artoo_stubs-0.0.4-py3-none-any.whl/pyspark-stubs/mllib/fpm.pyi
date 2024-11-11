from typing import Any, Generic, NamedTuple, TypeVar

from pyspark import SparkContext
from pyspark.mllib.common import JavaModelWrapper
from pyspark.mllib.util import JavaLoader, JavaSaveable
from pyspark.rdd import RDD

__all__ = ['FPGrowth', 'FPGrowthModel', 'PrefixSpan', 'PrefixSpanModel']

T = TypeVar('T')

class FPGrowthModel(JavaModelWrapper, JavaSaveable, JavaLoader['FPGrowthModel']):
    def freqItemsets(self) -> RDD['FPGrowth.FreqItemset']: ...
    @classmethod
    def load(cls, sc: SparkContext, path: str) -> FPGrowthModel: ...

class FPGrowth:
    @classmethod
    def train(cls, data: RDD[list[T]], minSupport: float = 0.3, numPartitions: int = -1) -> FPGrowthModel: ...
    class FreqItemset(NamedTuple):
        items: list[Any]
        freq: int

class PrefixSpanModel(JavaModelWrapper, Generic[T]):
    def freqSequences(self) -> RDD['PrefixSpan.FreqSequence']: ...

class PrefixSpan:
    @classmethod
    def train(cls, data: RDD[list[list[T]]], minSupport: float = 0.1, maxPatternLength: int = 10, maxLocalProjDBSize: int = 32000000) -> PrefixSpanModel[T]: ...
    class FreqSequence(NamedTuple):
        sequence: list[list[Any]]
        freq: int
