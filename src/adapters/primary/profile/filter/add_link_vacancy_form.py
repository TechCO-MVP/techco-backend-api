import json
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.domain.base_entity import from_dto_to_entity
from src.domain.profile import ProfileFilterProcessEntity
from src.use_cases.profile.add_unique_link_vacancy_form import add_unique_link_vacancy_form

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
        "execution_arn": null,
        "user_id": "6791f6f8886eb975df789f6a",
        "position_id": "yyy",
        "business_id": "xxx",
        "process_filters": {
            "role": "developer",
            "seniority": "Senior",
            "country_code": "CO",
            "city": "ogot",
            "description": "Experienced software engineer with expertise in Python.",
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
            "snapshot_id": "snap_m7cl5a21218si2ws8o"
        },
        "profiles": [
            {
                "id": "1",
                "name": "John Doe",
                "email": "
                "linkedin": "https://www.linkedin.com/in/johndoe",
            },
            {
                "id": "2",
                "name": "Jane Doe",
                "email": "
                "linkedin": "https://www.linkedin.com/in/janedoe",
            }
        ]
        }
    """
    logger.info("add unique link for each profile")
    logger.info(event)
    logger.info(context)
    try:
        if isinstance(event, str):
            event = json.loads(event)

        profile_process_entity = from_dto_to_entity(ProfileFilterProcessEntity, event)
        event_links = add_unique_link_vacancy_form(profile_process_entity)

        return event_links
    except Exception as e:
        logger.exception(e)
        return {"status": "Error", "errorInfo": e}
