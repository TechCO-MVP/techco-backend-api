import json
import requests
import time
import os

from aws_lambda_powertools import Logger

from src.adapters.secondary.scraping.constants import (
    TRADUCTION_FILTERS_BRIGHTDATA,
    RECORDS_LIMIT,
    BASE_URL_BRIGHTDATA,
)
from src.domain.base_entity import from_dto_to_entity
from src.domain.profile import ProfileFilterProcessEntity
from src.repositories.repository import IRepository
from src.utils.secrets import get_secret_by_name

logger = Logger("ProfileFilterProcessDocumentDBAdapter")
TOKEN_BRIGHTDATA = get_secret_by_name(os.getenv("TOKEN_SERVICE_BRIGHTDATA"))


class ScrapingProfileFilterProcessAdapter(IRepository[ProfileFilterProcessEntity]):

    def __init__(self):
        super().__init__()

    def getAll(self, filter_params: dict = None):
        logger.info(f"Getting all profile filter process entities with filter: {filter_params}")

        return [ProfileFilterProcessEntity]

    def getById(self, id: str) -> ProfileFilterProcessEntity | None:
        logger.info(f"Getting profile filter process status from brigthdata - snapshoot_id: {id}")

        return None  # from_dto_to_entity(ProfileFilterProcessEntity, result)

    def create(self, entity):
        logger.info("post scraping profile filter process data")
        entity_dto = entity.to_dto(flat=True)
        filters = entity_dto["process_filters"]
        logger.info(f"Entity: {filters}")

        base_filters = [
            {
                "name": TRADUCTION_FILTERS_BRIGHTDATA[key]["name"],
                "operator": TRADUCTION_FILTERS_BRIGHTDATA[key]["operator"],
                "value": value,
            }
            for key, value in filters.items()
            if key in TRADUCTION_FILTERS_BRIGHTDATA and value is not None and key != "skills"
        ]

        fake_filter = {"name": "country_code", "operator": "=", "value": filters["country_code"]}

        nested_filters = [
            {
                "operator": "or",
                "filters": [
                    {"name": item, "operator": "includes", "value": k["value"]}
                    for item in k["name"]
                ],
            }
            for k in base_filters
            if isinstance(k["name"], list)
        ]

        flat_filters = [
            {"name": k["name"], "operator": k["operator"], "value": k["value"]}
            for k in base_filters
            if not isinstance(k["name"], list)
        ]

        skills_filters = []
        for skill in filters.get("skills", []):
            skill_filter = {
                "operator": "or",
                "filters": [
                    {"name": item, "operator": "includes", "value": skill["name"]}
                    for item in TRADUCTION_FILTERS_BRIGHTDATA["skills"]["name"]
                ],
            }
            if not skill["required"]:
                skill_filter["filters"].append(fake_filter)
            skills_filters.append(skill_filter)

        payload = {
            "dataset_id": "gd_l1viktl72bvl7bjuj0",
            "filter": {
                "operator": "and",
                "filters": flat_filters + nested_filters + skills_filters,
            },
            "records_limit": RECORDS_LIMIT,
        }

        headers = {
            "Authorization": f"Bearer {TOKEN_BRIGHTDATA}",
            "Content-Type": "application/json",
        }

        logger.info(f"payload to brightdata: {payload}")

        response = requests.request(
            "POST", f"{BASE_URL_BRIGHTDATA}/filter", json=payload, headers=headers, timeout=310
        )

        logger.info(f"response brightdata: {response}")

        if response.status_code == 200:
            snapshot_id = response.json()["snapshot_id"]
            entity_dto["process_filters"]["snapshot_id"] = snapshot_id
            entity = from_dto_to_entity(ProfileFilterProcessEntity, entity_dto)
        else:
            error = {
                "message": (
                    f"Failed to create profile filter process: {response.status_code} - "
                    f"{response.text}"
                ),
                "event": entity_dto,
                "process_id": entity_dto.get("_id"),
            }
            logger.error(error["message"])
            raise Exception(error)

        logger.info(f"Entity: {entity}")
        return entity

    def update(self, id: str, entity):
        logger.info("Updating profile filter process entity")
        logger.info(f"Entity: {entity.to_dto(flat=True)}")

        return entity

    def delete(self, id: str):
        return True

    def get_status(self, id: str) -> bool:
        logger.info(f"Getting profile filter process status from brigthdata - snapshoot_id: {id}")

        headers = {"Authorization": f"Bearer {TOKEN_BRIGHTDATA}"}
        response = requests.request(
            "GET", f"{BASE_URL_BRIGHTDATA}/snapshots/{id}", headers=headers, timeout=5
        )

        logger.info(f"response brightdata: {response}")

        if response.status_code == 200 and response.json()["status"] == "ready":
            return True
        else:
            error = {
                "message": (
                    f"Failed to get status snapshoot: {response.status_code} - " f"{response.text}"
                ),
                "snapshoot_id": id,
            }
            logger.error(error["message"])
            raise Exception(error)

    def get_data(self, id: str):
        logger.info(f"Getting profile filter process data from brigthdata - snapshoot_id: {id}")

        params = {"format": "json"}
        headers = {"Authorization": f"Bearer {TOKEN_BRIGHTDATA}"}

        response = requests.request(
            "GET",
            f"{BASE_URL_BRIGHTDATA}/snapshots/{id}/download",
            headers=headers,
            params=params,
            timeout=310,
        )

        logger.info(f"response brightdata: {response}")

        if response.status_code == 200:
            return json.loads(response.text)
        elif response.status_code == 202:
            time.sleep(30)

            response_second_request = requests.request(
                "GET",
                f"{BASE_URL_BRIGHTDATA}/snapshots/{id}/download",
                headers=headers,
                params=params,
                timeout=310,
            )

            logger.info(f"response brightdata second request: {response}")
            if response_second_request.status_code == 200:
                return json.loads(response_second_request.text)
        else:
            final_response = response if response.status_code != 202 else response_second_request
            error = {
                "message": (
                    f"Failed to daowload snapshoot_id: {final_response.status_code} - "
                    f"{final_response.text}"
                ),
                "snapshoot_id": id,
            }
            logger.error(error["message"])
            raise Exception(error)
