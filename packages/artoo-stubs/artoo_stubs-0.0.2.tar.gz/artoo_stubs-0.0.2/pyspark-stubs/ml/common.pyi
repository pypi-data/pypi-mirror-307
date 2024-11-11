from typing import Any, Callable

import pyspark.context
from pyspark import RDD as RDD, SparkContext as SparkContext
from pyspark.ml._typing import C as C, JavaObjectOrPickleDump as JavaObjectOrPickleDump
from pyspark.serializers import AutoBatchedSerializer as AutoBatchedSerializer, CPickleSerializer as CPickleSerializer
from pyspark.sql import DataFrame as DataFrame, SparkSession as SparkSession

def callJavaFunc(sc: pyspark.context.SparkContext, func: Callable[..., 'JavaObjectOrPickleDump'], *args: Any) -> JavaObjectOrPickleDump: ...
def inherit_doc(cls) -> C: ...
