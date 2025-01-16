from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.user import UpdateUserDTO
from src.use_cases.user.update_user_data import put_user_data_use_case


logger = Logger()
app = APIGatewayRestResolver()


@app.put("/user/data")
def put_user_data():
    """Update user data."""
    try:

        body = app.current_event.json_body

        if not body:
            raise ValueError("Request body is empty")

        UpdateUserDTO(**body)
        put_user_data_use_case(body)

        return Response(
            status_code=200,
            body={"message": "User data updated successfully" },
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
    Handler function for put user data
    request: The request object, described like:
    {
        "body": {
            "user_id": "string",
            "full_name": "string",
            "roles": "array"
        }
    }
    """

    return app.resolve(event, context)
