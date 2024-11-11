import unittest

from _typeshed import Incomplete
from google.rpc import error_details_pb2 as error_details_pb2
from pyspark import Row as Row, SparkConf as SparkConf
from pyspark.sql.connect.dataframe import DataFrame as DataFrame
from pyspark.sql.connect.plan import SQL as SQL, LogicalPlan as LogicalPlan, Range as Range, Read as Read
from pyspark.sql.connect.session import SparkSession as SparkSession
from pyspark.testing.sqlutils import (
    SQLTestUtils as SQLTestUtils,
    have_pandas as have_pandas,
    pandas_requirement_message as pandas_requirement_message,
    pyarrow_requirement_message as pyarrow_requirement_message,
)
from pyspark.testing.utils import PySparkErrorTestUtils as PySparkErrorTestUtils

grpc_requirement_message: Incomplete
have_grpc: Incomplete
grpc_status_requirement_message: Incomplete
have_grpc_status: Incomplete
googleapis_common_protos_requirement_message: Incomplete
have_googleapis_common_protos: Incomplete
connect_requirement_message: Incomplete
should_test_connect: str

class MockRemoteSession:
    hooks: Incomplete
    session_id: Incomplete
    def __init__(self) -> None: ...
    def set_hook(self, name, hook) -> None: ...
    def drop_hook(self, name) -> None: ...
    def __getattr__(self, item): ...

class MockDF(DataFrame):
    def __init__(self, session: SparkSession, plan: LogicalPlan) -> None: ...
    def __getattr__(self, name): ...

class PlanOnlyTestFixture(unittest.TestCase, PySparkErrorTestUtils):
    @classmethod
    def setUpClass(cls) -> None: ...
    @classmethod
    def tearDownClass(cls) -> None: ...

class ReusedConnectTestCase(unittest.TestCase, SQLTestUtils, PySparkErrorTestUtils):
    @classmethod
    def conf(cls): ...
    @classmethod
    def master(cls): ...
    @classmethod
    def setUpClass(cls) -> None: ...
    @classmethod
    def tearDownClass(cls) -> None: ...
