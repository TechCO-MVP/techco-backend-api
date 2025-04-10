import json
import boto3
from aws_lambda_powertools import Logger

from src.utils.send_chat_message_by_websocket import send_chat_message_by_websocket

logger = Logger()
dynamodb = boto3.client("dynamodb")

def chat_message_use_case(connection_id, payload):
    message = payload.get("message")

    response_LLM = send_request_to_llm(message)

    send_chat_message_by_websocket(
        connection_id,
        {
            "type": "chat_message",
            "message": response_LLM["message"],
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "chat sent"})
    }

def send_request_to_llm(message):
    # Simulate sending a request to an LLM and getting a response
    # In a real-world scenario, this would involve making an API call to the LLM service
    logger.info(f"Sending request to LLM with message: {message}")
    
    # Simulated response from LLM
    response = {
        "status": "success",
        "response": f"LLM response to '{message}'",
        "message": "Message processed successfully by LLM, this is mocked response"
    }

    logger.info(f"Received response from LLM: {response}")
    
    return response