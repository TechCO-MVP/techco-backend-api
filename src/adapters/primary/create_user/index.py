from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.user import UserDTO
from src.use_cases.user.create_user import create_user_use_case

logger = Logger()
app = APIGatewayRestResolver()


@app.post("/user/create")
def create_user():
    try:

        body = app.current_event.json_body
        if not body:
            raise ValueError("Request body is empty")

        user_dto = UserDTO(**body)
        response = create_user_use_case(user_dto)

        return Response(
            status_code=200,
            body=response,
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

    except Exception:
        logger.exception("An error occurred")
        return Response(
            status_code=500,
            body={"message": "An error occurred"},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for creating a user
    request: The request object, described like:
    {
        "body": {
            "business": "string",
            "business_id": "string",
            "full_name": "string",
            "email": "string"
            "company_position": "string"
            "rol": "string"
        }
    }
    """

    return app.resolve(event, context)
