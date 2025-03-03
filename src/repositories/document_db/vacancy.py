from src.adapters.secondary.documentdb.vacancy import (
    VacancyDBAdapter,
)
from src.domain.vacancy import VacancyEntity
from src.repositories.repository import IRepository


class ProfileFilterProcessRepository(IRepository[VacancyEntity]):

    _adapter: IRepository[VacancyEntity]

    def __init__(self):
        super().__init__()
        self._adapter = VacancyDBAdapter()

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
