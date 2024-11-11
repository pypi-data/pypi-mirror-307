from enum import Enum
from typing import NamedTuple

from _typeshed import Incomplete
from pyspark.pandas.exceptions import PandasNotImplementedError as PandasNotImplementedError

MAX_MISSING_PARAMS_SIZE: int
COMMON_PARAMETER_SET: Incomplete
MODULE_GROUP_MATCH: Incomplete
RST_HEADER: str

class Implemented(Enum):
    IMPLEMENTED = 'Y'
    NOT_IMPLEMENTED = 'N'
    PARTIALLY_IMPLEMENTED = 'P'

class SupportedStatus(NamedTuple):
    implemented: str
    missing: str

def generate_supported_api(output_rst_file_path: str) -> None: ...
