import json
from pprint import pprint
import traceback
from aws_lambda_powertools import Logger
from src.use_cases.hiring_process.update_phase_value import update_phase_value
from src.models.pipefy.webhook import CardFieldUpdateEvent

logger = Logger("FieldUpdateEvent")


@logger.inject_lambda_context
def lambda_handler(event, _):
    """
    Lambda handler for field update event from Pipefy
    """
    logger.info("Field update event received")

    for record in event["Records"]:
        try:
            body = json.loads(record["body"])
            data = body["detail"]["data"]

            field_update_dto = CardFieldUpdateEvent(**data)
            update_phase_value(field_update_dto)

        except Exception as e:
            logger.error(f"Error processing record: {e}")
            pprint(traceback.format_exc(), indent=2)
