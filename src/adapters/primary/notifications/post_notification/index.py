from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from src.domain.notification import NotificationDTO
from src.utils.send_message_by_websocket import send_message_by_websocket


logger = Logger()
app = APIGatewayRestResolver()


@app.post("/notification/create")
def post_notification():
    """Post notification."""
    try:

        body = app.current_event.json_body

        if not body:
            raise ValueError("Request body is empty")
        

        notification_data = body.copy()
        for user in body.get("user_id", []):
            notification_data["user_id"] = user     
            notification_dto = NotificationDTO(**notification_data)
            
            send_message_by_websocket(notification_dto)

        message = "Notification created successfully"

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
            "user_id": str,
            "business_id": str,
            "message": str,
            "notification_type": str,
            "hiring_process_id": str,
            "phase_id": str,
        },
    }
    """

    return app.resolve(event, context)
