from src.adapters.secondary.scraping.brigthdata_adapter import ScrapingProfileFilterProcessAdapter
from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.repository import IRepository


class ScrapingProfileFilterProcessRepository(IRepository[ProfileFilterProcessEntity]):

    _adapter: ScrapingProfileFilterProcessAdapter

    def __init__(self):
        super().__init__()
        self._adapter = ScrapingProfileFilterProcessAdapter()

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

    def get_status(self, entity):
        return self._adapter.get_status(entity)

    def get_data(self, entity):
        return self._adapter.get_data(entity)
