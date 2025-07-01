from src.adapters.secondary.documentdb.position_configuration import (
    PositionConfigurationDBAdapter,
)
from src.domain.position_configuration import PositionConfigurationEntity
from src.repositories.repository import IRepository


class PositionConfigurationRepository(IRepository[PositionConfigurationEntity]):

    _adapter: PositionConfigurationDBAdapter

    def __init__(self):
        super().__init__()
        self._adapter = PositionConfigurationDBAdapter()

    def getAll(self, filter_params: dict = None):
        return self._adapter.getAll(filter_params)

    def getById(self, id: str):
        return self._adapter.getById(id)

    def create(self, entity):
        return self._adapter.create(entity)

    def update(self, id: str, entity):
        return self._adapter.update(id, entity)

    def delete(self, id: str):
        return self._adapter.delete(id)
