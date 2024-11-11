from pyspark.pandas.utils import verify_temp_column_name as verify_temp_column_name
from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql.window import Window as Window

CORRELATION_VALUE_1_COLUMN: str
CORRELATION_VALUE_2_COLUMN: str
CORRELATION_CORR_OUTPUT_COLUMN: str
CORRELATION_COUNT_OUTPUT_COLUMN: str

def compute(sdf: SparkDataFrame, groupKeys: list[str], method: str) -> SparkDataFrame: ...
