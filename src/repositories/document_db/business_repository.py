from src.adapters.secondary.documentdb.business_db_adapter import BusinessDocumentDBAdapter
from src.domain.business import BusinessEntity
from src.repositories.repository import IRepository


class BusinessRepository(IRepository[BusinessEntity]):

    _adapter: IRepository[BusinessEntity]

    def __init__(self):
        super().__init__()
        self._adapter = BusinessDocumentDBAdapter()

    def getAll(self):
        return self._adapter.getAll()

    def getById(self, id: int):
        return self._adapter.getById(id)

    def create(self, entity):
        return self._adapter.create(entity)

    def update(self, id: str, entity):
        return self._adapter.update(id, entity)

    def delete(self, id: str):
        return self._adapter.delete(id)
