from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.use_cases.notification.get_notification import get_notification_use_case
from src.use_cases.user.get_user_by_mail import get_user_by_mail_use_case


logger = Logger()
app = APIGatewayRestResolver()


@app.get("/notification/list")
def get_notification():
    """Get Notification."""
    try:

        authorizer = app.current_event.request_context.authorizer

        user = authorizer["claims"]

        user_entity = get_user_by_mail_use_case(user["email"])
        response = get_notification_use_case(user_entity)

        
        message = "Notification found successfully" if response else "notifications not found"

        return Response(
            status_code=200,
            body={
                "message": message,
                "body": {
                    "data": response,
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
    Handler function for get user notification
    request: The request is not required, mail is in requestContext post auth cognito

    """

    return app.resolve(event, context)
