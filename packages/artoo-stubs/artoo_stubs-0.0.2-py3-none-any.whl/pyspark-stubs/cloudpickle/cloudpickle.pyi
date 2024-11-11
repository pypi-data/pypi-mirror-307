from types import CellType as CellType

from _typeshed import Incomplete

from .compat import pickle as pickle

DEFAULT_PROTOCOL: Incomplete
PYPY: Incomplete
builtin_code_type: Incomplete

def register_pickle_by_value(module) -> None: ...
def unregister_pickle_by_value(module) -> None: ...
def list_registry_pickle_by_value(): ...
def cell_set(cell, value) -> None: ...

STORE_GLOBAL: Incomplete
DELETE_GLOBAL: Incomplete
LOAD_GLOBAL: Incomplete
GLOBAL_OPS: Incomplete
HAVE_ARGUMENT: Incomplete
EXTENDED_ARG: Incomplete

def parametrized_type_hint_getinitargs(obj): ...
def is_tornado_coroutine(func): ...
load = pickle.load
loads = pickle.loads

def subimport(name): ...
def dynamic_subimport(name, vars): ...
def instance(cls): ...

class _empty_cell_value:
    @classmethod
    def __reduce__(cls): ...
