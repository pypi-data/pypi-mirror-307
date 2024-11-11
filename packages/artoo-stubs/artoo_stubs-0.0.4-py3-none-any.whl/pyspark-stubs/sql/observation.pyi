from typing import Any

__all__ = ['Observation']

class Observation:
    def __init__(self, name: str | None = None) -> None: ...
    @property
    def get(self) -> dict[str, Any]: ...
