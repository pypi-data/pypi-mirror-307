from abc import ABCMeta
from typing import Any

from pyspark.errors import AnalysisException as AnalysisException
from pyspark.pandas._typing import Label as Label, Name as Name, Scalar as Scalar
from pyspark.pandas.exceptions import (
    SparkPandasIndexingError as SparkPandasIndexingError,
    SparkPandasNotImplementedError as SparkPandasNotImplementedError,
)
from pyspark.pandas.frame import DataFrame as DataFrame
from pyspark.pandas.generic import Frame as Frame
from pyspark.pandas.internal import (
    DEFAULT_SERIES_NAME as DEFAULT_SERIES_NAME,
    NATURAL_ORDER_COLUMN_NAME as NATURAL_ORDER_COLUMN_NAME,
    SPARK_DEFAULT_SERIES_NAME as SPARK_DEFAULT_SERIES_NAME,
    InternalField as InternalField,
    InternalFrame as InternalFrame,
)
from pyspark.pandas.series import Series as Series
from pyspark.pandas.utils import (
    is_name_like_tuple as is_name_like_tuple,
    is_name_like_value as is_name_like_value,
    lazy_property as lazy_property,
    name_like_string as name_like_string,
    same_anchor as same_anchor,
    scol_for as scol_for,
    spark_column_equals as spark_column_equals,
    verify_temp_column_name as verify_temp_column_name,
)
from pyspark.sql.types import BooleanType as BooleanType, DataType as DataType, LongType as LongType
from pyspark.sql.utils import get_column_class as get_column_class

class IndexerLike:
    def __init__(self, psdf_or_psser: Frame) -> None: ...

class AtIndexer(IndexerLike):
    def __getitem__(self, key: Any) -> Series | DataFrame | Scalar: ...

class iAtIndexer(IndexerLike):
    def __getitem__(self, key: Any) -> Series | DataFrame | Scalar: ...

class LocIndexerLike(IndexerLike, metaclass=ABCMeta):
    def __getitem__(self, key: Any) -> Series | DataFrame: ...
    def __setitem__(self, key: Any, value: Any) -> None: ...

class LocIndexer(LocIndexerLike): ...

class iLocIndexer(LocIndexerLike):
    def __setitem__(self, key: Any, value: Any) -> None: ...
