from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.position_configuration import PositionConfigurationDTO
from src.use_cases.position_configuration.post_position_configuration import post_position_configuration_use_case
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/position_configuration/create")
def post_position_configuration():
    """Post position configuration."""
    try:
        authorizer = app.current_event.request_context.authorizer["claims"]
        user_email = authorizer["email"]

        user_entity = get_user_by_mail_use_case(user_email)
        if not user_entity:
            raise ValueError("User not found")
        
        body = app.current_event.json_body
        body["user_id"] = user_entity.id

        update_status_dto = PositionConfigurationDTO(**body)
        
        response = post_position_configuration_use_case(update_status_dto)

        return Response(
            status_code=200,
            body={
                "message": "Position configuration created successfully",
                "body": {
                    "data": response.to_dto(flat=True),
                },
            },
            content_type=content_types.APPLICATION_JSON,
        )

    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=422, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except ValueError as e:
        logger.error(str(e))
        return Response(
            status_code=400, body={"message": str(e)}, content_type=content_types.APPLICATION_JSON
        )

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=500,
            body={"message": "An error occurred: %s" % e},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for put position status
    request: The request object, described like:
    {
        "body": {
            "thread_id": string,
            "status": string,
            "phases": [
                {
                    "name": string,
                    "thread_id": string,
                    "status": string,
                    "data": dict
                    "type": string
                }
            ],
            "type": string,
        }
    }
    """

    return app.resolve(event, context)
