from _typeshed import Incomplete

from .cloudpickle import (
    DEFAULT_PROTOCOL as DEFAULT_PROTOCOL,
    PYPY as PYPY,
    CellType as CellType,
    builtin_code_type as builtin_code_type,
    cell_set as cell_set,
    dynamic_subimport as dynamic_subimport,
    parametrized_type_hint_getinitargs as parametrized_type_hint_getinitargs,
    subimport as subimport,
)
from .compat import Pickler as Pickler, pickle as pickle

def dump(obj, file, protocol: Incomplete | None = None, buffer_callback: Incomplete | None = None) -> None: ...
def dumps(obj, protocol: Incomplete | None = None, buffer_callback: Incomplete | None = None): ...

load: Incomplete
loads: Incomplete

class CloudPickler(Pickler):
    dispatch_table: Incomplete
    def dump(self, obj): ...
    globals_ref: Incomplete
    proto: Incomplete
    def __init__(self, file, protocol: Incomplete | None = None, buffer_callback: Incomplete | None = None) -> None: ...
    def __init__(self, file, protocol: Incomplete | None = None) -> None: ...
    dispatch = dispatch_table
    def reducer_override(self, obj): ...
    def save_global(self, obj, name: Incomplete | None = None, pack=...): ...
    def save_function(self, obj, name: Incomplete | None = None): ...
    def save_pypy_builtin_func(self, obj) -> None: ...
