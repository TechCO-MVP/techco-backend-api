from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.base_entity import from_dto_to_entity
from src.domain.profile import ProfileFilterProcessEntity
from use_cases.profile.send_profile_url_query_use_case import send_profile_url_query_use_case

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context: LambdaContext) -> dict:
    """
    Lambda handler to send reuqest to scraping profile filter process
    {
        "_id": "67aa9fe5e45a8924426e2ffa",
        "created_at": "2025-02-11T00:55:01.488274",
        "updated_at": "2025-02-11T00:55:01.488284",
        "deleted_at": null,
        "status": "in_progress",
        "execution_arn": "...",
        "user_id": "6791f6f8886eb975df789f6a",
        "position_id": "yyy",
        "business_id": "xxx",
        "process_filters": {
            "role": "Software Engineer",
            "seniority": "Senior",
            "country_code": "USA",
            "city": "San Francisco",
            "description": "...",
            "responsabilities": [...],
            "skills": [...],
            "business_id": "xxx",
            "position_id": "yyy",
            "snapshot_id": "",
            "url_profiles": [...],
        }
    }
    """
    logger.info("Starting filter profile by url")

    try:
        profile_filter_process = from_dto_to_entity(
            ProfileFilterProcessEntity,
            event,
        )

        snapshot_id = send_profile_url_query_use_case(
            profile_filter_process,
        )

        logger.info(f"Snapshot id: {snapshot_id}")
        profile_filter_process.props.process_filters.snapshot_id = snapshot_id
        return profile_filter_process.to_dto(flat=True)
    except Exception as e:
        logger.error(f"Error creating pipe configuration for open position: {e}")
        raise
