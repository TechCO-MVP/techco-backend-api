from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class IRepository(ABC, Generic[T]):

    @abstractmethod
    def getAll(self, filter_params: dict = {}) -> List[T]:
        pass

    @abstractmethod
    def getById(self, id: str) -> T | None:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def update(self, id: str, entity: T) -> T | None:
        pass

    @abstractmethod
    def delete(self, id: str) -> bool:
        pass
