from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.profile import ProfileFilterProcessQueryDTO
from src.use_cases.profile.validate_status_profile_query import validate_status_profile_query_use_case

logger = Logger()


@logger.inject_lambda_context
def lambda_handler(event, context: LambdaContext) -> dict:
    """
    Lambda handler to validate status of scraping
    {
        "user_id": "123",
        "position_id": "123",
        "_id": "123",
        "business_id": "123",
        "role": "Software Engineer",
        "seniority": "Senior",
        "country": "USA",
        "city": "San Francisco",
        "description": "Experienced software engineer with expertise in Python and cloud technologies.",
        "responsabilities": [
            "Design and develop scalable and maintainable software solutions.",
            "Collaborate with cross-functional teams to deliver high-quality products.",
            "Participate in code reviews and provide constructive feedback."
        ],
        "skills": [
            "Python",
            "AWS",
            "Docker",
            "Kubernetes",
            "Agile Methodologies"
        ]
        "snapshot_id": "123"
    }
    """
    logger.info("Querying brightdata")
    logger.info(event)
    logger.info(context)

    profile_process_dto = ProfileFilterProcessQueryDTO(**event)
    status = validate_status_profile_query_use_case(profile_process_dto)

    if status:
        return event
    else:
        raise Exception("Error")
