import json
import boto3
from aws_lambda_powertools import Logger

from src.utils.send_chat_message_by_websocket import send_chat_message_by_websocket
from src.constants.index import TABLE_WEBSOCKET_CONNECTIONS, REGION_NAME, ENV, API_ID

logger = Logger()
dynamodb = boto3.client("dynamodb")

def chat_message_use_case(sender_connection_id, payload):
    message = payload.get("message")
    receiver_id = payload.get("receiver_id")

    response_LLM = send_request_to_llm(message)

    connection_id = get_receiver_connection_id(receiver_id)

    if connection_id:
        send_chat_message_by_websocket(
            receiver_id,
            connection_id,
            {
                "type": "chat_message",
                "message": response_LLM["message"],
            }
        )
    else:
        logger.info(f"No active WebSocket connection found for receiver_id: {receiver_id}")
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "No active WebSocket connection found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"status": "chat sent"})
    }

def get_receiver_connection_id(user_id):
    logger.info(f"getting connection_id from DynamoDB for user_id: {user_id}")
    response = dynamodb.query(
        TableName=TABLE_WEBSOCKET_CONNECTIONS,
        IndexName="user_id_index",
        KeyConditionExpression="user_id = :user_id",
        ExpressionAttributeValues={":user_id": {"S": user_id}},
    )
    logger.info(f"DynamoDB Query response: {response}")

    if not response["Items"]:
        return None

    connection_id = response["Items"][0]["connection_id"]["S"]
    logger.info(f"Found connection_id: {connection_id} for user_id: {user_id}")

    return connection_id

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