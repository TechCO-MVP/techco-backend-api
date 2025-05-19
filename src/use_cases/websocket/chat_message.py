import json

import boto3
from aws_lambda_powertools import Logger

from src.adapters.secondary.llm.open_ai_adapter import OpenAIAdapter
from src.domain.business import BusinessEntity
from src.domain.position_configuration import ChatPositionConfigurationPayload
from src.use_cases.business.get_business_by_id import get_business_by_id_use_case
from src.constants.position.configuration import assistant_phase_mapping
from src.utils.send_chat_message_by_websocket import send_chat_message_by_websocket
from src.constants.position.configuration import get_assistant_for_phase

logger = Logger()
dynamodb = boto3.client("dynamodb")


def chat_message_use_case(connection_id, payload, user_email):
    logger.info(f"Chat message use case started with payload: {payload}")
    ChatPositionConfigurationPayload(**payload)

    response_LLM = send_request_to_llm(payload, user_email)

    send_chat_message_by_websocket(
        connection_id,
        {
            "type": "chat_message",
            "payload": response_LLM,
        },
    )

    return {"statusCode": 200, "body": json.dumps({"status": "chat sent"})}


def send_request_to_llm(payload: dict, user_email: str) -> dict:
    business_entity: BusinessEntity = get_business_by_id_use_case(
        payload["business_id"], user_email
    )

    assistand_name = assistant_phase_mapping.get(payload["phase_type"])

    if not assistand_name:
        assistant_id = get_assistant_for_phase(payload["phase_type"])(None, payload["phase_type"])
        if not assistant_id:
            raise ValueError(f"Assistant not found for phase type: {payload['phase_type']}")
    else:
        assistant_id = business_entity.props.assistants[assistand_name].assistant_id

    context = {"business_id": business_entity.id}
    open_ai_adapter = OpenAIAdapter(context)
    open_ai_adapter.assistant_id = assistant_id

    logger.info(f"Sending request to LLM with message: {payload['message']}")

    thread_run = open_ai_adapter.create_message_thread(payload["thread_id"], payload["message"])

    response = open_ai_adapter.run_and_process_thread(thread_run)
    response = json.loads(response)
    payload.update(response)
    logger.info("Assistant:")
    logger.info(f"Received response from LLM: {response}")

    return payload
