import json
from aws_lambda_powertools import Logger
from src.use_cases.websocket.chat_message import chat_message_use_case

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):
    try:
        logger.info("event", event)
        body = json.loads(event.get("body", "{}"))
        action = body.get("action")
        payload = body.get("payload", {})
        connection_id = event["requestContext"]["connectionId"]
        user_id = event["requestContext"]["authorizer"]["user_id"]
        user_email = event["requestContext"]["authorizer"]["email"]

        logger.info(f"Received action: {action}, payload: {payload}")
        logger.info(f"message from user_id: {user_id}, email: {user_email}")

        if action == "chat_message":
            return chat_message_use_case(connection_id, payload, user_email)
        else:
            return json.dumps(
                {
                    "action": "Unknown action",
                    "payload": {
                        "message": "Unknown action"
                    },
                }
            )

    except Exception as e:
        logger.error(f"Error in @message handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
