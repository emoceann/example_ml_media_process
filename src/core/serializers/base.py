from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class BaseSerializer[T: Any, V: BaseModel](ABC):
    @abstractmethod
    def serialize(self, data: T) -> V:
        raise NotImplementedError
