import json
from aws_lambda_powertools import Logger

from src.models.pipefy.webhook import CardMoveEvent
from src.use_cases.hiring_process.update_phase import update_phase
from pydantic import ValidationError
logger = Logger("CardMoveEvent")


@logger.inject_lambda_context
def lambda_handler(event, context):
    """
    Lambda handler for card move event from Pipefy
    """
    logger.info("Card move event received")

    for record in event["Records"]:
        try:
            body = json.loads(record["body"])
            data = body["detail"]["data"]

            data["from_"] = data.pop("from")
            card_move_dto = CardMoveEvent(**data)
            update_phase(card_move_dto)

        except ValidationError as e:
            logger.error(f"Pydantic validation error: {e.json()}")
        except Exception as e:
            logger.error(f"Error processing record: {e}")
