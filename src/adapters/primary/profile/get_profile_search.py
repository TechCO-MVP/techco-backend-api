from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.profile import PROCESS_TYPE
from src.errors.entity_not_found import EntityNotFound
from src.use_cases.profile.get_profile_filter_use_case import get_profile_filter_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.get("/profile/filter")
def get_profile_filter():
    """
    Retrieve a profile filter process by position id
    {
        "position_id": "xxx"
    }
    """
    try:
        # call use case to get profile filter process by position id
        position_id = app.current_event.query_string_parameters.get("position_id")
        if not position_id:
            raise ValueError("Position ID is required")

        profile_filter_process_entities = get_profile_filter_use_case(
            position_id, PROCESS_TYPE.PROFILES_SEARCH
        )

        return Response(
            status_code=200,
            body={
                "message": "Profile filter process retrieved successfully",
                "body": profile_filter_process_entities[0].to_dto(flat=True),
            },
            content_type=content_types.APPLICATION_JSON,
        )
    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
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


def lambda_handler(event, context: LambdaContext) -> dict:
    """
    Lambda handler to get a profile filter process by position id
    {
        "position_id": "xxx"
    }
    """
    return app.resolve(event, context)
