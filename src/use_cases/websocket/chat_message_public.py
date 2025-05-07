import json

import boto3
from aws_lambda_powertools import Logger

from src.domain.position_configuration import ChatPositionConfigurationPayload
from src.utils.send_chat_message_by_websocket import send_chat_message_by_websocket

logger = Logger()
dynamodb = boto3.client("dynamodb")

def chat_message_public_use_case(connection_id, payload, user_email):
    logger.info(f"Chat message use case started with payload: {payload}")
    ChatPositionConfigurationPayload(**payload)

    response_LLM = send_request_to_llm(payload, user_email)

    send_chat_message_by_websocket(
        connection_id,
        {
            "type": "chat_message",
            "payload": response_LLM,
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "chat sent"})
    }

def send_request_to_llm(payload: dict) -> dict:
    payload["message"] = "this a mocked response from a publi chat"
        
    return payload