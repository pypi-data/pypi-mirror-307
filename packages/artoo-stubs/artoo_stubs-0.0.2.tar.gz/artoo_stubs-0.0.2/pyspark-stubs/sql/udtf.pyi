from _typeshed import Incomplete
from pyspark.sql._typing import ColumnOrName
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.session import SparkSession
from pyspark.sql.types import StructType

__all__ = ['UDTFRegistration']

class UserDefinedTableFunction:
    func: Incomplete
    evalType: Incomplete
    deterministic: Incomplete
    def __init__(self, func: type, returnType: StructType | str, name: str | None = None, evalType: int = ..., deterministic: bool = False) -> None: ...
    @property
    def returnType(self) -> StructType: ...
    def __call__(self, *cols: ColumnOrName) -> DataFrame: ...
    def asDeterministic(self) -> UserDefinedTableFunction: ...

class UDTFRegistration:
    sparkSession: Incomplete
    def __init__(self, sparkSession: SparkSession) -> None: ...
    def register(self, name: str, f: UserDefinedTableFunction) -> UserDefinedTableFunction: ...
