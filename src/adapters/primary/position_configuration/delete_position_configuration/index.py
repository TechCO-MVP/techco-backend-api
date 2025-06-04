from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from http import HTTPStatus
from pydantic import ValidationError

from src.use_cases.position_configuration.delete_position_configuration import (
    delete_position_configuration_use_case,
)
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.delete("/position_configuration/<position_configuration_id>")
def delete_position_configuration(position_configuration_id: str):
    """Delete position configuration."""
    try:
        authorizer = app.current_event.request_context.authorizer["claims"]
        user_email = authorizer["email"]
        user_entity = get_user_by_mail_use_case(user_email)

        if not user_entity:
            raise ValueError("User not found")

        delete_position_configuration_use_case(position_configuration_id, user_entity)

        return Response(
            status_code=HTTPStatus.OK.value,
            body={
                "message": "Position configuration deleted successfully",
                "body": {
                    "data": None,
                },
            },
            content_type=content_types.APPLICATION_JSON,
        )

    except ValidationError as e:
        logger.error(str(e))
        return Response(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY.value,
            body={"message": str(e)},
            content_type=content_types.APPLICATION_JSON
        )

    except ValueError as e:
        logger.error(str(e))
        match str(e):
            case "Position configuration not found":
                status_code = HTTPStatus.NOT_FOUND.value
            case "Position is active, cannot delete position configuration":
                status_code = HTTPStatus.CONFLICT.value
            case "User does not have permission to delete this position configuration":
                status_code = HTTPStatus.UNAUTHORIZED.value
        return Response(
            status_code=status_code,
            body={"message": str(e)},
            content_type=content_types.APPLICATION_JSON
        )

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
            body={"message": "An error occurred: %s" % e},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for delete position configuration
    request: The request object, described like:
    path_params:
        id: string
    """

    return app.resolve(event, context)
