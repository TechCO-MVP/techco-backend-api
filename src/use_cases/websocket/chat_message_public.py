import json

import boto3
from aws_lambda_powertools import Logger

from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.constants.position.configuration import assistant_phase_mapping
from src.domain.hiring_process import HiringProcessEntity
from src.domain.position import PositionEntity
from src.domain.position_configuration import ChatPositionConfigurationPayload
from src.use_cases.hiring_process.get_hiring_process import get_hiring_process_use_case
from src.use_cases.position.get_position_entity import get_position_entity_use_case
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
    hiring_process_entity: HiringProcessEntity = get_hiring_process_use_case({"hiring_process_id": payload["hiring_process_id"]})
    assistand_name = assistant_phase_mapping.get(payload["phase_type"])

    if not assistand_name:
        raise ValueError(f"Assistant not found for phase type: {payload['phase_type']}")

    position_entity: PositionEntity = get_position_entity_use_case({"id": hiring_process_entity.props.position_id})
    context = {"position_id": position_entity.id}
    open_ai_adapter = OpenAIAdapter(context)
    open_ai_adapter.assistant_id = position_entity.props.assistants[assistand_name].assistant_id

    logger.info(f"Sending request to LLM with message: {payload['message']}")

    thread_run = open_ai_adapter.create_message_thread(payload["thread_id"], payload["message"])

    response = open_ai_adapter.run_and_process_thread(thread_run)
    response = json.loads(response)
    payload.update(response)
    logger.info("Assistant:")
    logger.info(f"Received response from LLM: {response}")
        
    return payload