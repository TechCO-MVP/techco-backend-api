from aws_lambda_powertools import Logger
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response, content_types
from aws_lambda_powertools.utilities.typing import LambdaContext

from src.use_cases.hiring_process.processing_status import get_processing_status

logger = Logger()
app = APIGatewayRestResolver()


@app.get("/hiring_process/check_status/<process_id>")
def check_processing_status(process_id: str):
    """Check the status of file processing"""
    try:
        status = get_processing_status(process_id)

        if not status:
            return Response(
                status_code=404,
                body={"message": "Process not found"},
                content_type=content_types.APPLICATION_JSON,
            )

        return Response(status_code=200, body=status, content_type=content_types.APPLICATION_JSON)

    except Exception as e:
        logger.exception("An error occurred: %s", e)
        return Response(
            status_code=500,
            body={"message": "An error occurred: %s" % e},
            content_type=content_types.APPLICATION_JSON,
        )


@logger.inject_lambda_context
def handler(event: dict, context: LambdaContext) -> dict:
    """
    Handler function for send file to assistant
    request: The request object, described like:
    {
        "body": {
            "UpdateHiringProcessCustomFieldsDTO"
        }
    }
    """

    return app.resolve(event, context)
