from abc import ABC, abstractmethod


class IDatabaseClient(ABC):
    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass
