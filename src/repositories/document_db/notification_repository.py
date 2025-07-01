from src.adapters.secondary.documentdb.notification_db_adapter import NotificationDocumentDBAdapter
from src.domain.notification import NotificationEntity
from src.repositories.repository import IRepository


class NotificationRepository(IRepository[NotificationEntity]):

    _adapter: NotificationDocumentDBAdapter

    def __init__(self):
        super().__init__()
        self._adapter = NotificationDocumentDBAdapter()

    def getAll(self, params: dict):
        return self._adapter.getAll(params)

    def getById(self, id: str):
        return self._adapter.getById(id)

    def create(self, entity):
        return self._adapter.create(entity)

    def update(self, id: str, entity):
        return self._adapter.update(id, entity)

    def delete(self, id: str):
        return self._adapter.delete(id)
