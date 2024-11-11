from typing import Any, Callable

import pandas as pd
from pyspark.pandas._typing import DataFrameOrSeries as DataFrameOrSeries, Name as Name
from pyspark.pandas.frame import DataFrame as DataFrame
from pyspark.pandas.internal import (
    SPARK_DEFAULT_SERIES_NAME as SPARK_DEFAULT_SERIES_NAME,
    SPARK_INDEX_NAME_FORMAT as SPARK_INDEX_NAME_FORMAT,
    SPARK_INDEX_NAME_PATTERN as SPARK_INDEX_NAME_PATTERN,
    InternalField as InternalField,
    InternalFrame as InternalFrame,
)
from pyspark.pandas.series import Series as Series
from pyspark.pandas.typedef import (
    DataFrameType as DataFrameType,
    ScalarType as ScalarType,
    SeriesType as SeriesType,
    infer_return_type as infer_return_type,
)
from pyspark.pandas.utils import (
    is_name_like_tuple as is_name_like_tuple,
    is_name_like_value as is_name_like_value,
    log_advice as log_advice,
    name_like_string as name_like_string,
    scol_for as scol_for,
    verify_temp_column_name as verify_temp_column_name,
)
from pyspark.sql._typing import UserDefinedFunctionLike as UserDefinedFunctionLike
from pyspark.sql.functions import pandas_udf as pandas_udf
from pyspark.sql.types import DataType as DataType, LongType as LongType, StructField as StructField, StructType as StructType

class PandasOnSparkFrameMethods:
    def __init__(self, frame: DataFrame) -> None: ...
    def attach_id_column(self, id_type: str, column: Name) -> DataFrame: ...
    def apply_batch(self, func: Callable[..., pd.DataFrame], args: tuple = (), **kwds: Any) -> DataFrame: ...
    def transform_batch(self, func: Callable[..., pd.DataFrame | pd.Series], *args: Any, **kwargs: Any) -> DataFrameOrSeries: ...

class PandasOnSparkSeriesMethods:
    def __init__(self, series: Series) -> None: ...
    def transform_batch(self, func: Callable[..., pd.Series], *args: Any, **kwargs: Any) -> Series: ...
