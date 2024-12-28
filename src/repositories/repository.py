from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List

T = TypeVar("T")


class IRepository(ABC, Generic[T]):

    @abstractmethod
    def getAll(self) -> List[T]:
        pass

    @abstractmethod
    def getById(self, id: int) -> T | None:
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
