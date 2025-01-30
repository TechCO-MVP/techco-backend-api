from src.adapters.secondary.documentdb.profile_filter_process_db_adapter import (
    ProfileFilterProcessDocumentDBAdapter,
)
from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.repository import IRepository


class ProfileFilterProcessRepository(IRepository[ProfileFilterProcessEntity]):

    _adapter: IRepository[ProfileFilterProcessEntity]

    def __init__(self):
        super().__init__()
        self._adapter = ProfileFilterProcessDocumentDBAdapter()

    def getAll(self, filter_params: dict = None):
        return self._adapter.getAll(filter_params)

    def getById(self, id: int):
        return self._adapter.getById(id)

    def create(self, entity):
        return self._adapter.create(entity)

    def update(self, id: str, entity):
        return self._adapter.update(id, entity)

    def delete(self, id: str):
        return self._adapter.delete(id)
