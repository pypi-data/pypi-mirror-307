from abc import ABCMeta
from typing import Generic, TypeVar

from py4j.java_gateway import JavaClass as JavaClass, JavaObject as JavaObject
from pyspark import SparkContext as SparkContext, since as since
from pyspark.ml import (
    Estimator as Estimator,
    Model as Model,
    PredictionModel as PredictionModel,
    Predictor as Predictor,
    Transformer as Transformer,
)
from pyspark.ml._typing import ParamMap as ParamMap
from pyspark.ml.base import _PredictorParams
from pyspark.ml.common import inherit_doc as inherit_doc
from pyspark.ml.param import Param as Param, Params as Params
from pyspark.sql import DataFrame as DataFrame

T = TypeVar('T')
JW = TypeVar('JW', bound='JavaWrapper')
JM = TypeVar('JM', bound='JavaTransformer')
JP = TypeVar('JP', bound='JavaParams')

class JavaWrapper:
    def __init__(self, java_obj: JavaObject | None = None) -> None: ...
    def __del__(self) -> None: ...

class JavaParams(JavaWrapper, Params, metaclass=ABCMeta):
    def copy(self, extra: ParamMap | None = None) -> JP: ...
    def clear(self, param: Param) -> None: ...

class JavaEstimator(JavaParams, Estimator[JM], metaclass=ABCMeta): ...
class JavaTransformer(JavaParams, Transformer, metaclass=ABCMeta): ...

class JavaModel(JavaTransformer, Model, metaclass=ABCMeta):
    def __init__(self, java_model: JavaObject | None = None) -> None: ...

class JavaPredictor(Predictor, JavaEstimator[JM], _PredictorParams, Generic[JM], metaclass=ABCMeta): ...

class JavaPredictionModel(PredictionModel[T], JavaModel, _PredictorParams):
    @property
    def numFeatures(self) -> int: ...
    def predict(self, value: T) -> float: ...
