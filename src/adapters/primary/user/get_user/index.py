from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.role import Role
from src.domain.user import GetUserQueryParams
from src.use_cases.user.get_user import get_user_use_case
from src.utils.authorization import role_required

logger = Logger()
app = APIGatewayRestResolver()


@app.get("/user/list")
@role_required(app, [Role.SUPER_ADMIN, Role.BUSINESS_ADMIN])
def get_user():
    """Get user."""
    try:

        query_params = app.current_event.query_string_parameters
        GetUserQueryParams.validate_params(query_params)
        response = get_user_use_case(query_params)

        if isinstance(response, list):
            data = [user.to_dto(flat=True) for user in response]
        else:
            data = [response.to_dto(flat=True)]

        message = "User found successfully" if data else "User not found"

        return Response(
            status_code=200,
            body={
                "message": message,
                "body": {
                    "data": data,
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
    Handler function for get user
    request: The request object, described like:
    {
        "queryStringParameters": {
            "id": "string",
            "all": "boolean"
        }
    }
    """

    return app.resolve(event, context)
