from aws_lambda_powertools import Logger

logger = Logger("CardMoveEvent")


@logger.inject_lambda_context
def lambda_handler(event, context):
    """
    Lambda handler for card move event from Pipefy
    """
    logger.info("Card move event received")

    for record in event["Records"]:
        try:
            logger.info(record)
        except Exception as e:
            logger.error(f"Error processing record: {e}")
