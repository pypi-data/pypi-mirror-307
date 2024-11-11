from typing import Generic, TypeVar

from py4j.java_gateway import JavaObject as JavaObject
from pyspark import since as since
from pyspark.context import SparkContext as SparkContext
from pyspark.mllib._typing import VectorLike as VectorLike
from pyspark.mllib.common import callMLlibFunc as callMLlibFunc, inherit_doc as inherit_doc
from pyspark.mllib.linalg import SparseVector as SparseVector, Vector as Vector, Vectors as Vectors
from pyspark.mllib.regression import LabeledPoint as LabeledPoint
from pyspark.rdd import RDD as RDD
from pyspark.sql.dataframe import DataFrame as DataFrame

T = TypeVar('T')
L = TypeVar('L', bound='Loader')
JL = TypeVar('JL', bound='JavaLoader')

class MLUtils:
    @staticmethod
    def loadLibSVMFile(sc: SparkContext, path: str, numFeatures: int = -1, minPartitions: int | None = None) -> RDD['LabeledPoint']: ...
    @staticmethod
    def saveAsLibSVMFile(data: RDD['LabeledPoint'], dir: str) -> None: ...
    @staticmethod
    def loadLabeledPoints(sc: SparkContext, path: str, minPartitions: int | None = None) -> RDD['LabeledPoint']: ...
    @staticmethod
    def appendBias(data: Vector) -> Vector: ...
    @staticmethod
    def loadVectors(sc: SparkContext, path: str) -> RDD[Vector]: ...
    @staticmethod
    def convertVectorColumnsToML(dataset: DataFrame, *cols: str) -> DataFrame: ...
    @staticmethod
    def convertVectorColumnsFromML(dataset: DataFrame, *cols: str) -> DataFrame: ...
    @staticmethod
    def convertMatrixColumnsToML(dataset: DataFrame, *cols: str) -> DataFrame: ...
    @staticmethod
    def convertMatrixColumnsFromML(dataset: DataFrame, *cols: str) -> DataFrame: ...

class Saveable:
    def save(self, sc: SparkContext, path: str) -> None: ...

class JavaSaveable(Saveable):
    def save(self, sc: SparkContext, path: str) -> None: ...

class Loader(Generic[T]):
    @classmethod
    def load(cls, sc: SparkContext, path: str) -> L: ...

class JavaLoader(Loader[T]):
    @classmethod
    def load(cls, sc: SparkContext, path: str) -> JL: ...

class LinearDataGenerator:
    @staticmethod
    def generateLinearInput(intercept: float, weights: VectorLike, xMean: VectorLike, xVariance: VectorLike, nPoints: int, seed: int, eps: float) -> list['LabeledPoint']: ...
    @staticmethod
    def generateLinearRDD(sc: SparkContext, nexamples: int, nfeatures: int, eps: float, nParts: int = 2, intercept: float = 0.0) -> RDD['LabeledPoint']: ...
