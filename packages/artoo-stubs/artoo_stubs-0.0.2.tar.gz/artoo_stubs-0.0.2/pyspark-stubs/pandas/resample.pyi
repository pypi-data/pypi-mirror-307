from abc import ABCMeta
from typing import Any, Generic

from pyspark import SparkContext as SparkContext
from pyspark.pandas._typing import FrameLike as FrameLike
from pyspark.pandas.frame import DataFrame as DataFrame
from pyspark.pandas.internal import (
    SPARK_DEFAULT_INDEX_NAME as SPARK_DEFAULT_INDEX_NAME,
    InternalField as InternalField,
    InternalFrame as InternalFrame,
)
from pyspark.pandas.missing.resample import (
    MissingPandasLikeDataFrameResampler as MissingPandasLikeDataFrameResampler,
    MissingPandasLikeSeriesResampler as MissingPandasLikeSeriesResampler,
)
from pyspark.pandas.series import Series as Series, first_series as first_series
from pyspark.pandas.spark.functions import timestampdiff as timestampdiff
from pyspark.pandas.utils import scol_for as scol_for, verify_temp_column_name as verify_temp_column_name
from pyspark.sql import Column as Column
from pyspark.sql.types import (
    DataType as DataType,
    NumericType as NumericType,
    StructField as StructField,
    TimestampNTZType as TimestampNTZType,
)
from pyspark.sql.utils import is_remote as is_remote

class Resampler(Generic[FrameLike], metaclass=ABCMeta):
    def __init__(self, psdf: DataFrame, resamplekey: Series | None, rule: str, closed: str | None = None, label: str | None = None, agg_columns: list[Series] = []) -> None: ...
    def get_make_interval(self, unit: str, col: Column | int | float) -> Column: ...
    def min(self) -> FrameLike: ...
    def max(self) -> FrameLike: ...
    def sum(self) -> FrameLike: ...
    def mean(self) -> FrameLike: ...
    def std(self) -> FrameLike: ...
    def var(self) -> FrameLike: ...

class DataFrameResampler(Resampler[DataFrame]):
    def __init__(self, psdf: DataFrame, resamplekey: Series | None, rule: str, closed: str | None = None, label: str | None = None, agg_columns: list[Series] = []) -> None: ...
    def __getattr__(self, item: str) -> Any: ...

class SeriesResampler(Resampler[Series]):
    def __init__(self, psser: Series, resamplekey: Series | None, rule: str, closed: str | None = None, label: str | None = None, agg_columns: list[Series] = []) -> None: ...
    def __getattr__(self, item: str) -> Any: ...
