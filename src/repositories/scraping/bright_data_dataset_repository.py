from src.adapters.secondary.scraping.brightdata_dataset_adapter import BrightDatasetAdapter
from src.adapters.secondary.scraping.constants import BASE_URL_BRIGHTDATA, BRIGHT_DATA_DATASET_ID
from src.utils.secrets import get_secret_by_name
from src.constants.index import TOKEN_SERVICE_BRIGHTDATA_SECRET_NAME


class BrightDataDatasetRepository:

    _adapter: BrightDatasetAdapter

    def __init__(self):
        super().__init__()

        api_key = get_secret_by_name(TOKEN_SERVICE_BRIGHTDATA_SECRET_NAME)

        self._adapter = BrightDatasetAdapter(
            base_url=BASE_URL_BRIGHTDATA,
            api_key=api_key,
            dataset_id=BRIGHT_DATA_DATASET_ID,
        )

    def search_by_url(self, urls: list[str]):
        return self._adapter.search_by_url(urls)

    def get_snapshot_status(self, snapshot_id: str):
        return self._adapter.get_snapshot_status(snapshot_id)

    def get_snapshot_data(self, snapshot_id: str):
        return self._adapter.get_snapshot_data(snapshot_id)
