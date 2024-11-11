from typing import Any, TypeVar

from _typeshed import Incomplete
from pyspark.pandas.base import IndexOpsMixin as IndexOpsMixin
from pyspark.pandas.frame import DataFrame as DataFrame
from pyspark.pandas.generic import Frame as Frame
from pyspark.pandas.indexes.base import Index as Index
from pyspark.pandas.series import Series as Series

T = TypeVar('T')
FrameLike = TypeVar('FrameLike', bound='Frame')
IndexOpsLike = TypeVar('IndexOpsLike', bound='IndexOpsMixin')
Scalar: Incomplete
Label = tuple[Any, ...]
Name = Any | Label
Axis = int | str
Dtype: Incomplete
DataFrameOrSeries: Incomplete
SeriesOrIndex: Incomplete
