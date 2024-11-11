import unittest

from _typeshed import Incomplete
from pyspark import RDD as RDD, SparkConf as SparkConf, SparkContext as SparkContext
from pyspark.streaming import StreamingContext as StreamingContext
from pyspark.testing.utils import search_jar as search_jar

kinesis_test_environ_var: str
should_skip_kinesis_tests: Incomplete
kinesis_requirement_message: str
kinesis_asl_assembly_jar: Incomplete
existing_args: Incomplete
jars_args: Incomplete
should_test_kinesis: Incomplete

class PySparkStreamingTestCase(unittest.TestCase):
    timeout: int
    duration: float
    @classmethod
    def setUpClass(cls) -> None: ...
    @classmethod
    def tearDownClass(cls) -> None: ...
    ssc: Incomplete
    def setUp(self) -> None: ...
    def tearDown(self) -> None: ...
    def wait_for(self, result, n) -> None: ...
