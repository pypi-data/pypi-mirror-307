from typing import Callable, Mapping

from _typeshed import Incomplete
from pyspark import SparkContext as SparkContext
from pyspark.ml.util import try_remote_functions as try_remote_functions
from pyspark.sql._typing import UserDefinedFunctionLike as UserDefinedFunctionLike
from pyspark.sql.column import Column as Column
from pyspark.sql.functions import pandas_udf as pandas_udf
from pyspark.sql.types import (
    ArrayType as ArrayType,
    ByteType as ByteType,
    DataType as DataType,
    DoubleType as DoubleType,
    FloatType as FloatType,
    IntegerType as IntegerType,
    LongType as LongType,
    ShortType as ShortType,
    StringType as StringType,
    StructType as StructType,
)

supported_scalar_types: Incomplete
PredictBatchFunction: Incomplete

def vector_to_array(col: Column, dtype: str = 'float64') -> Column: ...
def array_to_vector(col: Column) -> Column: ...
def predict_batch_udf(make_predict_fn: Callable[[], PredictBatchFunction], *, return_type: DataType, batch_size: int, input_tensor_shapes: list[list[int] | None] | Mapping[int, list[int]] | None = None) -> UserDefinedFunctionLike: ...
