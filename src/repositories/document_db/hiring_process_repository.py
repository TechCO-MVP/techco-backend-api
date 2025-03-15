from src.adapters.secondary.documentdb.hiring_process_adapter import HiringProcessDBAdapter
from src.domain.hiring_process import HiringProcessEntity
from src.repositories.repository import IRepository


class HiringProcessRepository(IRepository[HiringProcessEntity]):

    _adapter: HiringProcessDBAdapter

    def __init__(self):
        super().__init__()
        self._adapter = HiringProcessDBAdapter()

    def getAll(self, params: dict):
        return self._adapter.getAll(params)

    def getById(self, id: str):
        return self._adapter.getById(id)

    def getByCardId(self, card_id: str):
        return self._adapter.getByCardId(card_id)

    def getByEmail(self, email: str):
        return self._adapter.getByEmail(email)

    def create(self, entity):
        return self._adapter.create(entity)

    def update(self, id: str, entity):
        return self._adapter.update(id, entity)

    def delete(self, id: str):
        return self._adapter.delete(id)

    def getByPositionId(self, params: dict):
        return self._adapter.getByPositionId(params)

    def getByLinkedinNumId(self, params: dict):
        return self._adapter.getByLinkedinNumId(params)
