from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from botocore.exceptions import ParamValidationError
from pydantic import ValidationError

from src.utils.errors import format_validation_error
from src.errors.entity_not_found import EntityNotFound
from src.use_cases.profile.start_filter_profile_url_use_case import (
    start_filter_profile_url_use_case,
)

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/profile/filter/start/url")
def start_profile_search_by_url():
    try:
        logger.info("Starting filter profile by url")
        user = app.current_event.request_context.authorizer["claims"]
        user_email = user["email"]

        body: dict = app.current_event.json_body

        if not body:
            raise ValueError("Request body is empty")

        position_id = body.get("position_id")
        if not position_id:
            raise ValueError("Position ID is required")

        business_id = body.get("business_id")
        if not business_id:
            raise ValueError("Business ID is required")

        url_profiles = body.get("url_profiles")
        if not url_profiles or not isinstance(url_profiles, list):
            raise ValueError("URL profiles is required")

        # call use case to start filter profile
        result = start_filter_profile_url_use_case(
            user_email, position_id, business_id, url_profiles
        )

        return Response(
            status_code=200,
            body={"message": "Filter profile started successfully", "body": result},
            content_type=content_types.APPLICATION_JSON,
        )
    except ParamValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )
    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=400,
            body={"message": format_validation_error(e)},
            content_type=content_types.APPLICATION_JSON,
        )
    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )
    except EntityNotFound as e:
        logger.error(str(e))
        return Response(
            status_code=404, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )
    except Exception:
        logger.exception("An error occurred")
        return Response(
            status_code=500,
            body={"message": "An error occurred"},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Lambda handler for the start filter profile endpoint
    request: {
        "body": {
            "filter": {
                "role": "developer",
                "seniority": "senior",
                "country_code": "Colombia",
                "city": "Medellin",
                "description": "....",
                "responsabilities": ["...."],
                "skills": ["python", "django", "aws"],
                "url_profiles": ["https://www.linkedin.com/in/username"]
            }
        }
    }
    """
    return app.resolve(event, context)
