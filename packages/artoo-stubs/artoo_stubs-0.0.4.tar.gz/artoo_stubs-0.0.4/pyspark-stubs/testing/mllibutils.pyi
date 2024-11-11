import unittest

from _typeshed import Incomplete
from pyspark import SparkContext as SparkContext
from pyspark.sql import SparkSession as SparkSession

class MLlibTestCase(unittest.TestCase):
    sc: Incomplete
    spark: Incomplete
    def setUp(self) -> None: ...
    def tearDown(self) -> None: ...
