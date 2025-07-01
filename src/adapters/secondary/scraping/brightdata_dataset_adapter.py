import requests
import json
import time

from typing import List
from aws_lambda_powertools import Logger


logger = Logger("BrightDataDatasetAdapter")


class BrightDatasetAdapter:
    """
    Adapter for BrightData dataset scraping.
    """

    def __init__(
        self,
        base_url: str,
        api_key: str,
        dataset_id: str,
    ):
        self.base_url = base_url
        self.api_key = api_key
        self.dataset_id = dataset_id

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def search_by_url(self, urls: List[str]) -> str:
        """
        Queires the brighdata API to get the profile filter process data by url
        and returns the snapshot id.
        """
        logger.info(f"Searching profile filter process by url: {urls}")

        payload = [{"url": url} for url in urls]
        params = {"dataset_id": self.dataset_id}

        response = requests.post(
            f"{self.base_url}/v3/trigger",
            json=payload,
            headers=self.headers,
            params=params,
        )

        logger.info(f"response brightdata: {response}")

        if response.status_code != 200:
            raise Exception(
                f"Failed to create profile filter process: {response.status_code} - "
                f"{response.text}"
            )

        data = response.json()
        if "snapshot_id" not in data:
            raise Exception(
                f"Failed to create profile filter process: {response.status_code} - "
                f"{response.text}"
            )

        return data["snapshot_id"]

    def get_snapshot_status(self, snapshot_id: str) -> dict:
        """
        Get the status of the snapshot.
        """
        logger.info(f"Getting snapshot status: {snapshot_id}")

        response = requests.get(
            f"{self.base_url}/v3/progress/{snapshot_id}",
            headers=self.headers,
        )

        logger.info(f"response brightdata: {response}")

        if response.status_code != 200:
            raise Exception(
                f"Failed to get snapshot status: {response.status_code} - " f"{response.text}"
            )

        return response.json()

    def get_snapshot_data(self, snapshot_id: str) -> List[dict]:
        """
        Get the data of the snapshot.
        """
        logger.info(f"Getting snapshot data: {snapshot_id}")

        params = {"format": "json"}
        response = requests.get(
            f"{self.base_url}/v3/snapshot/{snapshot_id}",
            headers=self.headers,
            params=params,
            timeout=310,
        )

        logger.info(f"response brightdata: {response}")

        if response.status_code == 200:
            return json.loads(response.text)

        if response.status_code == 202:
            time.sleep(60)

            response = requests.get(
                f"{self.base_url}/v3/snapshot/{snapshot_id}",
                headers=self.headers,
                params=params,
                timeout=310,
            )

            logger.info(f"response brightdata second request: {response}")
            if response.status_code == 200:
                return json.loads(response.text)

        raise Exception(
            f"Failed to get snapshot data: {response.status_code} - " f"{response.text}"
        )
