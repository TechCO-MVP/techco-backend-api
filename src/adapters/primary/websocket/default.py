import json
from aws_lambda_powertools import Logger
from src.use_cases.websocket.chat_message import chat_message_use_case
# from src.use_cases.websocket.unknow_action import unknown_action_use_case
# from src.handlers.notification_handler import handle_notification

logger = Logger()

@logger.inject_lambda_context
def handler(event, context):
    try:
        print("event", event)
        body = json.loads(event.get("body", "{}"))
        action = body.get("action")
        payload = body.get("payload", {})
        connection_id = event["requestContext"]["connectionId"]

        logger.info(f"Received action: {action}, payload: {payload}")

        if action == "chat_message":
            return chat_message_use_case(connection_id, payload)
        # else:
        #     return unknown_action_use_case(connection_id, action)

    except Exception as e:
        logger.error(f"Error in @message handler: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"})
        }
