
import json
import os

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.base_entity import from_dto_to_entity
from src.domain.profile import ProfileFilterProcessEntity
from src.utils.send_event_SQS import send_event_SQS

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context: LambdaContext) -> None:
    """
    Lambda handler to send error to SQS
    {
        "_id": "67aa9fe5e45a8924426e2ffa",
        "error": "Error in profile process",
        "created_at": "2025-02-11T00:55:01.488274",
        "updated_at": "2025-02-11T00:55:01.488284",
        "deleted_at": null,
        "status": "in_progress",
        "execution_arn": null,
        "user_id": "6791f6f8886eb975df789f6a",
        "position_id": "yyy",
        "business_id": "xxx",
        "process_filters": {
            "role": "Software Engineer",
            "seniority": "Senior",
            "country_code": "USA",
            "city": "San Francisco",
            "description": "Experienced software engineer with expertise in Python and cloud technologies.",
            "responsabilities": [
            "Design and develop scalable and maintainable software solutions.",
            "Collaborate with cross-functional teams to deliver high-quality products.",
            "Participate in code reviews and provide constructive feedback."
            ],
            "skills": [
            {
                "name": "Python",
                "required": true
            },
            {
                "name": "AWS",
                "required": true
            },
            {
                "name": "Docker",
                "required": true
            },
            {
                "name": "Kubernetes",
                "required": false
            },
            {
                "name": "Agile Methodologies",
                "required": false
            }
            ],
            "business_id": "xxx",
            "position_id": "yyy",
            "snapshot_id": ""
        }
    }
    """
    logger.info("Error in profile process")
    logger.info(event)
    logger.info(context)

    if isinstance(event, str):
        event = json.loads(event)

    from_dto_to_entity(ProfileFilterProcessEntity, json.loads(event))
    event["origin_process"] = "profile_filter_process"
    
    send_event_SQS(event, os.getenv("SQS_USER_NOTIFICATIONS_NAME", ""), "profile_filter_process")
    
    return
