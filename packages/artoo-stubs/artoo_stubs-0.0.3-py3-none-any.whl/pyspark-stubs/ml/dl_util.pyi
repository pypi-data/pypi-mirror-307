from typing import Any, Callable

from pyspark import cloudpickle as cloudpickle

class FunctionPickler:
    @staticmethod
    def pickle_fn_and_save(fn: Callable, file_path: str, save_dir: str, *args: Any, **kwargs: Any) -> str: ...
    @staticmethod
    def create_fn_run_script(pickled_fn_path: str, fn_output_path: str, script_path: str, prefix_code: str = '', suffix_code: str = '') -> str: ...
    @staticmethod
    def get_fn_output(fn_output_path: str) -> Any: ...
