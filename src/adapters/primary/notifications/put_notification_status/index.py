from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.notification import UpdateNotificationStatusDTO
from src.use_cases.notification.update_notification_status import put_notificationr_status_use_case


logger = Logger()
app = APIGatewayRestResolver()


@app.put("/notification/status")
def put_notification_status():
    """Update notification status."""
    try:

        body = app.current_event.json_body

        if not body:
            raise ValueError("Request body is empty")

        notification_dto = UpdateNotificationStatusDTO(**body)

        put_notificationr_status_use_case(notification_dto)

        message = "Notification status updated successfully"

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
    Handler function for up´date notification status
    request: The request object, described like:
    {
        "body": {
            "notification_id": "string"
        },
    }
    """

    return app.resolve(event, context)
