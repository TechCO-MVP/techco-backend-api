import json

from aws_lambda_powertools import Logger

from src.use_cases.websocket.chat_message_public import chat_message_public_use_case

logger = Logger()


@logger.inject_lambda_context
def handler(event, context):
    try:
        logger.info("event", event)
        body = json.loads(event.get("body", "{}"))
        action = body.get("action")
        payload = body.get("payload", {})
        connection_id = event["requestContext"]["connectionId"]
        
        logger.info(f"Received action: {action}, payload: {payload}")
        
        if action == "chat_message_public":
            return chat_message_public_use_case(connection_id, payload)
        else:
            return json.dumps(
                {
                    "action": "Unknown action",
                    "payload": {"message": "Unknown action"},
                }
            )

    except Exception as e:
        logger.error(f"Error in @message handler: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": "Internal server error"})}
