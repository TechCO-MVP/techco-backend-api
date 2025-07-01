from src.adapters.secondary.documentdb.user_db_adapter import UserDocumentDBAdapter
from src.domain.user import UserEntity
from src.repositories.repository import IRepository


class UserRepository(IRepository[UserEntity]):

    _adapter: UserDocumentDBAdapter

    def __init__(self):
        super().__init__()
        self._adapter = UserDocumentDBAdapter()

    def getAll(self, params: dict):
        return self._adapter.getAll(params)

    def search(self, params: dict):
        return self._adapter.search(params)

    def getById(self, id: str):
        return self._adapter.getById(id)

    def getByEmail(self, email: str):
        return self._adapter.getByEmail(email)

    def create(self, entity):
        return self._adapter.create(entity)

    def update(self, id: str, entity):
        return self._adapter.update(id, entity)

    def delete(self, id: str):
        return self._adapter.delete(id)

    def get_admin_user_by_business_id(self, business_id: str):
        return self._adapter.get_admin_user_by_business_id(business_id)
