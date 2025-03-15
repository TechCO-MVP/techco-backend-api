from aws_lambda_powertools import Logger

logger = Logger()


def lambda_handler(event: dict, _):
    """
    Notify the completion of the profile filter process.
    """
    try:
        logger.info("Notifying completion of profile filter process")
        logger.info(event)

        process_id: str = event.get("_id", None)
        if not process_id:
            raise Exception("The id is required")

        return event
    except Exception as e:
        logger.error(f"Error notifying completion of profile filter process: {e}")
        return {
            "status": "ERROR",
            "errorInfo": "Error notifying completion of profile filter process",
            "errorDetails": f"{e}",
        }
