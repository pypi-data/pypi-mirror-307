from typing import Callable
from uuid import UUID

class ModelCache:
    @staticmethod
    def add(uuid: UUID, predict_fn: Callable) -> None: ...
    @staticmethod
    def get(uuid: UUID) -> Callable | None: ...
