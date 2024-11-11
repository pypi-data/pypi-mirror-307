from typing import TypeVar

from _typeshed import Incomplete
from numpy import ndarray
from py4j.java_gateway import JavaObject
from pyspark.mllib.linalg import Vector as Vector

VectorLike = ndarray | Vector | list[float] | tuple[float, ...]
C = TypeVar('C', bound=type)
JavaObjectOrPickleDump = JavaObject | bytearray | bytes
CorrMethodType: Incomplete
KolmogorovSmirnovTestDistNameType: Incomplete
NormType: Incomplete
