from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.role import Role
from src.domain.user import UpdateUserStatusDTO
from src.use_cases.user.update_user_status import put_user_status_use_case
from src.utils.authorization import role_required


logger = Logger()
app = APIGatewayRestResolver()


@app.put("/user/status")
# @role_required(app, [Role.SUPER_ADMIN, Role.BUSINESS_ADMIN])
def put_user_status():
    """Update user status."""
    try:

        body = app.current_event.json_body
        if not body:
            raise ValueError("Request body is empty")

        user_dto = UpdateUserStatusDTO(**body)

        put_user_status_use_case(user_dto)

        message = "User status updated successfully" 
        if body["user_status"] == "disabled":
            message = "User disabled successfully"
            
        return Response(
            status_code=200,
            body={"message": message},
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
    Handler function for get user
    request: The request object, described like:
    {
        "body": {
            "user_id": "string",
            "status": "string",
            "user_email": "string"
        }
    }
    """

    return app.resolve(event, context)
