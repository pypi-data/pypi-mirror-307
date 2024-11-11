from typing import Any

from pyspark.pandas.frame import DataFrame
from pyspark.sql import SparkSession

__all__ = ['sql']

def sql(query: str, index_col: str | list[str] | None = None, globals: dict[str, Any] | None = None, locals: dict[str, Any] | None = None, **kwargs: Any) -> DataFrame: ...

class SQLProcessor:
    def __init__(self, scope: dict[str, Any], statement: str, session: SparkSession) -> None: ...
    def execute(self, index_col: str | list[str] | None) -> DataFrame: ...
