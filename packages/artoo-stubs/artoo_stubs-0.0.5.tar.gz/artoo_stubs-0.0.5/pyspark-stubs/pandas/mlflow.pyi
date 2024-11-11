import pandas as pd
from pyspark.pandas._typing import Dtype
from pyspark.pandas.frame import DataFrame
from pyspark.pandas.series import Series

__all__ = ['PythonModelWrapper', 'load_model']

class PythonModelWrapper:
    def __init__(self, model_uri: str, return_type_hint: str | type | Dtype) -> None: ...
    def predict(self, data: DataFrame | pd.DataFrame) -> Series | pd.Series: ...

def load_model(model_uri: str, predict_type: str | type | Dtype = 'infer') -> PythonModelWrapper: ...
